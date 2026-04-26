# Quickstart: Unit Testing Suite

## Overview
This feature introduces a comprehensive unit testing suite using `pytest`.

## Getting Started
1. Install dependencies:
   ```bash
   pip install pytest pytest-django pytest-mock
   ```

2. Configuration:
   The `pytest.ini` is located in the root directory. It configures the Django environment to use `core.settings` and adds `backend/src` to the `PYTHONPATH`.

3. Running Tests:
   Execute the following command from the project root:
   ```bash
   pytest
   ```

## Test Structure
- `backend/src/<module>/tests/test_repositories.py`: Data layer unit tests.
- `backend/src/<module>/tests/test_services.py`: Business logic unit tests (with mocked dependencies).

## Mocking
- Redis client and cross-module services (e.g., `NotificationService`) should be mocked using `mocker` from `pytest-mock`.
- Ensure tests remain fast by avoiding network or database connections for non-repository logic.
