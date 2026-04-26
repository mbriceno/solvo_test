# Tasks: Unit Testing Suite for Core Modules

## Implementation Strategy
- **Approach**: Incremental testing implementation, starting with foundation setup, followed by modular test suites for Authentication, Platforms, and Users.
- **Independence**: Each module's test suite (repository and service) is designed to be independently executable.
- **MVP**: Foundation + Authentication + Platforms test suites.

## Dependencies Graph
Setup (Phase 1) → Foundational (Phase 2) → US1 (Auth) → US2 (Platforms) → US3 (Users) → Polish

## Phase 1: Setup
- [X] T001 Install `pytest`, `pytest-django`, `pytest-mock` in `backend/requirements.txt`
- [X] T002 Create `pytest.ini` in the root directory to configure Django settings

## Phase 2: Foundational
- [X] T003 [P] Create `backend/src/authentication/tests/__init__.py`
- [X] T004 [P] Create `backend/src/platforms/tests/__init__.py`
- [X] T005 [P] Create `backend/src/users/tests/__init__.py`

## Phase 3: User Story 1 - Reliable Business Logic (Authentication)
- [X] T006 [US1] Create `backend/src/authentication/tests/test_services.py`
- [X] T007 [US1] Implement registration service tests in `backend/src/authentication/tests/test_services.py`
- [X] T008 [US1] Implement login service tests with JWT claims in `backend/src/authentication/tests/test_services.py`
- [X] T009 [US1] Create `backend/src/authentication/tests/test_repositories.py`

## Phase 4: User Story 2 - Robust Data Access (Platforms)
- [X] T010 [US2] Create `backend/src/platforms/tests/test_services.py`
- [X] T011 [US2] Implement RuleResolver tests (merging logic) in `backend/src/platforms/tests/test_services.py`
- [X] T012 [US2] Create `backend/src/platforms/tests/test_repositories.py`
- [X] T013 [US2] Implement Platform/GlobalConfig repository CRUD tests in `backend/src/platforms/tests/test_repositories.py`
## Phase 5: User Story 3 - Efficient and Isolated Tests (Users & Devices)
- [X] T014 [US3] Create `backend/src/users/tests/test_services.py`
- [X] T015 [US3] Implement DeviceService tests (max_devices validation) in `backend/src/users/tests/test_services.py`
- [X] T016 [US3] Create `backend/src/users/tests/test_repositories.py`
- [X] T017 [US3] Implement DeviceRepository tests (platform-scoped filtering) in `backend/src/users/tests/test_repositories.py`

## Phase 6: Polish & Cross-Cutting Concerns
- [X] T018 Run `pytest` and fix any issues
- [X] T019 Verify type annotations and 80-char line length in all test files
- [X] T020 Run `ruff check` on the `tests/` directories
