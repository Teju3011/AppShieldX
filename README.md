# AppShieldX — A Cloud-Native Runtime Protection and API Security Framework for Client–Server Android and iOS Applications

[![AppShieldX](https://img.shields.io/badge/AppShieldX-v1.0.0-00E5FF.svg)]()
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.3.3-6DB33F.svg)]()
[![Flutter](https://img.shields.io/badge/Flutter-3.24-02569B.svg)]()
[![React](https://img.shields.io/badge/React-18.3-61DAFB.svg)]()
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1.svg)]()
[![Redis](https://img.shields.io/badge/Redis-7.2-DC382D.svg)]()
[![AWS ECS](https://img.shields.io/badge/AWS-ECS%20Fargate-FF9900.svg)]()
[![Zero Trust](https://img.shields.io/badge/Zero--Trust-Enforced-red.svg)]()

> **AppShieldX** is an enterprise-grade cybersecurity platform providing mobile Runtime Application Self-Protection (RASP), hardware Keystore/Keychain integration, TLS certificate pinning, Zero-Trust Spring Cloud Gateway defenses, real-time threat risk calculation ($0-100$), immutable audit logging, a React 18 SOC dashboard, and native AWS deployment.
>
> 🔬 **Research Contribution**: Cross-layer threat correlation and server-side risk-adaptive enforcement using mobile runtime security telemetry and backend API behavior. Bridges the semantic gap between client RASP indicators and cloud API authorization across 4 authoritative response bands (`ALLOW`, `MONITOR`, `STEP_UP_AUTHENTICATION`, `RESTRICT_SENSITIVE_ACTIONS`).
>
> 📚 **Research Documentation**:
> - [Research Methodology & Validation Report](docs/research-methodology.md)
> - [Comparative Literature Review](docs/literature-review.md)
> - [Reusable Integration Guide](docs/reusable-integration-guide.md)
> - [Experimental Results Dataset](experiments/results/summary_metrics.json)

---

## 🏛️ System Architecture

```text
+-------------------------------------------------------------------------+
|                         MOBILE CLIENT (Flutter)                         |
|  [Hardware Keystore] <--> [TokenManager] <--> [RASP Engine (C/Native)]  |
|                                |                                        |
|                     Pinned TLS 1.3 Connection                           |
+--------------------------------+----------------------------------------+
                                 |
                                 v
+-------------------------------------------------------------------------+
|                  SPRING CLOUD API GATEWAY (Port 8080)                   |
|  - CorrelationIdFilter (UUID generation / propagation)                  |
|  - SecurityHeadersFilter (HSTS, CSP, X-Frame-Options: DENY)             |
|  - RateLimitEnforcementFilter (Redis atomic sliding-window Lua)         |
|  - JwtAuthenticationGatewayFilterFactory (Cryptographic token check)    |
+---+----------------------------+-----------------------------+----------+
    |                            |                             |
    v                            v                             v
+------------------+   +----------------------+   +-----------------------+
|  Auth Service    |   | User Service         |   | Business Service      |
|  (Port 8081)     |   | (Port 8082)          |   | (Port 8083)           |
|  - JWT Issuance  |   | - Profile CRUD       |   | - Zero-Trust Filter   |
|  - Refresh Cycle |   | - Password Rotation  |   | - Risk >= 70 Reject   |
|  - Token Blacklist   | - Role RBAC          |   | - Entity Ops          |
+------------------+   +----------------------+   +-----------------------+
    |                            |                             |
    +----------------------------+-----------------------------+
                                 |
        +------------------------+------------------------+
        |                                                 |
        v                                                 v
+----------------------------------+   +----------------------------------+
| Threat Detection Service (8084)  |   | Audit Logging Service (8085)     |
| - Telemetry Ingest & Dedup       |   | - Immutable Security Trail       |
| - Sliding Velocity Window        |   | - X-Correlation-ID Indexing      |
| - Dynamic Risk Scoring (0-100)   |   | - SIEM Metric Aggregation        |
+----------------------------------+   +----------------------------------+
        |                                                 |
        +------------------------+------------------------+
                                 |
                                 v
+-------------------------------------------------------------------------+
|                PERSISTENCE & OBSERVABILITY INFRASTRUCTURE               |
|  PostgreSQL 16 (Relational DDL)  |  Redis 7 (Distributed Cache & State) |
|  Prometheus 2.52 (Time Series)   |  Grafana 10.4 (SOC Telemetry Boards) |
|  Elasticsearch 8.13 / Logstash   |  React 18 Admin Dashboard (Port 5173)|
+-------------------------------------------------------------------------+
```

---

## 🚀 Key Framework Capabilities

### 1. Mobile Runtime Protection (RASP)
- **Multi-Heuristic Root & Jailbreak Detection**:
  - Probes for binary artifacts (`su`, `busybox`, `cydia`, `sileo`).
  - Analyzes `/proc/mounts` verifying system partitions are read-only.
  - Verifies process sandbox isolation.
- **Dynamic Binary Instrumentation & Frida Defense**:
  - Scans default listening local TCP ports (`27042`, `27043`).
  - Inspects `/proc/self/maps` for injected libraries (`frida-agent.so`, `gadget.so`).
  - Scans POSIX thread names in `/proc/self/task` (`gmain`, `gum-js-loop`).
- **Anti-Debugging & Tamper Resistance**:
  - Reads `/proc/self/status` verifying `TracerPid == 0`.
  - Kernel `sysctl` with `CTL_KERN` and `P_TRACED` on iOS.
  - App signature and DEX/Mach-O cryptographic checksum verification.
- **Hardware-Backed Storage**:
  - Uses `AndroidKeyStore` (AES-256-GCM) and iOS Keychain (`kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly`).
  - Screen privacy with Android `FLAG_SECURE` and iOS background blur.

### 2. Cloud-Native Zero-Trust API Defense
- **Spring Cloud Gateway (Port 8080)**:
  - Cryptographic JWT validation via `JwtAuthenticationGatewayFilterFactory`.
  - Distributed request correlation tracking (`X-Correlation-ID`).
  - Strict security headers (`HSTS`, `CSP`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`).
- **Redis Sliding-Window Rate Limiting**:
  - Atomic Redis Lua script (`sliding_window_rate_limiter.lua`) operating over Sorted Sets (`ZSET`).
  - Resilient to race conditions and burst attacks.
- **Real-Time Dynamic Device Risk Scoring (Port 8084)**:
  - Computes weighted device risk scores ($0 - 100$) from live mobile telemetry and threat velocity.
- **Zero-Trust Policy Enforcement (Port 8083)**:
  - Intercepts state-mutating requests with `ZeroTrustSecurityFilter`.
  - Blocks transactions from devices with risk scores $\ge 70$ with `HTTP 403 Forbidden`.
- **Immutable Audit Logging (Port 8085)**:
  - Write-only audit trail recording user identity, client IP, device fingerprint, risk score, and correlation ID.
- **React 18 SOC Admin Dashboard (Port 5173)**:
  - Live metric KPI cards, real-time threat feed, and interactive Recharts visualizations.

---

## 📡 Service Port Allocations & Credentials

| Service | Container Name | Port | Description |
| :--- | :--- | :--- | :--- |
| **API Gateway** | `security-framework-gateway` | `8080` | Edge reverse proxy & security filters |
| **Auth Service** | `security-framework-auth` | `8081` | JJWT lifecycle, refresh tokens, Redis blacklist |
| **User Service** | `security-framework-user` | `8082` | User profiles and RBAC management |
| **Business Service** | `security-framework-business` | `8083` | Transactions & Zero-Trust risk filter |
| **Threat Service** | `security-framework-threat` | `8084` | Telemetry ingestion & dynamic risk scoring |
| **Audit Service** | `security-framework-audit` | `8085` | Immutable audit log trail & SIEM metrics |
| **Admin Dashboard** | `security-framework-admin-ui` | `5173` | React 18 + TypeScript SOC interface |
| **PostgreSQL** | `security-framework-postgres` | `5432` | Primary relational database (PostgreSQL 16) |
| **Redis** | `security-framework-redis` | `6379` | Token blacklist & sliding-window rate limiter |
| **Prometheus** | `security-framework-prometheus`| `9090` | Time-series metric collector |
| **Grafana** | `security-framework-grafana` | `3000` | SOC observability dashboards |
| **Elasticsearch** | `security-framework-elasticsearch`| `9200` | SIEM security event index |
| **Kibana** | `security-framework-kibana` | `5601` | Log exploration interface |

### Seeded Credentials

| Account | Username / Email | Password | Role |
| :--- | :--- | :--- | :--- |
| **Admin SOC User** | `admin_sec` / `admin@security.local` | `AdminMasterPass2026!` | `ROLE_ADMIN` |
| **Standard User** | `demo_user` / `demo@security.local` | `UserDemoPass2026!` | `ROLE_USER` |
| **PostgreSQL Root**| `postgres_admin` | `SecuritySuperSecretPassword123!` | DB Superuser |
| **Redis Server** | `default` | `RedisStrongFrameworkPassword2026!` | Cache Admin |
| **Grafana Admin** | `admin` | `AdminSecurityGrafana2026!` | Grafana Admin |

---

## 🛠️ Quickstart & Deployment

### 1. Prerequisites
- Docker Engine 24+ & Docker Compose v2+
- Java JDK 17+ (or JDK 21 / 24)
- Maven 3.9+
- Node.js 20+
- Python 3.9+ (for security verification test suite)

### 2. Launch Entire Infrastructure with Docker Compose
```bash
# Clone and enter workspace
git clone https://github.com/framework/cloud-native-mobile-security-framework.git
cd cloud-native-mobile-security-framework

# Launch all 14 containers in detached mode
docker-compose up -d --build

# Verify container status
docker-compose ps
```

Access services:
- **SOC Admin Dashboard**: [http://localhost:5173](http://localhost:5173)
- **API Gateway**: [http://localhost:8080](http://localhost:8080)
- **Grafana Dashboard**: [http://localhost:3000](http://localhost:3000)
- **Kibana SIEM**: [http://localhost:5601](http://localhost:5601)
- **Prometheus Metrics**: [http://localhost:9090](http://localhost:9090)

---

## 🧪 Automated Testing & DevSecOps Verification

### 1. Run Microservices Unit & Integration Tests (100% Passing)
```bash
# Run Maven tests across microservices
mvn test -f backend/api-gateway/pom.xml
mvn test -f backend/auth-service/pom.xml
mvn test -f backend/user-service/pom.xml
mvn test -f backend/business-service/pom.xml
mvn test -f backend/threat-detection-service/pom.xml
mvn test -f backend/audit-logging-service/pom.xml
```

### 2. Run DevSecOps Compliance Auditor
```powershell
# Windows PowerShell
powershell -ExecutionPolicy Bypass -File .\scripts\run_devsecops_audit.ps1

# Linux / macOS Bash
bash ./scripts/run_devsecops_audit.sh
```

### 3. Run Automated Security Penetration Suite
```bash
python scripts/security_test_suite.py
```
Validates:
- Security headers & Correlation ID propagation
- Rejection of unauthenticated API calls (HTTP 401)
- Rejection of signature-tampered JWTs (HTTP 401)
- Protection against RFC 7515 `alg: none` exploit
- Zero-Trust blocking of high-risk mobile devices (HTTP 403)
- SQL injection prevention via parameterized queries
- Sliding-window rate limiting enforcement (HTTP 429)

### 4. Run End-to-End Pipeline Verification
```bash
python scripts/verify_e2e_pipeline.py
```

---

## 📂 Repository Structure

```text
cloud-native-mobile-security-framework/
├── admin-dashboard/                 # React 18 + TypeScript + Vite SOC Dashboard
│   ├── src/
│   │   ├── components/              # Layout, Sidebar, Navbar
│   │   ├── context/                 # AuthContext
│   │   ├── pages/                   # Dashboard, Threats, Audits, Users, Login
│   │   └── services/                # Axios API clients
│   ├── Dockerfile
│   └── nginx.conf
├── backend/                         # Spring Boot 3.3.3 Microservices
│   ├── api-gateway/                 # Reactive Gateway, JWT & RateLimit Filters (Port 8080)
│   ├── auth-service/                # JJWT Token Lifecycle & Redis Blacklist (Port 8081)
│   ├── user-service/                # User Profile Management & RBAC (Port 8082)
│   ├── business-service/            # Business Operations & Zero-Trust Filter (Port 8083)
│   ├── threat-detection-service/    # Telemetry Ingestion & Dynamic Risk Engine (Port 8084)
│   └── audit-logging-service/       # Immutable Audit Logs & SIEM Feeds (Port 8085)
├── database/                        # Database DDL & Flyway Migrations
│   ├── init.sql
│   └── migrations/
│       ├── V1__init_schema.sql
│       └── V2__seed_initial_data.sql
├── docs/                            # Comprehensive Project Documentation
│   ├── architecture.md
│   ├── btech-capstone-report.md     # Full Academic Project Report
│   ├── viva-presentation-guide.md   # Viva-Voce Q&A & Demo Script
│   └── ...
├── k8s/                             # Production Kubernetes Manifests
│   ├── namespace.yaml
│   ├── config-and-secrets.yaml
│   ├── data-stores.yaml             # Postgres StatefulSet & Redis Deployment
│   ├── microservices.yaml           # Deployments & Services with Health Probes
│   ├── ingress.yaml                 # TLS Ingress & CORS Rules
│   ├── hpa.yaml                     # Horizontal Pod Autoscalers
│   └── network-policy.yaml          # Zero-Trust Pod Microsegmentation
├── mobile/                          # Flutter Reference Consumer Application
│   ├── android/                     # Native Root, Frida, Debugger & Keystore Detectors
│   ├── ios/                         # Native Jailbreak, Sysctl Debugger & Keychain
│   └── lib/
│       ├── core/                    # RASP Manager, TokenManager, SQLite Event Queue
│       └── features/                # Riverpod Notifiers, RASP Matrix UI, Screens
├── monitoring/                      # Observability & SIEM Stack
│   ├── elk/                         # Logstash pipeline & Elasticsearch configs
│   ├── grafana/                     # Provisioned datasources and SOC dashboards
│   └── prometheus/                  # Prometheus scraping & alerting rules
├── redis/                           # Redis Configuration & Atomic Lua Scripts
│   ├── redis.conf
│   └── scripts/
│       ├── sliding_window_rate_limiter.lua
│       └── token_blacklist.lua
├── scripts/                         # DevSecOps & Automated Security Test Scripts
│   ├── security_test_suite.py
│   ├── verify_e2e_pipeline.py
│   ├── seed_threat_data.py
│   ├── run_devsecops_audit.ps1
│   └── run_devsecops_audit.sh
├── docker-compose.yml               # Master 14-Container Orchestration
└── README.md
```

---

## 📚 AppShieldX Documentation Suite

| Document | File Path | Description |
| :--- | :--- | :--- |
| **System Architecture** | [architecture.md](file:///C:/Users/tej30/.gemini/antigravity-ide/scratch/cloud-native-mobile-security-framework/docs/architecture.md) | End-to-end topology, network zoning, and service mesh details |
| **STRIDE Threat Model** | [threat-model.md](file:///C:/Users/tej30/.gemini/antigravity-ide/scratch/cloud-native-mobile-security-framework/docs/threat-model.md) | Trust boundaries, STRIDE threat matrix, and security limitations |
| **OpenAPI 3.0 Contract** | [openapi.yaml](file:///C:/Users/tej30/.gemini/antigravity-ide/scratch/cloud-native-mobile-security-framework/docs/openapi.yaml) | Machine-readable API specifications covering all `/api/v1/` routes |
| **REST API Guide** | [api.md](file:///C:/Users/tej30/.gemini/antigravity-ide/scratch/cloud-native-mobile-security-framework/docs/api.md) | Endpoint catalog, authentication schemas, and RFC 7807 error models |
| **AWS Cloud Deployment**| [aws-deployment.md](file:///C:/Users/tej30/.gemini/antigravity-ide/scratch/cloud-native-mobile-security-framework/docs/aws-deployment.md) | Step-by-step Terraform deployment for Demo Lite and Full Cloud |
| **Live Demonstration** | [demo-guide.md](file:///C:/Users/tej30/.gemini/antigravity-ide/scratch/cloud-native-mobile-security-framework/docs/demo-guide.md) | Reviewer-friendly step-by-step test scripts for Demos 1 through 6 |
| **Cost & Safe Teardown** | [cost-and-cleanup.md](file:///C:/Users/tej30/.gemini/antigravity-ide/scratch/cloud-native-mobile-security-framework/docs/cost-and-cleanup.md) | Budget breakdown (~$1.50/day) and automated cleanup instructions |

---

## ☁️ AWS Cloud Demonstration (Terraform & CLI)

AppShieldX provides fully automated Terraform infrastructure for AWS deployment:
```bash
# 1. Initialize and review Terraform configuration
cd infrastructure/terraform
terraform init
terraform plan -var="deployment_profile=demo_lite"

# 2. Deploy to AWS (obtain user approval before billable provisioning)
powershell -ExecutionPolicy Bypass -File ../aws/deploy_demo_lite.ps1

# 3. Verify deployed ALB & Gateway health
python ../aws/verify_aws_deployment.py --endpoint http://<ALB_DNS_NAME>

# 4. Teardown all resources after review (zero lingering charges)
powershell -ExecutionPolicy Bypass -File ../aws/cleanup_aws.ps1 -AutoApprove
```

---

## ⚖️ License
This project is released under the **MIT License**. Created for academic and enterprise research into mobile runtime protection and cloud-native API defense.
