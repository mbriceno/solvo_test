# Quickstart: Notifications Module

## Triggering a Notification (Internal)
```python
from notifications.services import NotificationService
from notifications.repositories import NotificationRepository

# Trigger a registration notification
service = NotificationService(NotificationRepository())
service.trigger_notification(
    user=new_user,
    notification_type='REGISTRATION',
    event_source='auth_service',
    context={'email': new_user.email}
)
```

## Consuming Notifications (External)
1. **GET /notifications/**: Fetch the user's notification list.
2. **PATCH /notifications/{id}/**: Mark a notification as read.

## Implementation Details
- **App**: `backend/src/notifications/`
- **Dispatcher**: `backend/src/notifications/dispatcher.py` (Strategy pattern)
- **Task**: `backend/src/notifications/tasks.py` (Celery)
