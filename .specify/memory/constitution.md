<!--
Sync Impact Report:
- Version change: 1.1.0 → 1.2.0
- List of modified principles:
    - VI. Event-Driven Extensibility (Specified Redis as broker)
- Added sections:
    - IX. API Documentation (drf-spectacular / OpenAPI 3.0)
- Removed sections: None
- Templates requiring updates (✅ updated / ⚠ pending):
    - .specify/templates/plan-template.md (⚠ pending)
    - .specify/templates/spec-template.md (✅ aligned)
    - .specify/templates/tasks-template.md (⚠ pending)
- Follow-up TODOs: None
-->

# Django DRF Backend API Constitution

## Core Principles

### I. Code Quality & Standards
All generated code MUST strictly comply with PEP8, Flake8, Ruff, and Pylance standards. This ensures high readability, consistency across the codebase, and reduces the likelihood of static analysis errors.

### II. Phased Development Cycle
During the initial development stages, all types of testing (unit, integration, contract, etc.) MUST be omitted. Focus remains on rapid prototyping and architectural validation. Testing strategies will be reintroduced in subsequent maturity phases.

### III. Clean Architecture & Decoupling
- Prioritize Clean Architecture and decoupling to ensure long-term maintainability.
- Apply SOLID, DRY, and KISS principles to all code development.
- Variable and function names MUST be self-descriptive (Clean Code standards).
- Code should be readable, maintainable, and avoid unnecessary complexity.
- Separate business logic into Services and Repositories. This ensures a decoupled, testable, and maintainable codebase.
- Business logic MUST remain independent of external frameworks and delivery mechanisms.

### IV. Scoped Platform-User Authentication
Authentication MUST be implemented using JWT (SimpleJWT). Token scopes MUST be strictly restricted by both the User ID AND the Platform ID. Access is granted only when both identity and origin are valid.

### V. Multi-Platform Identity Management
The system MUST allow the same email address to exist across multiple platforms as independent entities. Account isolation is enforced at the platform level, preventing cross-platform data leakage while supporting user flexibility.

### VI. Event-Driven Extensibility
The notification system MUST be designed based on events. All implementation MUST be prepared for asynchronous processing, specifically targeting Celery for task execution with Redis as the message broker to keep the request-response cycle performant.

### VII. Dynamic Business Logic
Business rules (e.g., `max_devices` per user) MUST be dynamic and configurable via the database. These rules MUST be accessible and modifiable by administrators without requiring code changes or deployments.

### VIII. Performance & Scalability
Implement a caching strategy using Redis from the start to ensure low-latency API responses and system scalability.

### IX. API Documentation
Use `drf-spectacular` to automatically generate an interactive **Swagger/OpenAPI 3.0** documentation interface. All endpoints MUST be properly documented with summaries and descriptions to ensure developer clarity and system discoverability.

## Technical Stack

The following stack is MANDATORY for all project components:
- **Language**: Python 3.x
- **Framework**: Django + Django REST Framework (DRF)
- **API Documentation**: drf-spectacular (Swagger UI/OpenAPI 3.0)
- **Authentication**: SimpleJWT for token management
- **Caching & Broker**: Redis (for caching and as a Celery broker)
- **Database**: SQLite (initial implementation)
- **Orchestration**: Docker & Docker Compose

## Development Workflow

1. **Static Analysis**: All code must pass Ruff and Pylance checks before being considered for integration.
2. **Schema-First**: Entities and database schemas must be defined and validated against the Clean Architecture principle before implementation.
3. **Repository Pattern**: Data access MUST be abstracted through Repositories.
4. **Service Layer**: Business logic MUST be encapsulated in Services.
5. **Event Modeling**: New features must identify relevant events for the notification system during the design phase.
6. **API Documentation**: Every new endpoint or change to existing ones MUST include OpenAPI schema annotations (summaries, descriptions) for `drf-spectacular`.
7. **Configuration Mapping**: Any new business rule must be mapped to a database configuration entry rather than being hardcoded.

## Governance
This constitution is the foundational authority for all development within the project. Every change, specification, and implementation plan MUST be validated against these principles.

1. Amendments to this constitution require a version bump following semantic versioning.
2. Compliance reviews are mandatory for every feature implementation.
3. If a principle cannot be met, a formal justification must be documented in the Implementation Plan.

**Version**: 1.2.0 | **Ratified**: 2026-04-24 | **Last Amended**: 2026-04-24
