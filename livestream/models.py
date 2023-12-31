from django.db import models
from django.contrib.auth.models import User

class LiveStream(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    livestream_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    stream_key = models.CharField(max_length=255, unique=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

class Gift(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='livestream/gifts/')

class Like(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='livestream/like/')