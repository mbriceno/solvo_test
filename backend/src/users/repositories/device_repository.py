from core.base import BaseRepository
from django.db.models import QuerySet
from platforms.models import Platform

from users.models import CustomUser, Device


class DeviceRepository(BaseRepository[Device]):
    model = Device

    def find_by_user_and_platform(
        self, user: CustomUser, platform: Platform,
    ) -> QuerySet[Device]:

        return self.model.objects.filter(user=user, platform=platform)

    def get_active_count_for_user(
        self, user: CustomUser, platform: Platform,
    ) -> int:
        return self.model.objects.filter(
            user=user, platform=platform, is_active=True,
        ).count()
