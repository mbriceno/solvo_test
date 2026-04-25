from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import GlobalConfig, Platform
from .rule_resolver import RuleResolver


@receiver(post_save, sender=Platform)
def platform_updated_handler(sender, instance: Platform, **kwargs) -> None:
    """
    Clear cached rules for a specific platform when its overrides change.
    """
    RuleResolver().invalidate_platform_rules(instance.slug)


@receiver(post_save, sender=GlobalConfig)
def global_config_updated_handler(sender, **kwargs) -> None:
    """
    When a global rule changes, it might affect all platforms.
    We clear the full cache to ensure consistency.
    """
    cache.clear()
