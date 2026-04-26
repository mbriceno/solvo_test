from typing import Any
from unittest.mock import MagicMock

import pytest

from platforms.models import GlobalConfig, Platform


@pytest.mark.django_db
def test_platform_repository_crud(mocker: Any) -> None:
    # Setup: Mock cache to prevent Redis connection errors during signal handling
    mock_cache = MagicMock()
    mocker.patch("platforms.rule_resolver.cache", new=mock_cache)
    mocker.patch("platforms.signals.cache", new=mock_cache)

    # Create GlobalConfig
    global_config = GlobalConfig.objects.create(
        rule_name="max_devices",
        default_value={"value": 5},
    )

    # Create Platform
    platform = Platform.objects.create(
        name="Test Platform",
        slug="test-platform",
        rule_overrides={"max_devices": 3},
    )

    # Read Platform by slug
    found_platform = Platform.objects.get(slug="test-platform")
    assert found_platform.name == "Test Platform"
    assert found_platform.rule_overrides == {"max_devices": 3}

    # Update Platform
    platform.name = "Updated Platform"
    platform.rule_overrides["max_devices"] = 4  # Update override
    platform.save()
    found_platform.refresh_from_db()
    assert found_platform.name == "Updated Platform"
    assert found_platform.rule_overrides["max_devices"] == 4

    # Delete Platform
    platform.delete()
    assert Platform.objects.count() == 0

    # Create GlobalConfig for fallback test
    global_config_fallback = GlobalConfig.objects.create(
        rule_name="another_rule",
        default_value={"value": 10},
    )
    platform_no_override = Platform.objects.create(
        name="No Override Platform",
        slug="no-override-platform",
        rule_overrides={},
    )
    # Read rule that should fallback to global
    found_global_config = GlobalConfig.objects.get(rule_name="another_rule")
    assert found_global_config.default_value == {"value": 10}
