from typing import Generic, TypeVar

from django.db import models

T = TypeVar("T", bound=models.Model)


class BaseRepository(Generic[T]):
    model: type[T]

    def get_all(self) -> list[T]:
        return list(self.model.objects.all())

    def get_by_id(self, id: int) -> T | None:
        try:
            return self.model.objects.get(id=id)
        except self.model.DoesNotExist:
            return None


class BaseService:
    pass


class BaseSelector:
    pass
