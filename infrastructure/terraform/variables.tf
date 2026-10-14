variable "aws_region" {
  type        = string
  description = "AWS region for deployment"
  default     = "ap-south-1"
}

variable "environment" {
  type        = string
  description = "Environment identifier (e.g. demo, staging, prod)"
  default     = "demo"
}

variable "project_name" {
  type        = string
  description = "Project name"
  default     = "AppShieldX"
}

variable "deployment_profile" {
  type        = string
  description = "Deployment profile: 'demo_lite' (minimal single-instance/cost footprint) or 'full_cloud' (managed RDS multi-AZ, ElastiCache, ALB, WAF)"
  default     = "demo_lite"

  validation {
    condition     = contains(["demo_lite", "full_cloud"], var.deployment_profile)
    error_message = "deployment_profile must be either 'demo_lite' or 'full_cloud'."
  }
}

variable "app_version" {
  type        = string
  description = "Application image tag version"
  default     = "1.0.0"
}

variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "db_username" {
  type        = string
  description = "PostgreSQL root administrator username"
  default     = "postgres_admin"
}

variable "db_password" {
  type        = string
  description = "PostgreSQL root administrator password"
  sensitive   = true
  default     = "SecuritySuperSecretPassword123!"
}

variable "jwt_secret" {
  type        = string
  description = "HS256 Base64 Secret Key for JWT token signing"
  sensitive   = true
  default     = "c2VjdXJlUmFzcEZyYW1ld29ya1N1cGVyU2VjcmV0S2V5MjAyNlZlcnlMb25nU3RyaW5nRm9ySFMyNTY="
}

variable "alert_email" {
  type        = string
  description = "Optional SOC alert notification email for SNS topic subscription"
  default     = "security-alerts@appshieldx.io"
}

variable "enable_waf" {
  type        = bool
  description = "Enable AWS WAFv2 on the Application Load Balancer"
  default     = false
}
