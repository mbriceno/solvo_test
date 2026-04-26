from typing import Any

import pytest
from platforms.models import Platform
from platforms.rule_resolver import RuleResolver
from rest_framework.exceptions import PermissionDenied

from users.models import CustomUser, Device
from users.repositories import DeviceRepository
from users.services import DeviceService


@pytest.fixture
def device_service(mocker: Any) -> DeviceService:
    mock_rule_resolver_instance = mocker.create_autospec(RuleResolver)
    mock_rule_resolver_instance.resolve.return_value = {"max_devices": 5}
    mock_device_repository = mocker.create_autospec(DeviceRepository)
    return DeviceService(
        rule_resolver=mock_rule_resolver_instance,
        repository=mock_device_repository,
    )


@pytest.mark.django_db
def test_device_service_max_devices_validation_exceeded(
    device_service: DeviceService, mocker: Any,
) -> None:
    # Setup - mock the cache globally via patch
    mocker.patch("django.core.cache.cache.delete_pattern")

    platform = Platform.objects.create(slug="test-platform")
    user = CustomUser.objects.create(email="user@test.com", platform=platform)

    device_service.rule_resolver.resolve.return_value = 2

    mock_existing_devices = [
        mocker.MagicMock(spec=Device, user=user, platform=platform),
        mocker.MagicMock(spec=Device, user=user, platform=platform),
    ]
    device_service.repository.get_active_count_for_user.return_value = len(
        mock_existing_devices,
    )

    with pytest.raises(PermissionDenied) as excinfo:
        device_service.register_device(user, platform, "new_device", "1.1.1.3")

    assert "Device limit reached for this platform." in str(excinfo.value)
    device_service.repository.model.objects.create.assert_not_called()


@pytest.mark.django_db
def test_device_service_max_devices_validation_allowed(
    device_service: DeviceService, mocker: Any,
) -> None:
    # Setup - mock the cache globally via patch
    mocker.patch("django.core.cache.cache.delete_pattern")

    platform = Platform.objects.create(slug="test-platform")
    user = CustomUser.objects.create(email="user@test.com", platform=platform)

    device_service.rule_resolver.resolve.return_value = 5
    device_service.repository.get_active_count_for_user.return_value = 0

    mock_new_device = mocker.MagicMock(spec=Device)
    device_service.repository.model.objects.create.return_value = (
        mock_new_device
    )

    device = device_service.register_device(
        user, platform, "new_device", "1.1.1.3",
    )

    assert device == mock_new_device
    device_service.repository.model.objects.create.assert_called_once()
