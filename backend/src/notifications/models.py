from django.conf import settings
from django.db import models


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    notification_type = models.CharField(max_length=100)
    event_source = models.CharField(max_length=100)
    template_context = models.JSONField(default=dict)
    is_read = models.BooleanField(default=False)

    # Channel flags
    send_email = models.BooleanField(default=False)
    send_sms = models.BooleanField(default=False)
    send_socket = models.BooleanField(default=False)

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.notification_type} for {self.user}"
