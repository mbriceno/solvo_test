# Tasks: Scoped Device Validation and Filtering

**Feature**: Scoped Device Validation and Filtering
**Plan**: [specs/002-scoped-device-validation/plan.md](plan.md)
**Status**: Completed

## Implementation Strategy

We follow a Service-Repository pattern to ensure strict data isolation. Implementation begins with foundational data layer updates (indexing and scoped repository methods), followed by service-level logic, and finally API integration with contextual extraction from JWT tokens.

- **MVP Scope**: User Story 1 (Platform-Isolated Device Retrieval)
- **Incremental Delivery**: Each user story phase results in a complete, independently testable (manually) increment.

## Dependencies

- **US1** depends on **Phase 2 (Foundational)**
- **US2** depends on **US1**

## Phase 1: Setup

- [x] T001 Verify project structure and basic dependencies in `backend/requirements.txt`

## Phase 2: Foundational (Blocking)

- [x] T002 Update `Device` model in `backend/src/users/models.py` to add composite index on `(user, platform)`
- [x] T003 Implement `find_by_user_and_platform` in `backend/src/users/repositories.py` with full type annotations

## Phase 3: User Story 1 - Platform-Isolated Device Retrieval (P1)

**Goal**: Users see only devices for their current platform.
**Independent Test**: Authenticate as same user on two platforms; verify `GET /devices/` returns mutually exclusive sets.

- [x] T004 [P] [US1] Implement `get_devices_for_user_on_platform` in `backend/src/users/services.py` with 80-char limit
- [x] T005 [US1] Update `get_queryset` in `backend/src/users/views.py` to use service-level scoped filtering

## Phase 4: User Story 2 - Secure Context Validation (P2)

**Goal**: Enforce platform scoping at the data layer via explicit context passing.
**Independent Test**: Verify service methods fail or reject requests if platform context is missing or mismatched.

- [x] T006 [P] [US2] Update `DeviceService.register_device` in `backend/src/users/services.py` to use explicit platform context
- [x] T007 [US2] Inject platform context into `DeviceService` calls in `backend/src/users/views.py` derived from authentication token

## Phase 5: Polish & Cross-Cutting Concerns

- [x] T008 Add `drf-spectacular` annotations to `DeviceViewSet` in `backend/src/users/views.py` describing scoped filtering
- [x] T009 Update `DECISIONS.md` in project root with Service-Repository pattern justification and indexing strategy
- [x] T010 Final manual sweep of all modified files for PEP8/Ruff compliance and 80-character line length

## Parallel Execution Examples

- **US1**: T004 (Service) can be developed in parallel with UI/Frontend preparation (if applicable), though T005 (View) depends on it.
- **US2**: T006 (Service update) can be done in parallel with T004 if the interface is stable.
