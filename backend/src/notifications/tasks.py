from celery import shared_task
from django.utils import timezone

from .dispatcher import NotificationDispatcher
from .models import Notification


@shared_task
def dispatch_notification(notification_id: int) -> None:
    try:
        notification = Notification.objects.get(id=notification_id)
    except Notification.DoesNotExist:
        return

    channels = {
        "email": notification.send_email,
        "sms": notification.send_sms,
        "socket": notification.send_socket,
    }

    dispatcher = NotificationDispatcher()
    dispatcher.dispatch(channels, notification.template_context)

    notification.sent_at = timezone.now()
    notification.save()
