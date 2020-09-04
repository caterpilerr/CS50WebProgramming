from django.contrib.auth.models import AbstractUser
from django.db import models

from . import util



class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    CATEGORIES_CHOICES = [
        ("fashion", "Fashion"),
        ("electronics", "Electronics"),
        ("home", "Home"),
        ("hobby", "Hobby"),
        ("toys", "Toys"),
        ("other", "Other")
    ]
    title = models.CharField(max_length=64)
    description = models.TextField(blank=False)
    category = models.CharField(max_length=64, choices=CATEGORIES_CHOICES)
    start_price = models.DecimalField(max_digits=13, decimal_places=2)
    price = models.DecimalField(max_digits=13, decimal_places=2)
    image = models.ImageField(upload_to=util.user_directory_path, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"{self.title}, price: {self.price}$"


class Bid(models.Model):
    value = models.DecimalField(max_digits=13, decimal_places=2)
    bidder = models.ForeignKey("User", on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"Bid: {self.value}$ on {self.listing} by {self.bidder}"


class WatchlistItem(models.Model):
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE)

    def __str__(self):
        return f"Watching {self.listing} by {self.owner}"

    
class Comment(models.Model):
    title = models.CharField(max_length=40)
    content = models.CharField(max_length=140)
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="comments")
    time = models.DateTimeField()

    def __str__(self):
        return f"Comment by {self.author} on {self.listing} at {self.time}"
