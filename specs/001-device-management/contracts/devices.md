# API Contract: Devices

## Base URL
`/api/v1/devices/`

## List Devices
`GET /`

### Headers
- `Authorization`: `Bearer <JWT>`

### Response (200 OK)
```json
{
  "count": 15,
  "total_pages": 2,
  "next": "http://api.example.com/devices/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "My iPhone",
      "ip_address": "192.168.1.1",
      "is_active": true,
      "last_seen": "2026-04-24T10:00:00Z"
    }
  ]
}
```

## Register Device
`POST /`

### Request Body
```json
{
  "name": "New Device",
  "ip_address": "192.168.1.5"
}
```

### Response (201 Created)
```json
{
  "id": 2,
  "name": "New Device",
  "ip_address": "192.168.1.5",
  "is_active": true
}
```

### Response (403 Forbidden)
```json
{
  "error": "Device limit reached for this platform."
}
```
