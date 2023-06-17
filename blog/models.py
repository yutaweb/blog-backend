from django.db import models
from django.contrib.auth import get_user_model
from mysite.models.account_models import User
import os


class Tag(models.Model):
    slug = models.CharField(primary_key=True, unique=True, max_length=20)
    name = models.CharField(unique=True, max_length=20)
    
    def __str__(self):
        return self.slug


def upload_image_to(instance, filename):
    return os.path.join('static', 'image', 'blogs', filename)


class Article(models.Model):
    title = models.CharField(default="", max_length=30)
    text = models.TextField(default="")
    image = models.ImageField(default="", blank=True, upload_to=upload_image_to)
    author = models.CharField(default="", max_length=30)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    count = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.TextField(default="", max_length=50)
    created_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
