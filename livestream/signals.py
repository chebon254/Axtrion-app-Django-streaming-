from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import  Gift

# @receiver(post_save, sender=Comment)
# def comment_post_save(sender, instance, **kwargs):
#     # Send WebSocket message
#     message = f"{instance.user.username} commented: {instance.text}"
#     send_message_to_group(instance.video.id, message, 'comment')
