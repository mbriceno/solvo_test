# Feature Specification: Scoped Device Validation and Filtering

**Feature Branch**: `002-scoped-device-validation`  
**Created**: April 25, 2026  
**Status**: Draft  
**Input**: User description: "Scoped Device Validation and Filtering (Service-Repository Pattern) ## 1. Platform-Scoped Data Access * **Repository Implementation**: Update `DeviceRepository` in `src/users/repositories/`. * **Method**: Add `find_by_user_and_platform(user_id, platform_id)` to ensure all queries are strictly isolated to the current platform context. * **Filtering**: It must explicitly filter by both identifiers to prevent cross-platform data leakage for the same user email. ## 2. Business Logic & Validation (Service Layer) * **Service Implementation**: Update `DeviceService` in `src/users/services/`. * **Validation Flow**: 1. Retrieve the active user and platform SLUG from the request/token context. ## 3. JWT & Context Integration * **Token Claims**: Ensure the `auth` module adds `platform_id` or `platform_slug` to the JWT payload. * **Dependency Injection**: Pass the platform context from the View/Middleware into the Service to keep the Service layer "pure" and decoupled from the `request` object. ## 4. API Endpoints & Pagination * **GET /devices/**: Must use `DeviceRepository` to fetch only scoped results. * **Swagger Documentation**: Annotate the endpoints using `drf-spectacular` to describe that results are automatically filtered by the platform authenticated in the Bearer token. ## 5. Decisions.md Update * Justify the **Service-Repository** pattern for this specific validation. * Detail the strategy for handling 1 million users by optimizing the repository queries with proper indexing on `(user_id, platform_id)`."

## User Scenarios *(mandatory)*

### User Story 1 - Platform-Isolated Device Retrieval (Priority: P1)

As a user who uses the same email across multiple platforms (e.g., Mobile App and Web Dashboard), I want to see only the devices registered to the platform I am currently logged into, so that my data is organized and secure.

**Why this priority**: Core security requirement to prevent data leakage between platforms and ensure a clean user experience.

**Independent Test**: Log in to Platform A, retrieve devices; log in to Platform B with the same user, retrieve devices. Confirm sets are mutually exclusive and correct.

**Acceptance Scenarios**:

1. **Given** a user has 3 devices on Platform A and 2 devices on Platform B, **When** they request their devices using a Platform A token, **Then** they should receive exactly 3 devices.
2. **Given** a user has 3 devices on Platform A and 2 devices on Platform B, **When** they request their devices using a Platform B token, **Then** they should receive exactly 2 devices.

---

### User Story 2 - Secure Context Validation (Priority: P2)

As a system administrator, I want the system to enforce platform scoping at the data layer, so that even if a developer makes a mistake in the UI, the API will never return devices from the wrong platform context.

**Why this priority**: Ensures robust security and "defense in depth" by enforcing constraints at the Repository level.

**Independent Test**: Attempt to query devices by user ID alone without a platform ID in the repository layer and ensure the method signature or implementation prevents it.

**Acceptance Scenarios**:

1. **Given** an authenticated request, **When** the system resolves the platform from the token, **Then** that platform identity must be passed all the way to the database query.
2. **Given** a token with a missing or invalid platform claim, **When** a device retrieval is attempted, **Then** the request should be rejected as unauthorized.

---

### Edge Cases

- **User has no devices on the current platform**: System should return an empty list, not an error or devices from another platform.
- **Platform slug in token does not match any existing platform record**: System should return an empty list or an authentication error (depending on whether the platform is validated at the middleware level).
- **Same device hardware registered on multiple platforms**: The system must distinguish between these instances based on the platform association.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST extract `platform_id` or `platform_slug` from the authentication token claims during request authentication.
- **FR-002**: System MUST implement a scoped retrieval method in the data access layer to ensure all queries are strictly isolated by both user and platform.
- **FR-003**: System MUST pass the platform identity from the API/Middleware layer to the business logic layer using dependency injection or method arguments, keeping the business logic independent of the web request object.
- **FR-004**: The device listing endpoint MUST utilize the scoped data access method to fetch results.
- **FR-005**: API documentation MUST clearly state that results are automatically filtered by the platform context found in the authentication token.
- **FR-006**: The database schema MUST support efficient querying on the combination of user and platform identifiers.

### Key Entities *(include if feature involves data)*

- **Device**: Represents a physical or virtual device registered to a user within a specific platform context.
- **Platform**: Represents a distinct application environment.
- **User**: The owner of the devices, whose identity is shared across platforms but whose data is scoped by them.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of device listing requests are correctly filtered by the platform context provided in the authentication token.
- **SC-002**: Query performance for device retrieval remains under 100ms even when the user table exceeds 1 million records.
- **SC-003**: Zero instances of cross-platform data leakage during security validation tests.

## Assumptions

- **Authentication Tokens**: It is assumed the authentication system supports custom claims for platform identity.
- **Statelessness**: The business logic layer is designed to be stateless with respect to the HTTP request.
- **Database Indexing**: The underlying database supports composite indexing.
- **Single Platform per Token**: Each authentication token is associated with exactly one platform context.
