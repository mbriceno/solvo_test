# API Contract: Authentication

## Base URL
`/api/v1/auth/`

## Register
`POST /register/`

### Request Body
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "platform_slug": "alpha"
}
```

### Response (201 Created)
```json
{
  "message": "User registered successfully."
}
```

## Login
`POST /login/`

### Request Body
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "platform_slug": "alpha"
}
```

### Response (200 OK)
```json
{
  "access": "<JWT>",
  "refresh": "<JWT>"
}
```
