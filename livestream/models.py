from django.db import models
from django.contrib.auth.models import User

class Livestream(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='livestream_thumbnails/', blank=True, null=True)
    is_live = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.title} - {self.user.username}'
