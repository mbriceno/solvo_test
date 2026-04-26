from typing import Any

import pytest
from django.contrib.auth import get_user_model
from notifications.services import NotificationService
from platforms.models import Platform
from users.models import CustomUser
from users.services import UserService

from authentication.serializers import CustomTokenObtainPairSerializer
from authentication.services import AuthService

User = get_user_model()


@pytest.fixture
def auth_service(mocker: Any) -> AuthService:
    user_service = mocker.create_autospec(UserService)
    notification_service = mocker.create_autospec(NotificationService)
    return AuthService(user_service, notification_service)


@pytest.mark.django_db
def test_register_user_triggers_notification(
    auth_service: AuthService,
    mocker: Any,
) -> None:
    # Setup
    platform = mocker.create_autospec(Platform)
    mock_user = mocker.create_autospec(CustomUser)
    auth_service.user_service.create_user.return_value = mock_user

    # Execute
    auth_service.register_user("test@example.com", "password", platform)

    # Verify
    auth_service.notification_service.trigger_notification.assert_called_once()
    assert auth_service.notification_service.trigger_notification.call_args[1][
        "user"
    ] == mock_user


@pytest.mark.django_db
def test_jwt_contains_platform_slug(mocker: Any) -> None:
    # Setup
    mocker.patch("django_redis.get_redis_connection")
    mocker.patch("platforms.rule_resolver.cache")
    platform = Platform.objects.create(slug="test-platform")
    user = User.objects.create(email="test@test.com", platform=platform)

    # Execute
    token = CustomTokenObtainPairSerializer.get_token(user)

    # Verify
    assert token["platform_slug"] == "test-platform"
