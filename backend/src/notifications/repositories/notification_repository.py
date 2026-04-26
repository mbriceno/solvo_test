from core.base import BaseRepository
from django.db.models import QuerySet
from users.models import CustomUser

from notifications.models import Notification


class NotificationRepository(BaseRepository[Notification]):
    model = Notification

    def create(self, **fields) -> Notification:
        return self.model.objects.create(**fields)

    def get_for_user(self, user: CustomUser) -> QuerySet[Notification]:
        return self.model.objects.filter(user=user)
