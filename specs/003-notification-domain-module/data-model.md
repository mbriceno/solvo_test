# Data Model: Notifications

## Entities

### Notification
Represents a message sent to a user.

| Field | Type | Description |
|-------|------|-------------|
| id | ID | Primary key |
| user | ForeignKey(CustomUser) | Recipient |
| notification_type | String | e.g., 'REGISTRATION' |
| event_source | String | e.g., 'auth_service' |
| template_context | JSON | Metadata for template rendering |
| is_read | Boolean | Read status |
| send_email | Boolean | Whether to send via Email |
| send_sms | Boolean | Whether to send via SMS |
| send_socket | Boolean | Whether to send via WebSocket |
| created_at | DateTime | Audit: Creation time |
| sent_at | DateTime | Audit: Delivery time (nullable) |

## Relationships
- `Notification` belongs to one `CustomUser`.
- `Notification` is triggered by an external event source.

## Validation Rules
- `notification_type` must be one of the supported types.
- `template_context` must be valid JSON.
- `user` must exist.
