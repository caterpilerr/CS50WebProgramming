import decimal
from datetime import datetime, timedelta
from pytz import UTC

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import CharField, Value
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .forms import ListingForm, BidForm, CommentForm
from .models import User, Listing, Bid, WatchlistItem, Comment
from .util import get_min_bid


def index(request):
    return listings_view(request)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def new_listing(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = ListingForm(request.POST, request.FILES)
            if form.is_valid():
                owner = User.objects.get(id=request.user.id)
                try:
                    listing = Listing.objects.get(
                        title=form.cleaned_data["title"],
                        owner=owner
                    )
                except Listing.DoesNotExist:
                    listing = Listing(
                        title=form.cleaned_data["title"],
                        description=form.cleaned_data["description"],
                        category=form.cleaned_data["category"],
                        start_price=form.cleaned_data["start_price"],
                        price=form.cleaned_data["start_price"],
                        image=form.cleaned_data["photo"],
                        start_date=datetime.today(),
                        end_date=datetime.today() +
                        timedelta(days=int(form.cleaned_data["duration"])),
                        owner=owner
                    )
                    listing.save()
                    messages.success(request, "Item listed successfully!")
                    return HttpResponseRedirect(reverse("index"))
                messages.error(request, "You already listed item with same name!")
    else:
        form = ListingForm()
    return render(request, "auctions/new_listing.html", {
        "form": form
    })


def listing(request, id):
    listing = Listing.objects.get(id=id)
    comments = listing.comments.all()

    bid_form = BidForm()
    comment_form = CommentForm()

    min_bid = get_min_bid(listing)
    bids_number = listing.bids.count()
    is_ended = listing.end_date < datetime.today()
    is_in_watchlist = False
    is_bid = False
    is_highest = False

    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        is_in_watchlist = user.watchlist.filter(listing=listing).exists()
        is_bid = listing.bids.filter(bidder=user).exists()
        if bids_number:
            is_highest = listing.bids.order_by("value").last().bidder == user
        if request.method == "POST":
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                value = bid_form.cleaned_data["value"]
                if value >= min_bid:
                    Bid.objects.update_or_create(
                        bidder=user,
                        listing=listing,
                        defaults={"value": value}
                    )
                    listing.price = value
                    listing.save()
                    messages.success(request, "You have made a bid!")
                    return HttpResponseRedirect(reverse("listing", args=[listing.id,]))
                messages.error(request, "Your bid is less than current price!")
    return render(request, "auctions/listing.html", {
        "bid_form": bid_form,
        "comment_form": comment_form,
        "listing": listing,
        "comments": comments,
        "min_bid": min_bid,
        "bids_number": bids_number,
        "is_in_watchlist": is_in_watchlist,
        "is_bid": is_bid,
        "is_highest": is_highest,
        "is_ended": is_ended,
    })
 

def watchlist(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        listing = Listing.objects.get(id=request.POST["listing_id"])
        if user.watchlist.filter(listing=listing).exists():
            WatchlistItem.objects.get(owner=user, listing=listing).delete()
            messages.success(request, "Removed from watchlist!")
        else:
            WatchlistItem.objects.create(owner=user, listing=listing)
            messages.success(request, "Item added to watchlist!")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    
    print(watchlist)
    listings = Listing.objects.filter(
        id__in=user.watchlist.values("listing")
    )
    
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


def post_comment(request):
    if request.user.is_authenticated and request.method == "POST":
        listing = Listing.objects.get(id=request.POST["listing_id"])
        user = User.objects.get(id=request.user.id)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = Comment(
                title=comment_form.cleaned_data["title"],
                content=comment_form.cleaned_data["content"],
                listing=listing,
                author=user,
                time=datetime.now()
            )
            comment.save()
            messages.success(request, "Comment added!")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


def listings_view(request, category=None):
    if category:
        listings = Listing.objects.filter(category=category, end_date__gt=datetime.now())
    else:
        listings = Listing.objects.filter(end_date__gt=datetime.now())
    return render(request, "auctions/index.html", context={
        "listings": listings,
        "category": category
    })


def bids(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        bids = user.bids.all()
        for bid in bids:
            bid.is_highest = bid.listing.bids.order_by("value").last().bidder == user
            bid.listing.is_ended = bid.listing.end_date < datetime.today()

        return render(request, "auctions/bids.html", {
            "bids" : bids
        })
