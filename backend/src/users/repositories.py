from django.db.models import QuerySet

from core.base import BaseRepository
from platforms.models import Platform

from .models import CustomUser, Device


class UserRepository(BaseRepository[CustomUser]):
    model = CustomUser

    def get_by_email_and_platform(
        self, email: str, platform: Platform,
    ) -> CustomUser:
        return self.model.objects.get(email=email, platform=platform)


class DeviceRepository(BaseRepository[Device]):
    model = Device

    def find_by_user_and_platform(
        self, user: CustomUser, platform: Platform,
    ) -> QuerySet[Device]:
        """
        Retrieves all devices for a specific user and platform.
        """
        return self.model.objects.filter(user=user, platform=platform)

    def get_active_count_for_user(
        self, user: CustomUser, platform: Platform,
    ) -> int:
        return self.model.objects.filter(
            user=user, platform=platform, is_active=True,
        ).count()
