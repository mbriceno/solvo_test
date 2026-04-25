# Research: Multi-Platform Device Management API

## Rule Resolver with Redis Caching

**Decision**: Implement a `RuleResolver` service that fetches `GlobalConfig` defaults and merges them with `Platform.rule_overrides`.
**Rationale**: Centralizes configuration logic and ensures overrides take precedence.
**Redis Integration**: Cache the resolved configuration for each `(platform_slug)` to ensure low-latency lookups during device registration.
**Alternatives Considered**: Fetching from DB on every request (rejected due to latency goals).

## Custom JWT Scoping

**Decision**: Customize `SimpleJWT` token generation to include `platform_slug` in the payload.
**Rationale**: Enables the backend to identify the platform context directly from the token, facilitating the scoped user model and rule resolution.
**Implementation**: Override `TokenObtainPairSerializer.get_token` to add the custom claim.

## Custom User Model with Multi-tenant Identity

**Decision**: Use `AbstractUser` with a unique constraint on `(email, platform)`.
**Rationale**: Satisfies the requirement for independent accounts with the same email across different platforms.
**Scalability**: Standard B-tree indexes on `(email, platform)` support efficient lookups even at 1M users.

## Event-Driven Dispatcher (LogProvider)

**Decision**: Implement a signal-based dispatcher (Django signals) that invokes an extensible `NotificationHandler`.
**Rationale**: Decouples business logic from notification delivery. Initially uses a `LogProvider` for simplicity.
**Celery Readiness**: Designed to transition to Celery by replacing the synchronous handler with a task delay call.
