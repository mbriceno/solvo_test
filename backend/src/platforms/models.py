from django.db import models


class GlobalConfig(models.Model):
    rule_name = models.CharField(max_length=255, unique=True)
    default_value = models.JSONField()

    def __str__(self) -> str:
        return self.rule_name


class Platform(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    rule_overrides = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return self.name
