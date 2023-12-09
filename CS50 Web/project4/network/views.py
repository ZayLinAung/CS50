import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.core.serializers import serialize
import time
from django.views.decorators.csrf import csrf_exempt

from .models import *

dataToPass = ''
selectedUser = ''

def index(request):
    global dataToPass
    dataToPass = 'index'
    return render(request, "network/index.html")


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })
        followerJSON = {"followers": []}
        followingJSON = {"following": []}

        # Attempt to create new user
        try:
            user = User.objects.create_user(username = username, email = email, password = password, follower = followerJSON, following = followingJSON)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def newPost(request):
    if request.method == "POST":
        username = request.user.username
        content = request.POST["content"]
        time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        p = Post.objects.create(username=username, content = content, time=time)
        p.save()
        return render(request, "network/index.html", {
            "Posts": Post.objects.all().order_by('-id')
            })

def profilePage(request, user):
    currentUser = User.objects.get(username = request.user.username)
    profileUser = User.objects.get(username = user)
    global dataToPass, selectedUser
    dataToPass = 'profilePage'
    selectedUser = user

    if request.method == "POST":

        if user in currentUser.following["following"]:
            currentUser.following["following"].remove(user)
            profileUser.follower["followers"].remove(request.user.username)
        else:
            currentUser.following["following"].append(user)
            profileUser.follower["followers"].append(request.user.username)
        currentUser.save()
        profileUser.save()

    return render(request, "network/profilePage.html", {
            "Users": profileUser,
            "currentUser" : currentUser,
            "follower" : len(profileUser.follower["followers"]),
            "following" : len(profileUser.following["following"])
    })

def following(request):
    global dataToPass
    dataToPass = 'following'
    return render(request, "network/following.html")

@csrf_exempt
def prototype(request):

    if request.method == "PUT":
        data = json.loads(request.body)
        updatePost = Post.objects.get(id = data.get('id'))
        if data.get('content') != None:
            updatePost.content = data.get('content')
        else:
            updatePost.likes = data.get('num_likes')
        updatePost.save()
        return HttpResponse(status=204)

    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))

    global dataToPass, selectedUser
    if dataToPass == 'following':
        currentUser = User.objects.get(username = request.user.username)
        posts = Post.objects.values().filter(username__in = currentUser.following["following"]).order_by('-id')

    if dataToPass == 'index':
        posts = Post.objects.values().all().order_by('-id')

    if dataToPass == 'profilePage':
        posts = Post.objects.values().filter(username = selectedUser).order_by('-id')

    data = []
    for i in range(start-1, end + 1):
        if (i < len(posts)):
            data.append(posts[i])

    JSON = {'posts' : data, 'total': len(posts)}

    return JsonResponse(JSON)