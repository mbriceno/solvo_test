from core.notifications import dispatch_notification
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def user_registered_handler(sender, instance, created, **kwargs):
    if created:
        dispatch_notification(
            "user_registered",
            email=instance.email,
            platform=instance.platform.slug,
        )
