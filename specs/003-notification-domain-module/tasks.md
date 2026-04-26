# Tasks: Isolated Notification Domain Module

**Feature**: Isolated Notification Domain Module
**Plan**: [specs/003-notification-domain-module/plan.md](plan.md)
**Status**: Draft

## Implementation Strategy

We implement a standalone `notifications` app to decouple business events from delivery channels. The strategy follows an asynchronous pattern using Celery and a Strategy-based dispatcher. We will first establish the persistence layer, followed by the delivery infrastructure, and finally integrate with the `authentication` service to trigger notifications on user registration.

- **MVP Scope**: User Story 1 (Multi-Channel Notification Dispatch)
- **Incremental Delivery**: User Story 1 provides the core infrastructure and first integration point. User Story 2 adds user-facing visibility and management.

## Dependencies

- **US1** depends on **Phase 2 (Foundational)**
- **US2** depends on **US1** (requires persistence and records to manage)

## Phase 1: Setup

- [ ] T001 Register `notifications` app in `backend/src/core/settings.py`
- [ ] T002 Create `notifications` app directory and `__init__.py` files in `backend/src/notifications/`
- [ ] T003 Create `notifications/apps.py` with standard Django app configuration

## Phase 2: Foundational (Blocking)

- [ ] T004 Create `Notification` model with channels flags and dynamic context in `backend/src/notifications/models.py`
- [ ] T005 Create `NotificationRepository` with `create` and `get_for_user` methods in `backend/src/notifications/repositories.py`

## Phase 3: User Story 1 - Multi-Channel Notification Dispatch (P1)

**Goal**: System triggers notifications via platform-configured channels asynchronously.
**Independent Test**: Trigger a registration event; verify record created with correct flags and Celery task enqueued.

- [ ] T006 [P] [US1] Implement `NotificationDispatcher` with Strategy pattern and Mock providers in `backend/src/notifications/dispatcher.py`
- [ ] T007 [P] [US1] Create `dispatch_notification` Celery task in `backend/src/notifications/tasks.py`
- [ ] T008 [US1] Implement `NotificationService.trigger_notification` in `backend/src/notifications/services.py` (includes RuleResolver check)
- [ ] T009 [US1] Create `AuthService` in `backend/src/authentication/services.py` to handle registration and notification trigger
- [ ] T010 [US1] Refactor `RegisterSerializer.create` in `backend/src/authentication/serializers.py` to delegate to `AuthService`

## Phase 4: User Story 2 - User Notification Management (P2)

**Goal**: Users can list their notifications and mark them as read.
**Independent Test**: GET `/notifications/` returns user's messages; PATCH `/notifications/{id}/` updates `is_read`.

- [ ] T011 [P] [US2] Create `NotificationSerializer` in `backend/src/notifications/serializers.py`
- [ ] T012 [US2] Implement `NotificationViewSet` with list and partial_update (mark as read) in `backend/src/notifications/views.py`
- [ ] T013 [US2] Configure `notifications` URLs in `backend/src/notifications/urls.py` and register in `backend/src/core/urls.py`

## Phase 5: Polish & Cross-Cutting Concerns

- [ ] T014 Add `drf-spectacular` annotations to notification endpoints for Swagger documentation
- [ ] T015 Update `DECISIONS.md` with justification for standalone notification architecture and Service-Repository isolation
- [ ] T016 Final manual sweep of all `notifications` module files for PEP8/Ruff compliance and 80-character line length

## Parallel Execution Examples

- **US1 Persistence**: T004 (Model) and T005 (Repository) can be developed once Phase 1 is done.
- **US1 Delivery**: T006 (Dispatcher) and T007 (Tasks) can be developed in parallel as they deal with different delivery concerns.
- **US2 API**: T011 (Serializer) and T012 (ViewSet) can be prepared while US1 integration (T009/T010) is being finalized.
