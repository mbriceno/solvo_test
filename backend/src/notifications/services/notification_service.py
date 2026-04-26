from platforms.rule_resolver import RuleResolver
from users.models import CustomUser

from ..repositories import NotificationRepository
from ..tasks import dispatch_notification


class NotificationService:
    def __init__(
        self,
        repository: NotificationRepository,
        rule_resolver: RuleResolver,
    ) -> None:
        self.repository = repository
        self.rule_resolver = rule_resolver

    def trigger_notification(
        self,
        user: CustomUser,
        notification_type: str,
        event_source: str,
        context: dict,
    ) -> None:
        platform_slug = user.platform.slug

        # Resolve rules for each channel
        send_email = self.rule_resolver.resolve(
            platform_slug, f"notify_{notification_type.lower()}_email"
        )
        send_sms = self.rule_resolver.resolve(
            platform_slug, f"notify_{notification_type.lower()}_sms"
        )
        send_socket = self.rule_resolver.resolve(
            platform_slug, f"notify_{notification_type.lower()}_socket"
        )

        # Create record
        notification = self.repository.create(
            user=user,
            notification_type=notification_type,
            event_source=event_source,
            template_context=context,
            send_email=bool(send_email),
            send_sms=bool(send_sms),
            send_socket=bool(send_socket),
        )

        # Enqueue dispatch task
        dispatch_notification.delay(notification.id)
