# Feature Specification: Unit Testing Suite for Core Modules

**Feature Branch**: `004-unit-testing-suite`  
**Created**: 2026-04-26  
**Status**: Draft  
**Input**: User description: "Unit Testing Suite for Core Modules: pytest, pytest-django, PEP8, Ruff, 80-char line length, type annotations, structure (tests/ in authentication, platforms, users), repositories and services. Auth: registration platform_slug, login JWT platform_slug, mock NotificationService. Platforms: Rule Resolver merging, Redis caching (mocked), Repository CRUD. Users: Device Repository queries, Device Service validation (max_devices). Mocking Redis and cross-module calls. In-memory DB for repos. DECISIONS.md justification."

## User Scenarios *(mandatory)*

### User Story 1 - Reliable Business Logic (Priority: P1)

As a developer, I want to verify that the core business logic (services) in Authentication, Platforms, and Users modules behaves correctly under various conditions so that I can confidently modify code without introducing regressions.

**Why this priority**: Business logic is the heart of the application. Ensuring its correctness is critical for stability and reliability.

**Independent Test**: Each service method can be tested in isolation by providing specific inputs and asserting expected outputs or side effects (like repository calls).

**Acceptance Scenarios**:

1. **Given** a new user registration request, **When** the registration service is called with a `platform_slug`, **Then** the user is created and correctly linked to that platform.
2. **Given** a user login, **When** the login logic generates a JWT, **Then** the `platform_slug` is included in the token claims.
3. **Given** a device registration request, **When** the user has already reached the `max_devices` limit, **Then** a `ValidationError` is raised and the device is not registered.

---

### User Story 2 - Robust Data Access (Priority: P2)

As a developer, I want to ensure that repository methods correctly interact with the database and return accurate data based on the provided context (e.g., user and platform) so that data integrity is maintained.

**Why this priority**: Repositories handle the persistence layer. Bugs here can lead to data leaks between platforms or incorrect counts.

**Independent Test**: Repository tests can run against an in-memory database to verify SQL/ORM logic independently of external database state.

**Acceptance Scenarios**:

1. **Given** devices belonging to different users and platforms, **When** searching for devices by a specific user and platform, **Then** only the matching devices are returned.
2. **Given** various active and inactive devices, **When** counting active devices for a user, **Then** the count accurately reflects the state.
3. **Given** Platform and GlobalConfig entities, **When** performing CRUD operations, **Then** the data is correctly persisted and retrieved.

---

### User Story 3 - Efficient and Isolated Tests (Priority: P3)

As a developer, I want my tests to be fast and isolated from external dependencies (like Redis or other modules) so that the test suite provides immediate feedback and doesn't fail due to environmental issues.

**Why this priority**: Test speed and reliability directly impact developer productivity. Isolation prevents cascading failures.

**Independent Test**: Verify that running tests does not require a running Redis instance or an active network connection to external services.

**Acceptance Scenarios**:

1. **Given** a service that uses Redis for caching, **When** the service is tested, **Then** all Redis calls are intercepted by mocks, allowing verification of cache hits and misses without an actual Redis server.
2. **Given** the Authentication service which notifies users, **When** registration is tested, **Then** the Notification Service is mocked, ensuring tests stay within the Authentication domain.

---

### Edge Cases

- **Max Devices Boundary**: Testing the exact limit (e.g., if limit is 5, test 4->5 succeeds, 5->6 fails).
- **Missing Platform Overrides**: Ensuring the Rule Resolver correctly falls back to `GlobalConfig` when a platform-specific override is missing.
- **Empty Query Results**: Ensuring repositories handle cases where no devices are found for a user/platform combination without errors.
- **Malformed JWT Claims**: Ensuring the login logic handles edge cases in claim generation if platform data is incomplete.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide unit tests for `authentication`, `platforms`, and `users` modules.
- **FR-002**: Tests MUST be organized into `tests/` directories within each module, containing `test_repositories.py` and `test_services.py`.
- **FR-003**: Service tests MUST mock all cross-module dependencies (e.g., `authentication` mocks `notifications`).
- **FR-004**: Platforms Rule Resolver tests MUST verify merging of `GlobalConfig` and `Platform` settings.
- **FR-005**: All Redis interactions MUST be mocked in unit tests to ensure isolation and speed.
- **FR-006**: Repository tests MUST use an in-memory database for execution.
- **FR-007**: Device Service MUST validate `max_devices` and raise `ValidationError` when the limit is exceeded.
- **FR-008**: All test code MUST follow PEP8 and Ruff standards with a strict 80-character line length.
- **FR-009**: All test functions and fixtures MUST include full Python type annotations.

### Key Entities *(include if feature involves data)*

- **Test Suite**: The collection of automated tests using `pytest`.
- **Mock Objects**: Simulated components used to isolate the code under test from external dependencies (Redis, NotificationService).
- **Service Layer**: The business logic layer of each module being tested.
- **Repository Layer**: The data access layer of each module being tested.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the specified test cases (Registration, Login, Rule Merging, Device Validation, etc.) pass in the test environment.
- **SC-002**: The entire unit test suite for these three modules executes in under 10 seconds on standard development hardware.
- **SC-003**: Code coverage for the service and repository layers in the `authentication`, `platforms`, and `users` modules reaches at least 90%.
- **SC-004**: 100% adherence to the 80-character line length and type annotation requirements, as verified by Ruff and Mypy.

## Assumptions

- **Existing Infrastructure**: The project already has a `pytest` configuration or expects one to be initialized.
- **Module Boundaries**: The current module structure (`authentication`, `platforms`, `users`) is stable and follow the repository/service pattern.
- **Tooling Availability**: `pytest`, `pytest-django`, and `ruff` are available or can be added to the project dependencies.
- **Mocking Library**: `unittest.mock` or `pytest-mock` will be used for isolation.
