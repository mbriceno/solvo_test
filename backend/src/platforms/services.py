from .repositories import PlatformRepository


class PlatformService:
    def __init__(self, repository: PlatformRepository):
        self.repository = repository

    def get_platform_by_slug(self, slug: str):
        return self.repository.get_by_slug(slug)
