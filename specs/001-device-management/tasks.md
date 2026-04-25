# Tasks: Multi-Platform Device Management API

**Input**: Design documents from `/specs/001-device-management/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Per Constitution Principle II, testing tasks are OMITTED in this development phase. Do not generate tasks for unit, integration, or contract tests unless specifically overridden.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`
- Paths shown below assume `backend/src/` as the base directory for source code

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure: `backend/src/{auth,users,platforms,core}`, `backend/manage.py`, `Dockerfile`, `docker-compose.yml`, `requirements.txt`
- [X] T002 [P] Initialize Django project and apps: `auth`, `users`, `platforms`
- [X] T003 [P] Configure Docker Compose with Python 3.x, SQLite, and Redis services
- [X] T004 [P] Configure linting and formatting with Ruff in `.ruff.toml`
- [X] T005 [P] Install primary dependencies: `django`, `djangorestframework`, `djangorestframework-simplejwt`, `redis`, `drf-spectacular`, `celery` in `requirements.txt`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure and base models that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Implement shared base classes (Repository, Service, Selector) in `backend/src/core/base.py`
- [X] T007 [P] Create `Platform` and `GlobalConfig` models in `backend/src/platforms/models.py`
- [X] T008 [P] Implement `CustomUser` model with `(email, platform)` unique constraint in `backend/src/users/models.py`
- [X] T009 Configure `settings.py` for `AUTH_USER_MODEL`, `REST_FRAMEWORK` (SimpleJWT, drf-spectacular), `CELERY`, and `CACHES` (Redis) in `backend/src/core/settings.py`
- [X] T010 [P] Initialize Celery application and configuration in `backend/src/core/celery.py`
- [X] T011 [P] Setup basic API routing structure in `backend/src/core/urls.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Multi-Platform Account Creation (Priority: P1) 🎯 MVP

**Goal**: Enable users to create independent accounts using the same email on different platforms with platform-scoped JWT authentication.

**Independent Test**: Register the same email address on two different platforms and verify two distinct user records exist. Authenticate with each and verify the `platform_slug` claim in the JWT.

### Implementation for User Story 1

- [X] T012 [P] [US1] Create `PlatformRepository` and `PlatformService` in `backend/src/platforms/repositories.py` and `backend/src/platforms/services.py`
- [X] T013 [P] [US1] Create `UserRepository` and `UserService` in `backend/src/users/repositories.py` and `backend/src/users/services.py`
- [X] T014 [US1] Implement `CustomTokenObtainPairSerializer` to include `platform_slug` claim in `backend/src/auth/serializers.py`
- [X] T015 [US1] Implement Register, Login, Refresh, and Logout views in `backend/src/auth/views.py`
- [X] T016 [US1] Configure SimpleJWT blacklisting for Logout in `backend/src/core/settings.py`
- [X] T017 [US1] Implement event-driven signal for platform registration in `backend/src/users/signals.py`
- [X] T018 [US1] Implement `LogProvider` notification handler in `backend/src/core/notifications.py`

**Checkpoint**: At this point, User Story 1 is fully functional and testable independently

---

## Phase 4: User Story 2 - Device Registration with Rule Validation (Priority: P2)

**Goal**: Allow users to register devices subject to dynamic `max_devices` rule validation cached in Redis.

**Independent Test**: Configure `max_devices` for a platform, register devices up to the limit, and verify the next registration attempt is rejected with a 403.

### Implementation for User Story 2

- [X] T019 [P] [US2] Create `Device` model in `backend/src/users/models.py`
- [X] T020 [P] [US2] Implement `RuleResolver` service with Redis caching logic in `backend/src/platforms/rule_resolver.py`
- [X] T021 [P] [US2] Create `DeviceRepository` and `DeviceService` in `backend/src/users/repositories.py` and `backend/src/users/services.py`
- [X] T022 [US2] Implement `DeviceViewSet` with registration logic (POST) in `backend/src/users/views.py`
- [X] T023 [US2] Integrate `RuleResolver` into `DeviceService` for `max_devices` validation

**Checkpoint**: At this point, User Stories 1 AND 2 work independently

---

## Phase 5: User Story 3 - List Managed Devices with Pagination (Priority: P3)

**Goal**: Provide a paginated list of registered devices with required metadata.

**Independent Test**: Register 15 devices, request the list with a page size of 10, and verify the metadata (`count`, `total_pages`, `next`, `previous`) and results.

### Implementation for User Story 3

- [X] T024 [P] [US3] Implement custom pagination class with mandatory metadata in `backend/src/core/pagination.py`
- [X] T025 [US3] Implement paginated list action (GET) in `DeviceViewSet` in `backend/src/users/views.py`
- [X] T026 [US3] Add `drf-spectacular` schema annotations (summaries, descriptions, tags) to all views in `backend/src/{auth,users,platforms}/views.py`

**Checkpoint**: All user stories are now independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T027 [P] Perform final Ruff compliance check and resolve issues across all modules
- [X] T028 Create `DECISIONS.md` documenting architecture, multi-tenant identity, and caching strategy in the project root
- [X] T029 [P] Finalize API documentation configuration and verify Swagger UI accessibility

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User Story 1 (Auth) should be completed first to enable authentication for other stories
  - User Stories 2 and 3 can proceed in parallel once Story 1 is ready

### User Story Dependencies

- **User Story 1 (P1)**: Foundation ready
- **User Story 2 (P2)**: Depends on User Story 1 (User identity and Platform context)
- **User Story 3 (P3)**: Depends on User Story 2 (Devices must exist to be listed)

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- T002, T003, T004, T005 in Setup can run in parallel
- T007, T008, T010, T011 in Foundational can run in parallel
- Once User Story 1 reaches a stable model/service state, work on Story 2 models can begin

---

## Parallel Example: User Story 1

```bash
# Launch repositories and services for User Story 1 together:
Task: "Create PlatformRepository and PlatformService in backend/src/platforms/repositories.py and backend/src/platforms/services.py"
Task: "Create UserRepository and UserService in backend/src/users/repositories.py and backend/src/users/services.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Auth and Identity)
4. **STOP and VALIDATE**: Test account isolation across platforms
5. Proceed once MVP identity logic is verified

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Identity MVP ready
3. Add User Story 2 → Test independently → Device Registration ready
4. Add User Story 3 → Test independently → Full Device Management ready
5. Each story adds value without breaking previous stories

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Verify functionality manually as automated tests are omitted per Constitution Principle II
- Commit after each task or logical group
