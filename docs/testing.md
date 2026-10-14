# Testing Strategy & Security Validation Guide

## 1. Overview & Testing Pyramid

The framework employs a rigorous multi-tier testing pyramid spanning unit tests, integration tests, contract verification, and automated vulnerability scanning:

```
               /\
              /  \      14 Demonstrable End-to-End Scenarios
             / E2E\     (Security Event Lifecycle & Policy Enforcement)
            /------\
           /  Sec   \   Security & Penetration Tests (Non-Destructive)
          /  Tests   \  (Invalid JWT, Rate-Limit Breaches, Malformed Payloads)
         /------------\
        / Integration  \ Spring Boot MockMvc / DataJpaTest / WireMock
       /     Tests      \
      /------------------\
     /    Unit Tests      \ JUnit 5, Mockito, Flutter Test, Kotlin JUnit
    /______________________\
```

---

## 2. Unit & Integration Testing Commands

### 2.1 Backend Services (Maven)
Execute all unit and security integration tests across the microservices suite:
```bash
cd backend
mvn clean test
```
To run tests for an isolated microservice:
```bash
mvn test -pl auth-service
mvn test -pl threat-detection-service
```

### 2.2 Flutter Mobile Client
Execute Dart unit and Riverpod provider state tests:
```bash
cd mobile
flutter test
```

### 2.3 Admin Dashboard (React/TypeScript)
Run frontend unit and lint checks:
```bash
cd admin-dashboard
npm test -- --watchAll=false
```

---

## 3. Safe Local Security Test Scenarios (14 Demonstrable Scenarios)

The project includes pre-configured, non-destructive test scripts demonstrating each framework defense mechanism:

1. **DEMO 1: Normal Secure Login**: Valid credentials return signed JWT and refresh token; records `AUTH_SUCCESS` audit event.
2. **DEMO 2: Invalid Login Attempt**: Incorrect password returns HTTP 401; records `AUTH_FAILURE` in database and increments Redis brute-force counter.
3. **DEMO 3: Expired JWT Handling**: Submitting an expired token to `/api/users/me` triggers HTTP 401 with standard error payload; client initiates seamless token rotation.
4. **DEMO 4: Unauthorized API Access**: Accessing protected endpoint without `Authorization` header triggers HTTP 401 from Gateway filter.
5. **DEMO 5: Forbidden Administrative Access**: User possessing only `ROLE_USER` attempting to invoke `/api/admin/**` triggers HTTP 403 Forbidden.
6. **DEMO 6: Distributed Rate Limiting**: Sending 6 consecutive login requests within 1 minute from the same IP returns HTTP 429 Too Many Requests and emits `RATE_LIMIT_EXCEEDED` alert.
7. **DEMO 7: Mobile Security Event Ingestion**: Simulated RASP probe dispatches `DEBUGGER_DETECTED` event via `/api/security/events`.
8. **DEMO 8: Runtime Threat Detection**: Device reporting `FRIDA_DETECTED` triggers immediate risk escalation to `CRITICAL`.
9. **DEMO 9: Persistent Incident Storage**: Verifying PostgreSQL `security_events` table stores immutable record with correlation ID, IP, and device metadata.
10. **DEMO 10: Audit Log Verification**: Validating all administrative and sensitive operations generate records in `audit_logs` table.
11. **DEMO 11: Real-Time Admin Dashboard Updates**: Opening React Admin Dashboard displays updated threat count, live charts, and severity breakdowns.
12. **DEMO 12: Prometheus Metric Scraping**: Verifying `/actuator/prometheus` exposes custom counters for `security_events_total` and `rate_limit_exceeded_total`.
13. **DEMO 13: Grafana Security Dashboard**: Pre-built dashboard visualizes real-time threat severity distributions and API latency percentiles.
14. **DEMO 14: Centralized ELK Log Pipeline**: Querying Kibana discovers structured JSON logs tagged with unified `correlationId`.
