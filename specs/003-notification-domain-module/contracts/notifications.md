# Notification Module Contracts

## Internal Service Contract (NotificationService)

Services (Auth, Devices, etc.) will call the `NotificationService` to trigger notifications.

### `trigger_notification(user, notification_type, event_source, context)`

**Arguments**:
- `user`: `CustomUser` instance.
- `notification_type`: `str` (e.g., 'REGISTRATION').
- `event_source`: `str` (e.g., 'auth_service').
- `context`: `dict` containing dynamic data for the notification.

**Behavior**:
1. Creates a `Notification` record.
2. Resolves delivery channels via `RuleResolver`.
3. Enqueues a Celery task for asynchronous dispatch.

## API Contract (User Notifications)

### GET /notifications/
List notifications for the authenticated user.

**Success Response**: 200 OK
```json
{
  "results": [
    {
      "id": 123,
      "notification_type": "REGISTRATION",
      "template_context": {"welcome_name": "John"},
      "is_read": false,
      "created_at": "2026-04-25T14:00:00Z"
    }
  ]
}
```

### PATCH /notifications/{id}/
Mark a notification as read.

**Request**:
```json
{"is_read": true}
```
**Success Response**: 200 OK
