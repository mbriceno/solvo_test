# Feature Specification: Isolated Notification Domain Module

**Feature Branch**: `003-notification-domain-module`  
**Created**: April 25, 2026  
**Status**: Draft  
**Input**: User description: "Isolated Notification Domain Module ## 1. Domain Module: `notifications` * **Architecture**: Create a standalone Django app in `src/notifications/`. * **Notification Model**: Implement with strict **Type Annotations** and 80-char limits: * `user`: ForeignKey to the user model (identity of the recipient). * `notification_type`: CharField (e.g., 'REGISTRATION', 'SYSTEM_ALERT'). * `event_source`: CharField (e.g., 'auth_service', 'device_service'). * `template_context`: JSONField for dynamic metadata. * `is_read`: BooleanField (default=False). * **Channels**: `send_email`, `send_sms`, `send_socket` (BooleanFields). * **Audit**: `created_at` (DateTime), `sent_at` (DateTime, nullable). ## 2. Service-Repository Pattern * **NotificationRepository**: Handles persistence and retrieval within `src/notifications/repositories/`. * **NotificationService**: * Orchestrates the creation of notification records. * Uses the `RuleResolver` from the `platforms` module to decide which channels (Email/SMS/Socket) should be active based on platform business rules. * All parameters and return types must be explicitly annotated. ## 3. Extensible Dispatcher (The "Strategy" Pattern) * **Logic**: Implement a dispatcher that checks the boolean flags and routes the `template_context` to specific provider handlers (Log, Mock Email, etc.). * **Implementation**: Create a `dispatch_notification` task (prepared for Celery) that reads the boolean flags (`send_email`, etc.) and routes the `template_context` to the appropriate "Mock" provider. * **Scalability**: The design must allow the addition of new providers (e.g., Push) without modifying the `auth` or `users` apps. ## 4. Documentation (DECISIONS.md) * Justify the creation of a standalone `notifications` module for microservice readiness. * Explain the use of the **Service-Repository** pattern to isolate delivery logic from business triggers."

## User Scenarios *(mandatory)*

### User Story 1 - Multi-Channel Notification Dispatch (Priority: P1)

As a system service (e.g., Auth or Device service), I want to trigger a notification for a user without worrying about the delivery details, so that the user receives the message via the channels configured for their platform.

**Why this priority**: Core value of the feature; decoupling notification triggers from delivery logic.

**Independent Test**: Trigger a 'REGISTRATION' event from the Auth service; verify that a notification record is created and that "Mock" delivery tasks are enqueued for the correct channels (Email/SMS/Socket) based on platform rules.

**Acceptance Scenarios**:

1. **Given** a platform has 'Email' enabled for 'REGISTRATION', **When** a registration notification is triggered, **Then** a notification record should be saved with `send_email=True` and an email dispatch task should be enqueued.
2. **Given** a platform has all channels disabled, **When** a notification is triggered, **Then** a record should be saved but no dispatch tasks should be enqueued.

---

### User Story 2 - User Notification Management (Priority: P2)

As a user, I want to see which notifications I have received and mark them as read, so that I can keep track of system alerts and updates.

**Why this priority**: Essential for user engagement and notification lifecycle management.

**Independent Test**: Retrieve notifications for a user; verify the `is_read` status can be toggled.

**Acceptance Scenarios**:

1. **Given** a user has unread notifications, **When** they request their notification list, **Then** they should see the metadata provided by the triggering service.
2. **Given** a specific notification, **When** the user marks it as read, **Then** the `is_read` status should be updated to `True`.

---

### Edge Cases

- **Platform rules missing for a channel**: The system should default to not sending if the rule cannot be resolved.
- **Triggering service provides invalid metadata**: The system should safely store the JSON metadata even if it's unstructured, ensuring the dispatch doesn't crash.
- **Recipient user does not exist**: The system should log an error and skip the notification creation.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide an isolated notification module that manages the persistence and dispatch lifecycle independently of other domains.
- **FR-002**: System MUST use platform-specific business rules to dynamically determine which delivery channels (Email, SMS, Socket) are active for a given notification type.
- **FR-003**: System MUST support asynchronous dispatching of notifications via a task queue to ensure non-blocking delivery.
- **FR-004**: System MUST store a dynamic context for each notification to allow for variable template data depending on the event source.
- **FR-005**: System MUST implement a dispatcher using the Strategy pattern to allow for new delivery providers (e.g., Push, Webhook) to be added without modifying core business logic.
- **FR-006**: System MUST track the audit trail for notifications, including creation time and successful dispatch time.

### Key Entities *(include if feature involves data)*

- **Notification**: The central record representing a message intended for a user. Contains recipient identity, type, source, dynamic metadata, and delivery channel flags.
- **Delivery Provider**: A modular handler responsible for the technical delivery of a message to a specific channel (e.g., "Mock Email Provider").

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of notification triggers result in correctly scoped database records and corresponding dispatch tasks.
- **SC-002**: New delivery channels can be added to the dispatcher with zero modifications to the existing `auth` or `users` modules.
- **SC-003**: Notification dispatching (from trigger to task enqueue) completes in under 50ms to maintain API responsiveness.

## Assumptions

- **Mock Providers**: Initial implementation will use mock providers that log the delivery instead of integrating with real external APIs (SendGrid, Twilio, etc.).
- **User Identity**: All notifications are tied to a `CustomUser` identity which exists across the system.
- **Platform Rules**: The `RuleResolver` from the `platforms` module is already capable of returning boolean flags for notification channels.
