from notifications.services import NotificationService
from platforms.models import Platform
from users.models import CustomUser
from users.services import UserService


class AuthService:
    def __init__(
        self,
        user_service: UserService,
        notification_service: NotificationService,
    ) -> None:
        self.user_service = user_service
        self.notification_service = notification_service

    def register_user(
        self,
        email: str,
        password: str,
        platform: Platform,
        **extra_fields,
    ) -> CustomUser:
        user = self.user_service.create_user(
            email=email,
            password=password,
            platform=platform,
            **extra_fields,
        )

        # Trigger notification
        self.notification_service.trigger_notification(
            user=user,
            notification_type="REGISTRATION",
            event_source="auth_service",
            context={"welcome_name": user.email},
        )

        return user
