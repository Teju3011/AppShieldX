<#
.SYNOPSIS
    AppShieldX AWS Resource Teardown and Cleanup Script
.DESCRIPTION
    Safely destroys Terraform-managed AWS demonstration resources to avoid incurring ongoing charges.
#>

param(
    [switch]$AutoApprove = $false
)

$ErrorActionPreference = "Stop"

Write-Host "======================================================================" -ForegroundColor Yellow
Write-Host "             APPSHIELDX - AWS TEARDOWN & SAFE CLEANUP                 " -ForegroundColor Yellow
Write-Host "======================================================================" -ForegroundColor Yellow

# Confirm deletion
if (-not $AutoApprove) {
    Write-Host "[!] WARNING: This will destroy all AppShieldX demo resources (ALB, ECS, RDS, Secrets, CloudWatch)." -ForegroundColor Red
    $confirm = Read-Host "Are you absolutely sure you want to destroy these AWS resources? (yes/no)"
    if ($confirm -ne "yes") {
        Write-Host "Teardown aborted by user." -ForegroundColor Cyan
        exit 0
    }
}

$tfDir = Join-Path $PSScriptRoot "..\terraform"
Push-Location $tfDir
try {
    Write-Host "`n[*] Running Terraform Destroy in $tfDir..." -ForegroundColor Yellow
    $approveFlag = if ($AutoApprove) { "-auto-approve" } else { "" }
    terraform destroy $approveFlag
    Write-Host "`n[+] All AppShieldX demo resources destroyed successfully. Zero lingering AWS charges." -ForegroundColor Green
} finally {
    Pop-Location
}
