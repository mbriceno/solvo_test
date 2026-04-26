from typing import Any
from unittest.mock import MagicMock

import pytest

from platforms.models import GlobalConfig, Platform
from platforms.rule_resolver import RuleResolver


@pytest.fixture
def mock_rule_resolver(mocker: Any) -> RuleResolver:
    return RuleResolver()


@pytest.mark.django_db
def test_rule_resolver_merging(mocker: Any) -> None:
    # Setup
    mock_cache = MagicMock()
    mock_cache.get.return_value = None
    mocker.patch("platforms.rule_resolver.cache", new=mock_cache)
    mocker.patch("platforms.signals.cache", new=mock_cache)

    global_config = GlobalConfig.objects.create(
        rule_name="max_devices",
        default_value={"value": 5},
    )
    platform = Platform.objects.create(
        slug="test-platform",
        rule_overrides={"max_devices": 3},
    )
    resolver = RuleResolver()

    # Execute
    value = resolver.resolve(platform.slug, "max_devices")

    # Verify
    assert value == 3


@pytest.mark.django_db
def test_rule_resolver_fallback(mocker: Any) -> None:
    # Setup
    mock_cache = MagicMock()
    mock_cache.get.return_value = None
    mocker.patch("platforms.rule_resolver.cache", new=mock_cache)
    mocker.patch("platforms.signals.cache", new=mock_cache)

    global_config = GlobalConfig.objects.create(
        rule_name="max_devices",
        default_value={"value": 5},
    )
    platform = Platform.objects.create(slug="empty-platform", rule_overrides={})
    resolver = RuleResolver()

    # Execute
    value = resolver.resolve(platform.slug, "max_devices")

    # Verify
    assert value == {"value": 5}
