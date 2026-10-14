output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "alb_dns_name" {
  description = "Public DNS hostname of the Application Load Balancer"
  value       = aws_lb.alb.dns_name
}

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.main.name
}

output "ecr_repository_urls" {
  description = "Map of created Amazon ECR repository URLs for image push"
  value       = { for k, v in aws_ecr_repository.repos : k => v.repository_url }
}

output "rds_endpoint" {
  description = "PostgreSQL RDS connection endpoint"
  value       = aws_db_instance.postgres.endpoint
}

output "secrets_manager_secret_arn" {
  description = "ARN of Secrets Manager credentials secret"
  value       = aws_secretsmanager_secret.app_secrets.arn
}

output "sns_alerts_topic_arn" {
  description = "ARN of the SNS topic for critical threat alerts"
  value       = aws_sns_topic.threat_alerts.arn
}

output "cloudwatch_log_group" {
  description = "CloudWatch log group for container logs"
  value       = aws_cloudwatch_log_group.ecs_logs.name
}

output "reports_s3_bucket" {
  description = "S3 bucket for compliance and audit report exports"
  value       = aws_s3_bucket.security_reports.bucket
}
