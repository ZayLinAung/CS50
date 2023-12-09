from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required

from .models import *

def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auctions.objects.all().order_by('-id')
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

@login_required
def createListing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        startbid = request.POST["startbid"]
        category = request.POST["category"]
        image = request.POST["image"]
        time = datetime.now().strftime("%Y-%m-%d %I:%M %p")

        p = Auctions.objects.create(username = request.user.username, title=title,description=description,startbid=startbid,category=category,image=image,time=time)
        p.save()
        return render(request, "auctions/index.html",{
            "auctions": reversed(Auctions.objects.all())
        })
    else:
        return render(request, "auctions/createList.html")

def listingPage(request,auction_id):
    auction = Auctions.objects.get(pk=auction_id)
    comments = Comments.objects.filter(auction = auction)
    bidAuction = Bids.objects.filter(auction = auction).first()
    if bidAuction == None:
        Bids.objects.create(currentBid = auction.startbid, auction = auction)
        bidAuction = Bids.objects.get(auction = auction)
    inWatchList = Watchlist.objects.filter(username = request.user.username, auction = auction).exists()
    return render(request, "auctions/listingPage.html",{
        "auctions": Auctions.objects.get(id=auction_id),
        "inWatchList": inWatchList,
        "bidAuction": bidAuction,
        "comments": comments
    })

@login_required
def WatchList(request):
    if request.method == "POST":
        auction_id = request.POST["auction_id"]
        auction = Auctions.objects.get(pk=auction_id)
        if Watchlist.objects.filter(username = request.user.username, auction = auction).exists():
            Watchlist.objects.get(username = request.user.username, auction = auction).delete()
        else:
            p = Watchlist.objects.create(username = request.user.username, auction = auction)
            p.save()
        return redirect("/listingPage/" + auction_id)
    else:
        myWatchlist = Watchlist.objects.filter(username= request.user.username)
        return render(request, "auctions/watchlist.html", {
            "myWatchlist": myWatchlist
        })

def Bid(request, auction_id):
    if request.method == "POST":
        auction = Auctions.objects.get(pk=auction_id)
        bidObj = Bids.objects.get(auction = auction)
        newbid = request.POST["newbid"]
        bidObj.currentBidder = request.user.username
        bidObj.currentBid = newbid
        bidObj.save()
        return redirect("/listingPage/" + auction_id)

def ClosedAuction(request):
    if request.method == "POST":
        auction_id = request.POST["auction_id"]
        auction = Auctions.objects.get(pk=auction_id)
        auction.closed = True
        auction.save()

    return render(request, "auctions/closedAuction.html", {
        "auctions": Auctions.objects.all().order_by('-id')
    })

def addComments(request, auction_id):
     if request.method == "POST":
        auction = Auctions.objects.get(pk=auction_id)
        comment = request.POST["comment"]
        newComment = Comments.objects.create(auction = auction, username = request.user.username, comment = comment)
        newComment.save()
        return redirect("/listingPage/" + auction_id)

def Category(request, item):
    auction = Auctions.objects.filter(category = item).order_by('-id')
    return render(request, "auctions/index.html", {
        "auctions": auction
    })