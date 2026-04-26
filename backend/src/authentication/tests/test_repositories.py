from typing import Any

import pytest
from platforms.models import Platform
from users.models import CustomUser
from users.repositories import UserRepository


@pytest.mark.django_db
def test_user_repository_find_by_email(mocker: Any) -> None:
    # Setup
    mocker.patch("django_redis.get_redis_connection")
    mocker.patch("platforms.rule_resolver.cache")
    platform = Platform.objects.create(slug="test-platform")
    user = CustomUser.objects.create(email="test@test.com", platform=platform)
    repo = UserRepository()

    # Execute
    found_user = repo.get_by_email_and_platform("test@test.com", platform)

    # Verify
    assert found_user == user
