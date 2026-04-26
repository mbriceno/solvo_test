# Data Model: Unit Testing Suite for Core Modules

## Entities

### Test Fixture Models
These entities are used within the `pytest` framework to set up test scenarios.

- **UserFixture**: Represents a test user profile linked to a specific platform.
  - Fields: `username`, `email`, `platform_slug`.
- **PlatformFixture**: Represents the platform configuration and overrides.
  - Fields: `slug`, `defaults`, `overrides`.
- **DeviceFixture**: Represents a user's device.
  - Fields: `user_id`, `platform_slug`, `device_id`, `status` (active/inactive).

## Validation Rules
- **Device Count**: `max_devices` validation logic is retrieved from `Platform` configuration via `RuleResolver`.
- **Platform Scope**: Repositories MUST filter queries by `platform_slug` to ensure strict tenant isolation.
- **Mocking Strategy**: 
  - All Redis operations: Mocked with `unittest.mock` or `pytest-mock` to return predefined values (no network call).
  - Cross-module services: All `NotificationService` calls must be mocked to avoid triggering actual notifications during unit tests.
