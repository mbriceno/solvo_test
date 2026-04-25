# Data Model: Multi-Platform Device Management API

## Entities

### GlobalConfig
- `rule_name`: String (Unique) - e.g., "max_devices"
- `default_value`: JSON - Default value for the rule

### Platform
- `name`: String
- `slug`: String (Unique) - e.g., "alpha"
- `rule_overrides`: JSONField - Platform-specific values (e.g., `{"max_devices": 10}`)

### CustomUser (AbstractUser)
- `email`: Email
- `platform`: ForeignKey(Platform)
- `UniqueConstraint`: `(email, platform)`

### Device
- `user`: ForeignKey(CustomUser)
- `platform`: ForeignKey(Platform)
- `name`: String
- `ip_address`: GenericIPAddressField
- `is_active`: Boolean (Default: True)
- `last_seen`: DateTime (Auto_now)

## Validation Rules

- **Device Registration**:
  - Fetch `max_devices` from `RuleResolver`.
  - Count active devices for `(user, platform)`.
  - Reject if `count >= max_devices`.

## Relationships
- `Platform` is the root tenant.
- `User` and `Device` are strictly scoped to a `Platform`.
