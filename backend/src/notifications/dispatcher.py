import logging
from abc import ABC, abstractmethod

logger = logging.getLogger("django")


class BaseNotificationProvider(ABC):
    @abstractmethod
    def send(self, context: dict) -> None:
        pass


class MockEmailProvider(BaseNotificationProvider):
    def send(self, context: dict) -> None:
        logger.info(
            "[MOCK EMAIL] Sending notification with context: %s", context,
        )


class MockSMSProvider(BaseNotificationProvider):
    def send(self, context: dict) -> None:
        logger.info(
            "[MOCK SMS] Sending notification with context: %s", context,
        )


class MockSocketProvider(BaseNotificationProvider):
    def send(self, context: dict) -> None:
        logger.info(
            "[MOCK SOCKET] Sending notification with context: %s", context,
        )


class NotificationDispatcher:
    def __init__(self) -> None:
        self.providers = {
            "email": MockEmailProvider(),
            "sms": MockSMSProvider(),
            "socket": MockSocketProvider(),
        }

    def dispatch(self, channels: dict, context: dict) -> None:
        for channel, active in channels.items():
            if active and channel in self.providers:
                self.providers[channel].send(context)
