# Quickstart: Scoped Device Validation

## Setup
1. Authenticate with a specific platform:
   ```bash
   curl -X POST /auth/login/ -d '{"email": "user@example.com", "password": "password", "platform_slug": "mobile"}'
   ```
2. Use the returned access token to list devices:
   ```bash
   curl -H "Authorization: Bearer <token>" /devices/
   ```

## Development
- Repository: `src/users/repositories.py`
- Service: `src/users/services.py`
- View: `src/users/views.py`

## Linting
Ensure all code follows the 80-character limit and PEP8:
```bash
ruff check .
```
