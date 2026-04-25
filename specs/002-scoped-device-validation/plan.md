# Implementation Plan: Scoped Device Logic (Service-Repository Pattern)

**Branch**: `002-scoped-device-validation` | **Date**: 2026-04-25 | **Spec**: `/specs/002-scoped-device-validation/spec.md`
**Input**: Feature specification from `/specs/002-scoped-device-validation/spec.md`

## Summary
Implement platform-scoped device validation and filtering using the Service-Repository pattern. All queries will be strictly isolated to the authenticated user and platform context derived from the JWT.

## Technical Context
**Language/Version**: Python 3.x
**Primary Dependencies**: Django, DRF, SimpleJWT, Redis, drf-spectacular
**Storage**: SQLite (initial), Redis (caching/broker)
**Testing**: OMITTED (per Constitution Principle II)
**Target Platform**: Docker / Linux
**Project Type**: Backend API
**Performance Goals**: Low-latency with optimized indexing
**Constraints**: 80-char line limit, strict typing, PEP8/Ruff

## Constitution Check

- [x] **I. Code Quality**: Plan enforces 80-char limit, type hints, and PEP8.
- [x] **II. Phased Development**: No testing tasks included.
- [x] **III. Clean Architecture**: Logic separated into Services and Repositories.
- [x] **IV. Scoped Auth**: Design uses `platform_slug` from JWT.
- [x] **V. Multi-Platform Identity**: Models support user isolation by platform.
- [x] **VI. Event-Driven**: Celery/Redis used for notifications (already in core).
- [x] **VII. Dynamic Business Rules**: Rules fetched via RuleResolver.
- [x] **VIII. Performance**: Composite indexing planned for scale.
- [x] **IX. API Documentation**: drf-spectacular annotations planned.

## Project Structure

### Documentation (this feature)
```text
specs/002-scoped-device-validation/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    └── devices.md
```

### Source Code
```text
backend/src/
├── core/
│   ├── base.py
│   └── settings.py
├── users/
│   ├── models.py          # Add indexing
│   ├── repositories.py    # Add list_by_platform
│   ├── services.py        # Add filtered retrieval
│   └── views.py           # Update ViewSet filters
└── platforms/
    ├── models.py
    └── repositories.py
```

**Structure Decision**: Standard Django project structure with Service-Repository abstraction.

## Implementation Phases

### Phase 1: Data Layer Optimization
- Update `Device` model in `users/models.py` to add a composite index on `(user, platform)`.
- Update `DeviceRepository` in `users/repositories.py` to add `list_by_platform(user, platform)`.

### Phase 2: Business Logic Enhancement
- Update `DeviceService` in `users/services.py` to include retrieval logic.
- Ensure 100% type hinting and 80-char line limit.

### Phase 3: API & Context Integration
- Update `DeviceViewSet` in `users/views.py` to use `DeviceService` for all operations.
- Extract `platform_slug` from JWT context and pass it to the service layer.
- Update OpenAPI schema annotations.

### Phase 4: Quality Verification
- Manually verify PEP8/Ruff compliance.
- Ensure all functions have full type annotations.
