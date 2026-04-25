from django.apps import AppConfig


class PlatformsAppConfig(AppConfig):
    name = "platforms"

    def ready(self) -> None:
        import platforms.signals  # noqa: F401
