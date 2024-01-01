from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from main.models import UserProfile  # Make sure to adjust the import path if needed

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, full_name=instance.username)
