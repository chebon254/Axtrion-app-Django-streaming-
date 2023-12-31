from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image_uploads/profile_images/', blank=True, null=True)
    full_name = models.CharField(max_length=255)
    bio = models.TextField()

    def __str__(self):
        return self.user.username

class UserFollowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=10, choices=[('short', 'Short'), ('long', 'Long')])
    duration = models.PositiveIntegerField(blank=True, null=True)  # Duration in seconds
    upload_date = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='main/thumbnails/', blank=True, null=True)
    custom_thumbnail = models.ImageField(upload_to='main/custom_thumbnails/', blank=True, null=True)
    file = models.FileField(upload_to='main/uploaded_videos/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Signal to automatically update video category based on duration
@receiver(pre_save, sender=Video)
def update_video_category(sender, instance, **kwargs):
    if instance.duration is not None and instance.duration <= 70:
        instance.category = 'short'
    else:
        instance.category = 'long'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.text}'

class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.video.title} - {self.timestamp}'

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.message}'