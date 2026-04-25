import logging

logger = logging.getLogger(__name__)


class BaseNotificationHandler:
    def handle(self, event_name, **kwargs):
        raise NotImplementedError


class LogProvider(BaseNotificationHandler):
    def handle(self, event_name, **kwargs):
        logger.info("Notification Event: %s | Data: %s", event_name, kwargs)


def dispatch_notification(event_name, **kwargs):
    # In a more complex setup, we could load handlers from settings
    handler = LogProvider()
    handler.handle(event_name, **kwargs)
