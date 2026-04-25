# Research: Scoped Device Logic

## Decision: Contextual Platform Extraction
- **Decision**: Implement a mechanism to extract `platform_slug` from the JWT token and inject it into the Service layer.
- **Rationale**: Ensures the business logic remains "pure" and decoupled from the `request` object while maintaining strict platform isolation.
- **Alternatives considered**: Directly accessing `request.user.platform` in the View, but this violates the goal of passing the context explicitly to the Service.

## Decision: Scoped Repository Method
- **Decision**: Add `list_by_platform(user_id, platform_id)` to `DeviceRepository`.
- **Rationale**: Mandated by the specification to ensure queries are strictly isolated at the data access layer.
- **Alternatives considered**: Filtering in the Service layer, but Repository-level filtering is more efficient and secure.

## Decision: Service Layer Validation
- **Decision**: Update `DeviceService` to handle filtered retrieval and validation.
- **Rationale**: Consolidates business logic in the Service layer as per the Service-Repository pattern.

## Decision: Formatting & Typing
- **Decision**: Enforce strict 80-character line length and comprehensive Python Type Annotations.
- **Rationale**: Required for high code quality and consistency with project standards (PEP8/Ruff).

## Technical Findings
- `CustomTokenObtainPairSerializer` already injects `platform_slug` into the JWT.
- `Device` model already has `user` and `platform` foreign keys.
- `DeviceRepository` inherits from `BaseRepository` and needs the new method.
- `DeviceViewSet` currently filters only by `user`, needs to filter by `platform` as well.
