from typing import Any
from unittest.mock import MagicMock

import pytest
from platforms.models import Platform

from users.models import CustomUser, Device
from users.repositories import DeviceRepository


@pytest.mark.django_db
def test_device_repository_find_by_user_and_platform(mocker: Any) -> None:
    # Setup
    mocker.patch("django_redis.get_redis_connection")
    mocker.patch(
        "django.core.cache.caches.__getitem__", return_value=MagicMock(),
    )
    mocker.patch("platforms.rule_resolver.cache")
    mocker.patch("platforms.signals.cache")

    platform1 = Platform.objects.create(slug="platform1", name="P1")
    platform2 = Platform.objects.create(slug="platform2", name="P2")
    user1 = CustomUser.objects.create(
        username="u1", email="user1@test.com", platform=platform1,
    )
    user2 = CustomUser.objects.create(
        username="u2", email="user2@test.com", platform=platform2,
    )

    device1 = Device.objects.create(
        user=user1, platform=platform1, name="d1", ip_address="1.1.1.1",
    )
    device2 = Device.objects.create(
        user=user1, platform=platform2, name="d2", ip_address="1.1.1.2",
    )
    device3 = Device.objects.create(
        user=user2, platform=platform1, name="d3", ip_address="1.1.1.3",
    )

    repo = DeviceRepository()

    # Execute
    devices = repo.find_by_user_and_platform(user1, platform1)

    # Verify
    assert device1 in devices
    assert device2 not in devices
    assert device3 not in devices


@pytest.mark.django_db
def test_device_repository_count_active_devices(mocker: Any) -> None:
    # Setup
    mocker.patch("django_redis.get_redis_connection")
    mocker.patch(
        "django.core.cache.caches.__getitem__", return_value=MagicMock(),
    )
    mocker.patch("platforms.rule_resolver.cache")
    mocker.patch("platforms.signals.cache")

    platform = Platform.objects.create(slug="platform1", name="P1")
    user = CustomUser.objects.create(
        username="u3", email="user@test.com", platform=platform,
    )

    Device.objects.create(
        user=user,
        platform=platform,
        name="d1",
        ip_address="1.1.1.1",
        is_active=True,
    )
    Device.objects.create(
        user=user,
        platform=platform,
        name="d2",
        ip_address="1.1.1.2",
        is_active=True,
    )
    Device.objects.create(
        user=user,
        platform=platform,
        name="d3",
        ip_address="1.1.1.3",
        is_active=False,
    )

    repo = DeviceRepository()

    # Execute
    count = repo.get_active_count_for_user(user, platform)

    # Verify
    assert count == 2
