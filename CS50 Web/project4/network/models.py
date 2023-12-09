from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follower = models.JSONField()
    following = models.JSONField()
    pass


class Post(models.Model):
    username = models.CharField(max_length = 64)
    content = models.CharField(max_length = 5000)
    time = models.CharField(max_length = 100)
    likes = models.IntegerField(default = 0)

    def __str__(self):
        return f"{self.id}: {self.username}, {self.content}, {self.time}"