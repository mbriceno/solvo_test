# Architectural Decisions: Multi-Platform Device Management API

## 1. Clean Architecture & Decoupling
The project follows a modular structure where business logic is separated from Django's views and models. We use the **Repository Pattern** for data access and the **Service Layer** for orchestrating business rules.

## 2. Multi-tenant Identity Management
To support independent accounts with the same email across different platforms, we implemented a `CustomUser` model with a `UniqueConstraint(email, platform)`. Username generation follows the pattern `{email}_{platform_slug}` to ensure compatibility with Django's internal uniqueness requirements.

## 3. Dynamic Rule Validation & Caching
Business rules (e.g., `max_devices`) are hierarchical. The `RuleResolver` merges `GlobalConfig` defaults with `Platform` overrides. To maintain low latency, resolved rules are cached in **Redis** with a 1-hour expiration.

## 4. Scoped Authentication
JWT tokens generated via `SimpleJWT` include a custom `platform_slug` claim. This allows the backend to derive the tenant context directly from the token, ensuring that users can only access resources belonging to their registered platform.

## 5. Automated Documentation
We use `drf-spectacular` for OpenAPI 3.0 schema generation. This ensures that the API is self-documenting and provides an interactive Swagger UI for developers.

## 7. Service-Repository for Scoped Validation
The **Service-Repository** pattern was specifically leveraged to enforce platform-scoped data access. By moving filtering logic into `DeviceRepository.find_by_user_and_platform` and orchestrating it through `DeviceService`, we ensure that data isolation is not a "view-level concern" but a foundational property of the system. This "defense in depth" prevents cross-platform data leakage even if different delivery mechanisms (CLI, Admin, API) are added later.

## 8. Indexing Strategy for Scale
To support the target scale of **1 million users**, a composite index was added to the `Device` model on `(user_id, platform_id)`. This ensures that scoped retrieval queries (which are the most frequent operation) remain low-latency and performant as the dataset grows. The indexing strategy prioritizes read performance in the primary user journey.

## 9. Isolated Notification Domain Module
The `notifications` system is implemented as a standalone domain module to ensure microservice readiness and clean separation of concerns. By using a **Service-Repository** pattern and a **Strategy-based Dispatcher**, we isolate delivery logic (Email, SMS, Socket) from business triggers (e.g., Auth registration). This architecture allows the system to scale its delivery capabilities independently of other core business services.

