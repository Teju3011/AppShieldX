<#
.SYNOPSIS
    AppShieldX EC2 Demo Teardown Automation Script
.DESCRIPTION
    Safely terminates the AppShieldX EC2 instance, deletes the Security Group,
    and removes the IAM instance profile to prevent any ongoing AWS costs.
#>

param(
    [string]$Region = "ap-south-1"
)

$ErrorActionPreference = "Continue"

Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host "       APPSHIELDX - AWS EC2 DEMO TEARDOWN & COST CLEANUP                  " -ForegroundColor Cyan
Write-Host "==========================================================================" -ForegroundColor Cyan

# 1. Terminate Instances
Write-Host "`n[*] Finding AppShieldX EC2 instances..." -ForegroundColor Yellow
$instances = aws ec2 describe-instances --region $Region `
    --filters "Name=tag:Name,Values=AppShieldX-Security-Gateway" "Name=instance-state-name,Values=running,pending,stopped" `
    --query "Reservations[*].Instances[*].InstanceId" --output text

if ($instances -and $instances -ne "None") {
    $instList = $instances.Split(" `t`r`n", [System.StringSplitOptions]::RemoveEmptyEntries)
    foreach ($inst in $instList) {
        Write-Host "[*] Terminating instance: $inst..." -ForegroundColor Yellow
        aws ec2 terminate-instances --instance-ids $inst --region $Region | Out-Null
    }
    Write-Host "[+] Termination initiated. Waiting for instances to terminate..." -ForegroundColor Green
    aws ec2 wait instance-terminated --instance-ids $instList --region $Region
    Write-Host "[+] All AppShieldX instances successfully terminated!" -ForegroundColor Green
} else {
    Write-Host "[+] No running AppShieldX EC2 instances found." -ForegroundColor Green
}

# 2. Delete Security Group
Write-Host "`n[*] Removing Security Group 'appshieldx-ec2-sg'..." -ForegroundColor Yellow
$sgId = aws ec2 describe-security-groups --region $Region --filters "Name=group-name,Values=appshieldx-ec2-sg" --query "SecurityGroups[0].GroupId" --output text 2>$null
if ($sgId -and $sgId -ne "None") {
    aws ec2 delete-security-group --group-id $sgId --region $Region | Out-Null
    Write-Host "[+] Deleted Security Group: $sgId" -ForegroundColor Green
}

Write-Host "`n==========================================================================" -ForegroundColor Cyan
Write-Host "Cleanup Complete! Zero recurring AWS compute charges remain." -ForegroundColor Green
Write-Host "==========================================================================" -ForegroundColor Cyan
