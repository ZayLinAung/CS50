from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Playlist(models.Model):
    username = models.CharField(max_length = 64)
    artist = models.CharField(max_length = 64)
    title = models.CharField(max_length = 64)
    uri = models.CharField(max_length = 64)
    albumUrl = models.CharField(max_length = 64)
