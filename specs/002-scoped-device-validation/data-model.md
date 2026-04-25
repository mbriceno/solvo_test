# Data Model: Scoped Devices

## Entities

### Device
Represents a user's device within a platform context.

| Field | Type | Description |
|-------|------|-------------|
| id | ID | Primary key |
| user | ForeignKey(CustomUser) | Owner of the device |
| platform | ForeignKey(Platform) | Platform context |
| name | String | Device name |
| ip_address | GenericIPAddress | Device IP |
| is_active | Boolean | Active status |
| last_seen | DateTime | Last activity |

## Relationships
- `Device` belongs to one `CustomUser`.
- `Device` belongs to one `Platform`.
- `CustomUser` has many `Device`s.
- `Platform` has many `Device`s.

## Validation Rules
- Retrieval MUST be filtered by BOTH `user_id` and `platform_id`.
- Index on `(user_id, platform_id)` is required for performance at scale.
