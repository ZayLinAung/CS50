from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("listingPage/<str:auction_id>", views.listingPage, name="listingPage"),
    path("watchlist", views.WatchList, name = "watchlist"),
    path("bid/<str:auction_id>", views.Bid, name = "bid"),
    path("closedauction", views.ClosedAuction, name = "closedAuction"),
    path("comments/<str:auction_id>", views.addComments, name = "comments"),
    path("category/<str:item>", views.Category, name = "category"),
]
