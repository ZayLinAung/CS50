from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('login', views.login_view, name = 'login'),
    path('logout', views.logout_view, name = 'logout'),
    path('register', views.register, name = 'register'),
    path('search', views.search, name = 'search'),
    path('chooseMedia', views.chooseMedia, name = 'chooseMedia'),
    path('gptSearch', views.gptSearch, name = 'gptSearch'),
    path('spotifyLogin', views.spotifyLogin, name = 'spotifyLogin'),
    path('callback', views.spotifyCallback, name = 'callback'),
    path('playlist', views.playlist, name = 'playlist')
]