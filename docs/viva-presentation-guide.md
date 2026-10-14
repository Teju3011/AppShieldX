# B.Tech Capstone Viva-Voce & Defense Presentation Guide

## Title
**Cloud-Native Runtime Protection and API Security Framework for Client-Server Mobile Applications**

---

## 1. Quick Project Elevator Pitch (30-Second Opening)
> *"Respected Examiners, our project is a production-grade Cloud-Native Security Framework designed to eliminate the asymmetric threat gap between untrusted mobile devices and enterprise API backends. Instead of treating the mobile app as a black-box, our framework embeds a lightweight client-side RASP (Runtime Application Self-Protection) SDK that continuously monitors the environment for root/jailbreak, Frida hooks, and debuggers, cryptographically reporting device risk telemetry to our Cloud-Native Zero-Trust API plane. Our Spring Cloud Gateway, Redis sliding-window rate limiters, and Threat Detection microservices dynamically gate transaction execution based on live risk scores, maintaining immutable audit trails and real-time SOC observability."*

---

## 2. Live Demonstration Script (Step-by-Step for Presentation)

### Step 1: Start Infrastructure & Microservices
```bash
# Terminal 1: Launch all containers
docker-compose up -d
docker-compose ps
```
- **Show Examiner**: All 6 Spring Boot microservices, Postgres, Redis, Prometheus, Grafana, ELK, and React Admin Dashboard running healthy on the custom bridge network.

### Step 2: Access SOC Admin Dashboard (Port 5173)
- Navigate to `http://localhost:5173`.
- Log in with credentials: `admin_sec` / `AdminMasterPass2026!`.
- **Show Examiner**: Real-time KPI cards (Total Threats, Critical Incidents, Monitored Devices, Active Block Rate), Live Recharts threat distribution pie chart and severity timeline.

### Step 3: Demonstrate Automated DevSecOps Audit
```bash
powershell -ExecutionPolicy Bypass -File .\scripts\run_devsecops_audit.ps1
```
- **Show Examiner**: Automated scans verifying zero hardcoded credentials, non-root Dockerfile users, and Kubernetes zero-trust network policies.

### Step 4: Run End-to-End Penetration & Security Test Suite
```bash
python scripts/security_test_suite.py
```
- **Show Examiner**: Live test executions proving:
  1. Automated rejection of tampered JWTs.
  2. RFC 7515 `alg: none` exploit rejection.
  3. Rejection of SQL injection attempts with parameterized queries.
  4. Instant HTTP 403 Forbidden blocking of mobile clients reporting device risk score $\ge 70$.
  5. Sliding-window rate limit enforcement (HTTP 429).

### Step 5: Run Full Pipeline Verification
```bash
python scripts/verify_e2e_pipeline.py
```
- **Show Examiner**: 8/8 verification gates passing with 100% compliance.

---

## 3. Top 30 Viva-Voce Questions & Comprehensive Answers

### Architectural Questions
#### Q1: Why did you build a Security Framework instead of just a secure mobile app?
**Answer**:
A secure mobile app is a single point solution. A **Security Framework** provides reusable architectural capabilities (client-side RASP, token lifecycle, Zero-Trust gateway filters, telemetry ingestion, dynamic risk scoring, immutable audit trails) that can be embedded into any mobile client and enterprise microservice ecosystem.

#### Q2: What is the Zero-Trust Architecture in this project?
**Answer**:
In conventional architectures, once a user authenticates with username/password, the server assumes the device is trustworthy. Under our Zero-Trust model:
1. *Never Trust, Always Verify*: Even with a valid JWT, every state-mutating request carries the client's `X-Device-Fingerprint` and `X-Device-Risk-Score`.
2. *Context-Aware Policy*: If a device is rooted, running Frida, or exhibiting high threat velocity ($R_{\text{device}} \ge 70$), the request is aborted with `HTTP 403 Forbidden` before it reaches business logic.

#### Q3: Why did you choose Spring Cloud Gateway instead of Zuul or Nginx?
**Answer**:
Spring Cloud Gateway is built on Spring Framework 6 and Project Reactor (non-blocking WebFlux netty server). It handles thousands of concurrent client connections with low thread overhead, supports reactive filter chains (`GatewayFilterFactory`), and integrates natively with Spring Security, Micrometer Prometheus metrics, and Redis.

---

### Client-Side RASP & Mobile Security Questions
#### Q4: How does your Android module detect Frida if the attacker renames the server binary?
**Answer**:
Our `FridaDetector.java` uses multiple heuristic layers:
1. *Network Probing*: Scans default local TCP ports `27042` and `27043`.
2. *Memory Map Inspection*: Parses `/proc/self/maps` looking for loaded memory segments matching `frida-agent.so`, `libfrida.so`, `gadget.so`.
3. *Thread Name Inspection*: Scans `/proc/self/task` for Frida internal threads (`gmain`, `gum-js-loop`). Even if the binary is renamed, Frida's Gum engine still names its internal POSIX threads.

#### Q5: How do you detect an attached debugger on Android and iOS?
**Answer**:
- On Android: Query `android.os.Debug.isDebuggerConnected()` and read `/proc/self/status` verifying `TracerPid == 0`.
- On iOS: Call POSIX `sysctl` with `CTL_KERN`, `KERN_PROC`, `KERN_PROC_PID` and test the `P_TRACED` bit flag in `kp_proc.p_flag`.

#### Q6: How does Certificate Pinning work and what attack does it prevent?
**Answer**:
Certificate pinning binds the client connection to the specific cryptographic Public Key (SHA-256 Subject Public Key Info - SPKI) of the server certificate. It prevents Man-In-The-Middle (MITM) attacks where an attacker installs a custom CA certificate into the device's root store (using tools like Burp Suite, Charles Proxy, or Fiddler).

#### Q7: What is `FLAG_SECURE` in Android?
**Answer**:
`WindowManager.LayoutParams.FLAG_SECURE` instructs the Android window manager that the window contents are sensitive. The OS blacks out the screen in the recent-apps switcher, prevents local screen captures via `takeScreenshot()`, and blocks third-party screen mirroring apps.

---

### Backend, Auth & Database Questions
#### Q8: How is the sliding-window rate limiter implemented?
**Answer**:
We implemented an atomic Lua script in Redis (`sliding_window_rate_limiter.lua`) using a Redis Sorted Set (`ZSET`). Each request timestamp is added with `ZADD`. Requests older than `now - window` are purged with `ZREMRANGEBYSCORE`. `ZCARD` returns the current count. Because it executes as an atomic Lua script on the Redis server, it guarantees zero race conditions without requiring distributed locks.

#### Q9: What happens when a user logs out?
**Answer**:
Since JWTs are stateless, they normally remain valid until expiration. Our `TokenBlacklistService` writes the revoked token or token ID into Redis with a Time-To-Live (TTL) matching the token's remaining validity. The API Gateway filter checks `hasKey("blacklist:" + token)`. If blacklisted, the request is immediately rejected with `HTTP 401 Unauthorized`.

#### Q10: How do you prevent SQL Injection and XSS?
**Answer**:
1. *SQL Injection*: Zero raw SQL concatenations. Spring Data JPA uses parameterized PreparedStatements under Hibernate.
2. *XSS*: Spring Security `SecurityHeadersFilter` injects `Content-Security-Policy: default-src 'self'`, `X-Content-Type-Options: nosniff`, and `X-XSS-Protection: 1; mode=block`.

---

### Cloud-Native & DevSecOps Questions
#### Q11: What Kubernetes resources did you implement and why?
**Answer**:
We created `k8s/` manifests including:
- `StatefulSet` for PostgreSQL with persistent volume claims (`PVC`).
- `Deployment` for stateless microservices with Horizontal Pod Autoscalers (`HPA`) scaling between 2 to 10 replicas on CPU/memory load.
- `ConfigMap` and `Secret` separating sensitive credentials from code.
- `Ingress` with TLS termination and CORS policy.
- `NetworkPolicy` enforcing Zero-Trust microsegmentation: default-deny all, only gateway allowed to call business service, only microservices allowed to reach Postgres/Redis.

#### Q12: How are distributed requests traced across 6 microservices?
**Answer**:
The API Gateway generates a unique `X-Correlation-ID` (UUID) in `CorrelationIdFilter` if not present on ingress. This header is propagated across downstream HTTP hops and recorded in every application log via Logback MDC and into every record in `audit-logging-service`.
