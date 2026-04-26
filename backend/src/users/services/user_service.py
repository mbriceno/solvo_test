from platforms.models import Platform

from users.models import CustomUser
from users.repositories import UserRepository


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def create_user(
        self,
        email: str,
        password: str,
        platform: Platform,
        **extra_fields,
    ) -> CustomUser:
        user = CustomUser(
            email=email,
            platform=platform,
            username=f"{email}_{platform.slug}",
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user
