from core.base import BaseRepository

from platforms.models import Platform


class PlatformRepository(BaseRepository[Platform]):
    model = Platform

    def get_by_slug(self, slug: str) -> Platform:
        return self.model.objects.get(slug=slug)
