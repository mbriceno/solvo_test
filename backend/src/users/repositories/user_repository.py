from core.base import BaseRepository
from platforms.models import Platform

from users.models import CustomUser


class UserRepository(BaseRepository[CustomUser]):
    model = CustomUser

    def get_by_email_and_platform(
        self, email: str, platform: Platform,
    ) -> CustomUser:
        return self.model.objects.get(email=email, platform=platform)
