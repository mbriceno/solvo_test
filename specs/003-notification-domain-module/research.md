# Research: Isolated Notification Domain Module

## Decision: Notification App Structure
- **Decision**: Create a standalone Django app `notifications` in `backend/src/notifications/`.
- **Rationale**: Ensures domain isolation and microservice readiness. Delivery logic is decoupled from business triggers.
- **Alternatives considered**: Adding notifications to `users` app, but that would violate the Single Responsibility Principle as notifications grow.

## Decision: Channel Resolution via RuleResolver
- **Decision**: `NotificationService` will interact with `platforms.rule_resolver.RuleResolver` to fetch platform-specific channel settings (e.g., `send_email`, `send_sms`).
- **Rationale**: Centralizes business rule management in the `platforms` module while allowing dynamic behavior.

## Decision: Strategy Pattern for Delivery
- **Decision**: Implement a `NotificationDispatcher` that uses a strategy pattern to route messages to different providers.
- **Rationale**: Enables adding new providers (e.g., Push, Slack) without modifying core notification logic. Initial providers will be "Mock" versions that log output.

## Decision: Asynchronous Processing
- **Decision**: Use Celery tasks for the actual dispatching.
- **Rationale**: Per Constitution Principle VI, notifications should be asynchronous to keep the request-response cycle performant.

## Decision: Authentication Service Integration
- **Decision**: Create/Update `backend/src/authentication/services.py` to orchestrate user registration and trigger the `NotificationService`.
- **Rationale**: Moves business logic out of serializers and into a dedicated service layer, adhering to Clean Architecture.

## Technical Findings
- `RuleResolver` is already implemented in `platforms` and supports JSON-based overrides.
- Celery is already configured in `core/celery.py`.
- `CustomUser` model is the primary recipient identity.
