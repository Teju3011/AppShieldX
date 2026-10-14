# REST API & Gateway Routing Specification

## 1. Gateway Routing Architecture & Headers

All external traffic enters through the **Spring Cloud API Gateway** on port `8080`. The Gateway enforces TLS termination, JWT validation, Redis-backed sliding-window rate limiting, and standard security headers.

### Required & Injected HTTP Headers

| Header | Description | Required on Request | Set / Validated By |
| :--- | :--- | :--- | :--- |
| `Authorization` | Bearer token format: `Bearer <JWT_ACCESS_TOKEN>` | Yes (for protected routes) | Validated by Gateway filter |
| `X-Correlation-ID` | Canonical request tracing UUID | Optional on Client (Gateway generates if missing) | Propagated across all services |
| `X-Device-ID` | Hardware/OS-derived unique identifier | Required on mobile auth & security endpoints | Verified by Threat Service |
| `Strict-Transport-Security` | Enforces HTTPS: `max-age=31536000; includeSubDomains` | Injected by Gateway | Gateway Response Filter |
| `X-Content-Type-Options` | Enforces MIME sniffing protection: `nosniff` | Injected by Gateway | Gateway Response Filter |
| `Content-Security-Policy` | Restricts resource loading | Injected by Gateway | Gateway Response Filter |

---

## 2. Global Standardized Error Model

All services adhere to the RFC 7807 compliant standardized error response structure handled by each service's `GlobalExceptionHandler`:

```json
{
  "timestamp": "2026-09-18T18:30:00.123Z",
  "status": 400,
  "error": "Bad Request",
  "message": "Validation failed: Email is not well-formed",
  "path": "/api/auth/register",
  "correlationId": "e14b2d35-90f7-4a57-b2f5-d069e2c45163"
}
```

---

## 3. Comprehensive REST Endpoint Catalog

### 3.1 Authentication Endpoints (`auth-service`)

#### `POST /api/auth/register`
- **Description**: Registers a new user account with default role `ROLE_USER`.
- **Authentication**: None (Public).
- **Rate Limit**: 5 requests / min / IP.
- **Request Body**:
```json
{
  "username": "developer_alice",
  "email": "alice@securityframework.io",
  "password": "SecurePassword123!"
}
```
- **Response (201 Created)**:
```json
{
  "id": "7b8d4f4e-128a-4db5-b827-0cf7a3036cf1",
  "username": "developer_alice",
  "email": "alice@securityframework.io",
  "message": "User registered successfully"
}
```

#### `POST /api/auth/login`
- **Description**: Authenticates user credentials and returns short-lived access JWT and refresh token.
- **Authentication**: None (Public).
- **Rate Limit**: 5 requests / min / IP.
- **Request Body**:
```json
{
  "email": "alice@securityframework.io",
  "password": "SecurePassword123!"
}
```
- **Response (200 OK)**:
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "tokenType": "Bearer",
  "expiresIn": 900,
  "user": {
    "id": "7b8d4f4e-128a-4db5-b827-0cf7a3036cf1",
    "username": "developer_alice",
    "roles": ["ROLE_USER"]
  }
}
```

#### `POST /api/auth/refresh`
- **Description**: Rotates refresh token and issues a new access token.
- **Authentication**: None (Refresh Token presented in body).
- **Request Body**:
```json
{
  "refreshToken": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}
```
- **Response (200 OK)**:
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "8f480329fc12d1b...",
  "tokenType": "Bearer",
  "expiresIn": 900
}
```

#### `POST /api/auth/logout`
- **Description**: Revokes refresh token in database and blacklists access token in Redis.
- **Authentication**: Bearer Token required.
- **Response (200 OK)**:
```json
{
  "message": "Session terminated successfully"
}
```

---

### 3.2 User Endpoints (`user-service`)

#### `GET /api/users/me`
- **Description**: Returns the authenticated caller's profile and active roles.
- **Authentication**: Bearer Token (`ROLE_USER` or `ROLE_ADMIN`).
- **Response (200 OK)**:
```json
{
  "id": "7b8d4f4e-128a-4db5-b827-0cf7a3036cf1",
  "username": "developer_alice",
  "email": "alice@securityframework.io",
  "roles": ["ROLE_USER"],
  "accountLocked": false,
  "createdAt": "2026-09-18T18:00:00Z"
}
```

---

### 3.3 Security & Threat Detection Endpoints (`threat-detection-service`)

#### `POST /api/security/events`
- **Description**: Ingests mobile runtime security events and anomalies.
- **Authentication**: Bearer Token or Device Fingerprint.
- **Rate Limit**: 20 requests / min / device.
- **Request Body**:
```json
{
  "deviceId": "c4b9f2d1-8a9e-4b2a-8f91-23f0a9b81e4c",
  "eventType": "FRIDA_DETECTED",
  "severity": "CRITICAL",
  "source": "MOBILE_RASP",
  "description": "Frida listening port 27042 open and frida-gadget.so mapped in memory",
  "metadata": {
    "osVersion": "Android 14",
    "architecture": "arm64-v8a",
    "tracerPid": 4812
  }
}
```
- **Response (202 Accepted)**:
```json
{
  "eventId": "9a01f78e-5b12-4cf3-94c5-55e69e46a781",
  "status": "PROCESSED",
  "assessedRiskLevel": "CRITICAL",
  "action": "SESSION_REVOKED"
}
```

#### `GET /api/security/status`
- **Description**: Queries current risk posture and active policies for the authenticated device.
- **Authentication**: Bearer Token.
- **Response (200 OK)**:
```json
{
  "deviceId": "c4b9f2d1-8a9e-4b2a-8f91-23f0a9b81e4c",
  "currentRiskLevel": "LOW",
  "activeThreats": 0,
  "enforcedPolicy": "ALLOW_NORMAL"
}
```

---

### 3.4 Business Resource Endpoints (`business-service`)

#### `GET /api/business/records`
- **Description**: Fetches user-scoped secure business records.
- **Authentication**: Bearer Token (`ROLE_USER`).
- **Response (200 OK)**:
```json
[
  {
    "id": "18a9ef34-bca1-47fa-92b1-098e7ad18f62",
    "title": "Confidential Security Audit Q3",
    "sensitivity": "RESTRICTED",
    "createdAt": "2026-09-18T12:00:00Z"
  }
]
```

---

### 3.5 Administrative Endpoints (`user-service` / Admin Route)

#### `GET /api/admin/dashboard/stats`
- **Description**: Aggregates high-level metrics for the React Admin Dashboard.
- **Authentication**: Bearer Token with `ROLE_ADMIN`.
- **Response (200 OK)**:
```json
{
  "totalUsers": 1240,
  "activeUsers": 890,
  "totalSecurityEvents": 312,
  "criticalThreats": 4,
  "failedLoginsLast24h": 47,
  "blockedRequests": 18,
  "systemHealth": "UP"
}
```

#### `GET /api/admin/security-events`
- **Description**: Paginated query of all captured runtime security events.
- **Authentication**: Bearer Token with `ROLE_ADMIN`.
- **Query Params**: `page=0&size=20&severity=CRITICAL`
- **Response (200 OK)**: Paginated Spring Data list of security event entities.
