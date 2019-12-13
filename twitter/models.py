from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from stream_django import activity
from django.db import models
from django.utils import timezone


class Tweet(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def publish(self):
        self.created_at = timezone.now()
        self.save()


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    target = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
