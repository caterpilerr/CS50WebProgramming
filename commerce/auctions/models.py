from django.contrib.auth.models import AbstractUser
from django.db import models

from . import util


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(blank=False)
    start_price = models.DecimalField(max_digits=13, decimal_places=2)
    price = models.DecimalField(max_digits=13, decimal_places=2)
    image = models.FileField(upload_to=util.images_directory_path())

    def __str__(self):
        return f"{self.title}, price: {self.price}$"


class Bid(models.Model):
    value = models.DecimalField(max_digits=13, decimal_places=2)
    bidder = models.ForeignKey("User", on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"Bid: {self.value}$ on {self.listing} by {self.bidder}"


    
