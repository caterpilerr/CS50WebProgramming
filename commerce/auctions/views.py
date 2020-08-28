import decimal
from datetime import datetime, timedelta
from pytz import UTC

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .forms import ListingForm, BidForm
from .models import User, Listing, Bid, WatchlistItem
from .util import get_bid_increment


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", context={
        "listings": listings
    })


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
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                owner = User.objects.get(id=request.user.id)
                listing = Listing.objects.get(
                    title=form.cleaned_data["title"],
                    owner=owner
                )
            except Listing.DoesNotExist:
                listing = Listing(
                    title=form.cleaned_data["title"],
                    description=form.cleaned_data["description"],
                    start_price=form.cleaned_data["start_price"],
                    price=form.cleaned_data["start_price"],
                    image=form.cleaned_data["photo"],
                    start_date=datetime.today(),
                    end_date=datetime.today() + 
                        timedelta(days=int(form.cleaned_data["duration"])),
                    owner=owner
                )
                listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()
    return render(request, "auctions/new_listing.html", {
        "form": form
    })


def listing(request, id):
    listing = Listing.objects.get(id=id)
    bid_increment = get_bid_increment(listing)
    min_bid = listing.price + bid_increment
    bids_number = listing.bids.count()

    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        is_watched = user.watchlist.filter(listing=listing).exists()
        if request.method == "POST":
            form = BidForm(request.POST)
            if form.is_valid():
                if form.cleaned_data["value"] >= min_bid:
                    bid = Bid(
                        value=form.cleaned_data["value"],
                        bidder=user,
                        listing=listing
                    )
                    bid.save()
                    listing.price = bid.value
                    listing.save()
                    messages.success(request, "You have made a bid!")
                    return HttpResponseRedirect(reverse("listing", args={listing.id}))
                messages.error(request, "Your bid is less than current price!")
        else:
            form = BidForm()
            return render(request, "auctions/listing.html", {
                "form": form,
                "listing": listing,
                "min_bid": min_bid,
                "bids_number": bids_number,
                "is_watched": is_watched
            })
    else:
        return render(request, "auctions/listing.html", {
            "form": form,
            "listing": listing,
            "min_bid": min_bid,
            "bids_number": bids_number
        })
    


def add_to_watchlist(request):
    if request.method == "POST":
        listing = Listing.objects.get(id=request.POST["listing_id"])
        user = User.objects.get(id=request.user.id)
        if user.watchlist.filter(listing=listing).exists():
            messages.error(request, "Item is already in watchlist!")
        else:
            WatchlistItem.objects.create(owner=user, listing=listing)
            messages.success(request, "Item added to watchlist!")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


def remove_from_watchlist(request):
    if request.method == "POST":
        listing = Listing.objects.get(id=request.POST["listing_id"])
        user = User.objects.get(id=request.user.id)
        if user.watchlist.filter(listing=listing).exists():
            WatchlistItem.objects.get(owner=user, listing=listing).delete()
            messages.success(request, "Removed from watchlist!")
        else:
            messages.error(request, "Item already removed!")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
