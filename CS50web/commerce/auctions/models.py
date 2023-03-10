from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass

class Auctions(models.Model):
    username = models.CharField(max_length = 64, default="")
    title = models.CharField(max_length = 64)
    description = models.CharField(max_length = 5000)
    startbid = models.DecimalField(max_digits = 10, decimal_places = 3)
    category = models.CharField(max_length = 64, default="")
    image = models.CharField(max_length = 1000)
    time = models.CharField(max_length = 100, default="")
    closed = models.BooleanField(default=False)

class Bids(models.Model):
    currentBid = models.DecimalField(default = 0, max_digits = 10, decimal_places = 3)
    currentBidder = models.CharField(max_length = 64)
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="bidauction")

class Watchlist(models.Model):
    username = models.CharField(max_length = 64, default="")
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="WLauction")

class Comments(models.Model):
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="CMauction")
    username = models.CharField(max_length = 64, default="")
    comment = models.CharField(max_length = 5000)