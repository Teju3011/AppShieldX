# AppShieldX - AWS Cost Considerations & Safe Cleanup Guide

## 1. Budget Safety Principles

AppShieldX is designed to minimize cloud expenditures during academic and technical evaluations.
All cloud resources are tagged with:
- `Project = AppShieldX`
- `Environment = Demo`
- `ManagedBy = AppShieldX`

**Rule**: Cloud resources must never be left running unattended. Always destroy the demonstration environment when the live review session concludes.

---

## 2. Itemized Cost Estimation

### Profile A: Demo Lite (Recommended for Live Evaluation)
The **Demo Lite** profile uses single-AZ lightweight instances and public subnet routing with strict security groups to avoid NAT Gateway charges (~$1.08/day per NAT Gateway).

| AWS Resource | Resource Size / Type | Unit Cost | Estimated 24h Cost |
| :--- | :--- | :--- | :--- |
| **Amazon ECS on AWS Fargate** | 1 Task (0.5 vCPU, 1 GB RAM) | $0.024 / hr | $0.58 |
| **Application Load Balancer (ALB)** | 1 ALB (Basic ingress) | $0.0225 / hr | $0.54 |
| **Amazon RDS PostgreSQL** | 1 `db.t4g.micro` (Single-AZ, 20 GB gp3) | $0.018 / hr | $0.43 |
| **AWS Secrets Manager** | 1 Secret | $0.40 / mo | $0.01 |
| **Amazon CloudWatch Logs** | Ingestion & Storage (< 1 GB) | $0.50 / GB | $0.05 |
| **Amazon S3** | Standard Storage (< 1 GB) | $0.023 / GB | $0.01 |
| **Data Transfer** | Outbound to Internet (< 5 GB) | $0.09 / GB | $0.15 |
| **Total 24-Hour Evaluation Cost** | | | **~$1.77 USD** |

---

### Profile B: Full Cloud Demo Profile
The **Full Cloud Demo** profile implements enterprise Multi-AZ high availability with managed ElastiCache Redis and AWS WAF:

| AWS Resource | Resource Size / Type | Unit Cost | Estimated 24h Cost |
| :--- | :--- | :--- | :--- |
| **Amazon ECS Fargate** | 2 Tasks (Multi-AZ) | $0.048 / hr | $1.15 |
| **AWS ALB + AWS WAFv2** | ALB + 1 Web ACL | $0.035 / hr | $0.84 |
| **Amazon RDS Multi-AZ** | 1 `db.t4g.small` (Multi-AZ) | $0.072 / hr | $1.73 |
| **Amazon ElastiCache Redis** | 1 `cache.t4g.micro` node | $0.017 / hr | $0.41 |
| **AWS NAT Gateways** | 2 NAT Gateways (Multi-AZ) | $0.09 / hr | $2.16 |
| **Total 24-Hour Evaluation Cost** | | | **~$6.29 USD** |

---

## 3. Safe Teardown & Destruction Instructions

To prevent any unexpected billing, follow either of the two teardown workflows below:

### Option 1: Automated PowerShell Cleanup
From the repository root:
```powershell
powershell -ExecutionPolicy Bypass -File .\infrastructure\aws\cleanup_aws.ps1
```

### Option 2: Direct Terraform Teardown
```powershell
cd infrastructure\terraform
terraform destroy -var="deployment_profile=demo_lite" -auto-approve
```

### Verification of Zero Lingering Resources
Run the following AWS CLI checks to confirm that all resources have been purged:
```powershell
# 1. Verify ECS Tasks are terminated
aws ecs list-tasks --cluster appshieldx-demo-cluster --region ap-south-1

# 2. Verify Load Balancer is deleted
aws elbv2 describe-load-balancers --names appshieldx-demo-alb --region ap-south-1

# 3. Verify RDS Database instance is terminated
aws rds describe-db-instances --db-instance-identifier appshieldx-demo-postgres --region ap-south-1
```
If each command returns a `ResourceNotFound` error or an empty list, all billable infrastructure has been completely destroyed.
