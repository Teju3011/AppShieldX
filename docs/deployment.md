# Deployment & Operational Runbook

## 1. Prerequisites & Host Sizing

| Component | Minimum Sizing | Recommended Sizing |
| :--- | :--- | :--- |
| **CPU** | 4 Cores | 8 Cores |
| **RAM** | 8 GB | 16 GB |
| **Disk** | 25 GB SSD | 50 GB NVMe |
| **Software** | Docker 24+, Docker Compose v2.20+, Java 21+, Node 18+ |

---

## 2. Local Multi-Container Deployment (Docker Compose)

### 2.1 Configuration Step
Copy the environment template and verify database and secret values:
```bash
cp .env.example .env
```

### 2.2 Orchestration Bootstrap
To launch the complete cloud-native infrastructure and all microservices in order:
```bash
# Build all microservice images and spin up stack
docker compose up -d --build

# Verify container statuses and health probes
docker compose ps
```

### 2.3 Verification Health Check Matrix
Once containers report `healthy`:
- **API Gateway**: `curl -f http://localhost:8080/actuator/health`
- **Auth Service**: `curl -f http://localhost:8081/actuator/health`
- **Threat Detection**: `curl -f http://localhost:8084/actuator/health`
- **Admin Dashboard**: Open `http://localhost:5173` in a web browser
- **Grafana**: Open `http://localhost:3000` (User: `admin`, Pass: `Grafana_Admin_Secure123!`)
- **Kibana**: Open `http://localhost:5601`

---

## 3. Kubernetes Production Staging Deployment

The `infrastructure/kubernetes/` directory contains standard K8s manifests organized by resource type:
```bash
# 1. Create dedicated namespace
kubectl apply -f infrastructure/kubernetes/namespace.yaml

# 2. Deploy ConfigMaps & Secrets
kubectl apply -f infrastructure/kubernetes/configmap.yaml
kubectl apply -f infrastructure/kubernetes/secrets.yaml

# 3. Deploy Stateful Storage (PostgreSQL & Redis)
kubectl apply -f infrastructure/kubernetes/postgres/
kubectl apply -f infrastructure/kubernetes/redis/

# 4. Deploy Core Microservices
kubectl apply -f infrastructure/kubernetes/api-gateway/
kubectl apply -f infrastructure/kubernetes/auth-service/
kubectl apply -f infrastructure/kubernetes/user-service/
kubectl apply -f infrastructure/kubernetes/business-service/
kubectl apply -f infrastructure/kubernetes/threat-detection-service/
kubectl apply -f infrastructure/kubernetes/audit-logging-service/

# 5. Apply Ingress Controller Rules
kubectl apply -f infrastructure/kubernetes/ingress.yaml
```
