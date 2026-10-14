# AppShieldX - Reviewer Demonstration & Live Verification Guide

## 1. Overview
This live demonstration guide provides a reproducible, step-by-step verification plan for evaluating each core security capability of **AppShieldX: A Cloud-Native Runtime Protection and API Security Framework**.

Every test includes concrete CLI commands, HTTP request payloads, expected responses, and SOC dashboard observations.

---

## 2. Live Demonstrations

### Demo 1: Authentication Security & Role-Based Access Control (RBAC)
**Goal**: Prove JWT token issuance, password hashing, and rejection of tampered/expired tokens.

#### Step 1.1: Register a new user
```bash
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo_evaluator",
    "email": "evaluator@appshieldx.io",
    "password": "StrongPassword2026!"
  }'
```
**Expected Response**: `HTTP 201 Created` with user ID.

#### Step 1.2: Authenticate and obtain JWT
```bash
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "evaluator@appshieldx.io",
    "password": "StrongPassword2026!"
  }'
```
**Expected Response**: `HTTP 200 OK` containing `accessToken` and `refreshToken`.

#### Step 1.3: Access protected endpoint
```bash
curl -X GET http://localhost:8080/api/v1/users/me \
  -H "Authorization: Bearer <VALID_JWT_TOKEN>"
```
**Expected Response**: `HTTP 200 OK` with user profile.

#### Step 1.4: Tampered JWT signature rejection
```bash
curl -X GET http://localhost:8080/api/v1/users/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.tampered.signature"
```
**Expected Response**: `HTTP 401 Unauthorized` with message `"Invalid or expired JWT token"`.

---

### Demo 2: Distributed Sliding-Window Rate Limiting
**Goal**: Prove that the API Gateway enforces rate limiting via atomic Redis Lua scripts.

#### Step 2.1: Send rapid login requests exceeding the threshold (10 req/min)
Execute the automated rate-limiting test:
```bash
python -c "
import urllib.request, json
for i in range(15):
    try:
        req = urllib.request.Request('http://localhost:8080/api/v1/auth/login', 
            data=json.dumps({'email':'spam@test.io','password':'bad'}).encode(),
            headers={'Content-Type':'application/json'})
        resp = urllib.request.urlopen(req)
        print(f'Req {i+1}: HTTP {resp.status}')
    except urllib.error.HTTPError as e:
        print(f'Req {i+1}: HTTP {e.code} (Rate Limit Enforced)')
"
```
**Expected Result**: Requests 1–10 return `HTTP 401/200`. Request 11+ returns `HTTP 429 Too Many Requests` with headers:
- `Retry-After: 60`
- `X-RateLimit-Limit: 10`
- `X-RateLimit-Remaining: 0`

---

### Demo 3: Insecure Direct Object Reference (IDOR) & Zero-Trust Block
**Goal**: Prove that users cannot access resources belonging to other accounts.

#### Step 3.1: Authenticate as User A and create a confidential resource
```bash
curl -X POST http://localhost:8080/api/v1/resources \
  -H "Authorization: Bearer <USER_A_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"title": "User A Financial Audit", "sensitivity": "RESTRICTED"}'
```
Returns resource ID: e.g., `267dc6f8-9bca-42f9-9770-da9cd1e1f75a`.

#### Step 3.2: Authenticate as User B and attempt to retrieve User A's resource
```bash
curl -X GET http://localhost:8080/api/v1/resources/267dc6f8-9bca-42f9-9770-da9cd1e1f75a \
  -H "Authorization: Bearer <USER_B_TOKEN>"
```
**Expected Response**: `HTTP 403 Forbidden` or `HTTP 404 Not Found`. Cross-user data leakage is strictly prevented.

---

### Demo 4: Mobile Runtime Threat Ingestion & Dynamic Risk Scoring
**Goal**: Prove that mobile RASP events are ingested, verified, and escalate the device risk score.

#### Step 4.1: Submit a Frida and Root detection event
```bash
curl -X POST http://localhost:8080/api/v1/security/events \
  -H "Content-Type: application/json" \
  -H "X-Device-ID: demo-device-pixel-99" \
  -d '{
    "deviceId": "demo-device-pixel-99",
    "eventType": "FRIDA_DETECTED",
    "severity": "CRITICAL",
    "platform": "ANDROID",
    "detectionReason": "TCP port 27042 open and frida-agent.so found in /proc/self/maps"
  }'
```
**Expected Response**: `HTTP 202 Accepted`
```json
{
  "eventId": "...",
  "status": "PROCESSED",
  "assessedRiskScore": 85,
  "assessedRiskLevel": "CRITICAL",
  "actionEnforced": "SESSION_REVOKED"
}
```

#### Step 4.2: Verify Zero-Trust blocking of compromised device
Attempt to perform a transaction from the same device:
```bash
curl -X POST http://localhost:8080/api/v1/resources \
  -H "Authorization: Bearer <USER_TOKEN>" \
  -H "X-Device-ID: demo-device-pixel-99" \
  -H "Content-Type: application/json" \
  -d '{"title": "Attempted transaction from rooted phone"}'
```
**Expected Response**: `HTTP 403 Forbidden`
`ZERO_TRUST_BLOCK: Request rejected due to elevated device risk score: 85 >= 70 threshold.`

---

### Demo 5: Threat Correlation & SOC Dashboard Real-Time Visibility
**Goal**: Observe real security events and risk charts on the Web SOC Dashboard.

1. Open browser: **`http://localhost:5173`**
2. Log in with SOC Admin credentials:
   - Username / Email: `admin@security.local`
   - Password: `AdminMasterPass2026!`
3. Navigate to:
   - **Overview**: View total users, active devices, and threat severity distribution.
   - **Threat Telemetry**: View the `FRIDA_DETECTED` event ingested in Demo 4.
   - **API Gateway Security**: Observe rate-limit rejections and 403 Zero-Trust blocks.
   - **Device Fleet Posture**: Observe Android vs iOS compromise ratios and hardware attestation percentages.

---

### Demo 6: AWS Cloud Deployment & Telemetry Verification
**Goal**: Demonstrate live cloud deployment on AWS ECS Fargate and ALB.

#### Step 6.1: Run verification script against deployed ALB
```bash
python infrastructure/aws/verify_aws_deployment.py --endpoint http://<ALB_DNS_NAME> --region ap-south-1
```
**Expected Observations**:
1. `[PASS]` Gateway Health endpoint returns `HTTP 200 OK`.
2. `[PASS]` Strict security response headers present (`Strict-Transport-Security`, `Content-Security-Policy`).
3. `[PASS]` AWS ECS cluster and service status reporting active tasks.
4. Database and Redis are isolated within private subnets with no public internet route.
