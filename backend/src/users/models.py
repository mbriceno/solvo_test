from django.contrib.auth.models import AbstractUser
from django.db import models
from platforms.models import Platform


class CustomUser(AbstractUser):
    email = models.EmailField()
    platform = models.ForeignKey(
        Platform, on_delete=models.CASCADE, related_name="users",
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=["email", "platform"], name="unique_email_per_platform",
            ),
        )

    # Use email and platform for authentication if needed, but standard
    # username is still there by default in AbstractUser.
    # We might want to override username or use email as primary.
    # For now, following spec's multi-tenant identity.


class Device(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="devices",
    )
    platform = models.ForeignKey(
        Platform, on_delete=models.CASCADE, related_name="devices",
    )
    name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "platform"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.user.email})"
