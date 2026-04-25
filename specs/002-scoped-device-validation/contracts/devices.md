# API Contract: Devices

## Endpoints

### GET /devices/
List devices for the authenticated user on the current platform.

**Authentication**: Bearer Token (JWT)

**Success Response**:
- **Code**: 200 OK
- **Content**:
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "My Phone",
      "ip_address": "192.168.1.1",
      "is_active": true,
      "last_seen": "2026-04-25T12:00:00Z"
    }
  ]
}
```

**Description**:
Results are automatically filtered based on the `user_id` and `platform_slug` embedded in the JWT. Users will only see devices belonging to the platform they used to authenticate.
