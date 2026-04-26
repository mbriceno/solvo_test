from django.db.models import QuerySet
from platforms.models import Platform
from platforms.rule_resolver import RuleResolver
from rest_framework.exceptions import PermissionDenied

from users.models import CustomUser, Device
from users.repositories import DeviceRepository


class DeviceService:

    def __init__(
        self, repository: DeviceRepository, rule_resolver: RuleResolver,
    ) -> None:
        self.repository = repository
        self.rule_resolver = rule_resolver

    def get_devices_for_user_on_platform(
        self, user: CustomUser, platform: Platform,
    ) -> QuerySet[Device]:

        return self.repository.find_by_user_and_platform(user, platform)

    def register_device(
        self, user: CustomUser, platform: Platform, name: str, ip_address: str,
    ) -> Device:

        max_devices = self.rule_resolver.resolve(platform.slug, "max_devices")
        if max_devices is not None:
            current_count = self.repository.get_active_count_for_user(
                user, platform,
            )
            if current_count >= max_devices:
                raise PermissionDenied(
                    "Device limit reached for this platform.",
                )

        return self.repository.model.objects.create(
            user=user,
            platform=platform,
            name=name,
            ip_address=ip_address,
        )
