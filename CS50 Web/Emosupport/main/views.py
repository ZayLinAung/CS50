import json
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
import urllib.parse
from openai import OpenAI
import json, requests, datetime

from .models import *

CLIENT_ID = '615aab0b7e6d47f98f43fba9b9748332'
CLIENT_SECRET = '98bcb10235a6484a8fa6dad37e4aea4a'
REDIRECT_URI = 'http://127.0.0.1:8000/callback'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

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
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


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
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username = username, email = email, password = password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


def index(request):
    return render(request, 'index.html')


def spotifyCallback(request):
    if (request.GET.get('error') != None):
        return redirect('chooseMedia')
    req_body = {
        'code': request.GET.get('code'),
        'grant_type': "authorization_code",
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data = req_body)
    token_info = response.json()
    request.session['access_token'] = token_info['access_token']
    request.session['refresh_token'] = token_info['refresh_token']
    request.session['expires_at'] = datetime.datetime.now().timestamp() + token_info['expires_in']
    return redirect('search')


@login_required
def search(request):
    return render(request, 'search.html')


def chooseMedia(request):
    return render(request, 'chooseMedia.html')

def gptSearch(request):
    if request.method == 'POST':
        feeling = request.POST['feeling']
        genre = request.POST['genre']
        description = request.POST['feeling']
        artist = request.POST['artist']
        data = json.loads(gptPrompt(feeling, genre, artist, description))
        song_list = spotifySearch(request, data)

        return render(request, "spotifyResult.html", {
            'data': json.dumps(song_list)
        })
    

def spotifySearch(request, data):
    if datetime.datetime.now().timestamp() > request.session['expires_at']:
        return redirect('refresh_token')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {request.session['access_token']}"
    }

    json_list = []

    for key in data:
        for song in data[key]:
            music = song['musicName']
            artist = song['artist']
            response = requests.get(API_BASE_URL + f'search?q={artist}%{music}&type=track&limit=3', headers = headers)
            json_list.append(response.json())
    
    playlist = Playlist.objects.filter(username = request.user.username)

    uris = []
    for song in playlist:
        uris.append(song.uri)
    
    song_list = []

    for data in json_list:
        for song in data['tracks']['items']:
            song_list.append({
                'artist': song['artists'][0]['name'],
                'title': song['name'],
                'uri': song['uri'].split(':')[-1],
                'albumUrl': song['album']['images'][0]['url'],
                'inPlaylist': song['uri'].split(':')[-1] in uris
            })
        
    return song_list


def gptPrompt(feeling, genre, artist, description):
    client = OpenAI()

    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "You are a helpful assistant that generates JSON. You always return just the JSON with no additonal description or context."},
        {"role": "user", "content": 
         f"I am feeling {feeling}. My music description is {description}. The artist must be {artist}. Pleae give me JSON object that represents at least 10 spotify music that aligns with my mood. The genre is {genre} It should have fields 'musicName' and 'artist'"}
    ]
    )
    return(response.choices[0].message.content)


def spotifyLogin(request):
    scope = 'user-read-private user-read-email'

    params = {
        'client_id': CLIENT_ID,
        'response_type' : 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)

@csrf_exempt
def playlist(request):
    if request.method == 'POST' or request.method == 'PUT':
        if request.method == 'PUT':
            data = json.loads(request.body)
            artist = data.get('artist')
            title = data.get('title')
            albumUrl = data.get('albumUrl')
            uri = data.get('uri')

        elif request.method == 'POST':
            artist = request.POST['artist']
            title = request.POST['title']
            albumUrl = request.POST['albumUrl']
            uri = request.POST['uri']


        if Playlist.objects.filter(username = request.user.username, uri = uri).count() == 0:
            newPlaylist = Playlist.objects.create(username = request.user.username, artist = artist, title = title, albumUrl = albumUrl, uri = uri)
            newPlaylist.save()
        else:
            Playlist.objects.get(username = request.user.username, artist = artist, title = title, albumUrl = albumUrl, uri = uri).delete()
        

    playlists = list(Playlist.objects.filter(username = request.user.username).values())
    for dic in playlists:
        dic['inPlaylist'] = True

    return render(request, "playlist.html", {
        'data': json.dumps(playlists)
    })