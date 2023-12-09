
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.newPost, name="newPost"),
    path("profilePage/<str:user>/", views.profilePage, name="profilePage"),
    path("following", views.following, name="following"),
    path("prototype", views.prototype, name="prototype")
]
