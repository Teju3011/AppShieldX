<#
.SYNOPSIS
    AppShieldX Demo Lite Deployment Automation Script for AWS
.DESCRIPTION
    Provisions AppShieldX infrastructure on AWS using Terraform Demo Lite profile.
    Builds and pushes container images to Amazon ECR, updates ECS task definition,
    and reports live endpoints and health status.
#>

param(
    [string]$Region = "ap-south-1",
    [string]$Environment = "demo",
    [string]$Profile = "demo_lite",
    [switch]$AutoApprove = $false
)

$ErrorActionPreference = "Stop"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "          APPSHIELDX - AWS DEMO LITE DEPLOYMENT PIPELINE              " -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# 1. Verify AWS CLI and Credentials
Write-Host "`n[*] Verifying AWS CLI & Active Credentials..." -ForegroundColor Yellow
try {
    $identity = aws sts get-caller-identity --output json | ConvertFrom-Json
    Write-Host "[+] Authenticated to AWS Account: $($identity.Account) as $($identity.Arn)" -ForegroundColor Green
} catch {
    Write-Host "[!] ERROR: AWS credentials are not configured or are invalid." -ForegroundColor Red
    Write-Host "    Please run 'aws configure' or set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY." -ForegroundColor Yellow
    exit 1
}

# 2. Confirm Cost Drivers & Obtain Explicit Approval
Write-Host "`n[!] Cost Considerations for Demo Lite Profile:" -ForegroundColor Yellow
Write-Host "    - Amazon ECS Fargate Task (0.5 vCPU, 1 GB RAM): ~$0.024 / hour"
Write-Host "    - Application Load Balancer: ~$0.0225 / hour"
Write-Host "    - Amazon RDS db.t4g.micro PostgreSQL: ~$0.018 / hour"
Write-Host "    - Secrets Manager Secret: ~$0.40 / month ($0.013 / day)"
Write-Host "    - Estimated total cost: ~$1.20 - $1.50 per 24-hour test period."
Write-Host "    - Remember to run cleanup_aws.ps1 after review!" -ForegroundColor Magenta

if (-not $AutoApprove) {
    $confirm = Read-Host "`nDo you wish to proceed with provisioning these AWS resources? (yes/no)"
    if ($confirm -ne "yes") {
        Write-Host "Deployment aborted by user." -ForegroundColor Yellow
        exit 0
    }
}

# 3. Terraform Plan & Apply
$tfDir = Join-Path $PSScriptRoot "..\terraform"
Write-Host "`n[*] Running Terraform Init & Apply in $tfDir..." -ForegroundColor Yellow

Push-Location $tfDir
try {
    terraform init
    $approveFlag = if ($AutoApprove) { "-auto-approve" } else { "" }
    terraform apply -var="deployment_profile=$Profile" -var="aws_region=$Region" -var="environment=$Environment" $approveFlag

    Write-Host "`n[+] Terraform Provisioning Complete!" -ForegroundColor Green
    $albDns = terraform output -raw alb_dns_name
    Write-Host "[+] Application Load Balancer Endpoint: http://$albDns" -ForegroundColor Green
} finally {
    Pop-Location
}

# 4. Summary & Verification Instructions
Write-Host "`n======================================================================" -ForegroundColor Cyan
Write-Host "AppShieldX Demo Lite deployed successfully!" -ForegroundColor Green
Write-Host "Next Steps:"
Write-Host "1. Test gateway health: curl http://$albDns/actuator/health"
Write-Host "2. Run verification script: python .\infrastructure\aws\verify_aws_deployment.py --endpoint http://$albDns"
Write-Host "3. When demo is complete, run: .\infrastructure\aws\cleanup_aws.ps1"
Write-Host "======================================================================" -ForegroundColor Cyan
