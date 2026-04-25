from django.core.cache import cache

from .models import GlobalConfig, Platform


class RuleResolver:
    CACHE_TIMEOUT = 3600  # 1 hour

    def resolve(self, platform_slug: str, rule_name: str):
        cache_key = f"rule:{platform_slug}:{rule_name}"
        cached_value = cache.get(cache_key)

        if cached_value is not None:
            return cached_value

        # Resolve rule
        try:
            global_config = GlobalConfig.objects.get(rule_name=rule_name)
            default_value = global_config.default_value
        except GlobalConfig.DoesNotExist:
            default_value = None

        try:
            platform = Platform.objects.get(slug=platform_slug)
            platform_value = platform.rule_overrides.get(
                rule_name, default_value,
            )
        except Platform.DoesNotExist:
            platform_value = default_value

        # Cache and return
        cache.set(cache_key, platform_value, self.CACHE_TIMEOUT)
        return platform_value

    def invalidate_platform_rules(self, platform_slug: str):
        # In a real scenario, we might want to track keys or use a pattern
        # Redis supports keys but it's not efficient.
        # For this prototype, we'll assume resolution is updated on next expiry or manual clear.
        pass
