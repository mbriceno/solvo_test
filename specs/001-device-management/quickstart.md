# Quickstart: Multi-Platform Device Management API

## Environment Setup
1. `docker-compose up -d --build`
2. `docker-compose exec backend python manage.py migrate`
3. `docker-compose exec backend python manage.py createsuperuser`

## Initial Configuration
1. Access Django Admin.
2. Create a `Platform` (slug: `alpha`).
3. Create a `GlobalConfig` entry:
   - `rule_name`: `max_devices`
   - `default_value`: `5`

## Usage Flow
1. **Register**: `POST /api/v1/auth/register/` with `platform_slug: alpha`.
2. **Login**: `POST /api/v1/auth/login/` to get JWT.
3. **Register Device**: `POST /api/v1/devices/` with Bearer token.
4. **List Devices**: `GET /api/v1/devices/` to see paginated results.

## Documentation
- Interactive Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
