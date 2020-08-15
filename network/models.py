from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("User", blank=True, related_name="followers")
    liked_posts = models.ManyToManyField("Post", blank=True, related_name="likers")

class Post(models.Model):
    content = models.CharField(max_length=1024)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts_created")

    def __str__(self):
        return f"{self.content[:10]}... by {self.author.username}"
