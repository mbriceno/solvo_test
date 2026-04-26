# Research: Unit Testing Suite for Core Modules

## Research Findings

### 1. Pytest Configuration with 'src/' layout
- **Configuration**: Since `manage.py` is in `backend/` and `src/` is a subdirectory, `PYTHONPATH` needs to be updated.
- **`pytest.ini` approach**:
  ```ini
  [pytest]
  DJANGO_SETTINGS_MODULE = core.settings
  pythonpath = backend/src
  testpaths = backend/src
  django_find_project = false
  ```
  Setting `django_find_project = false` prevents `pytest-django` from trying to auto-discover `manage.py` in the root, which simplifies the configuration for non-standard layouts.

### 2. Mocking Redis
- **Approach**: Use `pytest-mock` to patch the Redis client instance or the connection factory.
- **Pattern**:
  ```python
  def test_cache_logic(mocker):
      mock_redis = mocker.patch("django_redis.get_redis_connection")
      # Assert mock_redis.return_value.get(...) works as expected
  ```
- **Benefit**: Ensures test isolation and prevents dependencies on an active Redis server during unit test execution.

### 3. Mocking Celery Tasks
- **Approach**: Configure Celery to be synchronous during tests or patch the task `delay()`/`apply_async()` methods.
- **Pattern**:
  ```python
  # Using pytest-mock to patch the task
  def test_task_trigger(mocker):
      mock_task = mocker.patch("notifications.tasks.send_notification.delay")
      # Perform action that triggers task
      mock_task.assert_called_once()
  ```

### 4. Testing SimpleJWT Claims
- **Approach**: Instantiate the `Token` object (e.g., `RefreshToken.for_user(user)`) and assert the presence of custom claims in the payload.
- **Pattern**:
  ```python
  from rest_framework_simplejwt.tokens import RefreshToken
  
  def test_jwt_claims(user):
      token = RefreshToken.for_user(user)
      assert token.payload["platform_slug"] == "example-platform"
  ```

## Decisions & Rationale

- **Decision**: Use `pytest-mock` (via `mocker` fixture) for all mocking.
- **Rationale**: Provides consistent, clean, and thread-safe patching API that integrates well with `pytest`.
- **Decision**: Use `pytest-django` for database-backed tests.
- **Rationale**: Simplifies Django test setup, database transactions, and client/request mocking.
