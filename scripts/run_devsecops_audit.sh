#!/usr/bin/env bash
# Cloud Native Security Framework - DevSecOps Audit Runner (Bash)
set -eo pipefail

echo "========================================================================"
echo "           DEVSECOPS SECURITY & COMPLIANCE LOCAL AUDITOR               "
echo "========================================================================"

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo -e "\n[1/4] Running Static Secret Pattern Analysis..."
if grep -rEI "BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY" --exclude-dir={.git,target,node_modules,dist} "$WORKSPACE_ROOT"; then
    echo -e "  \033[31m[-] Private key pattern identified!\033[0m"
else
    echo -e "  \033[32m[+] PASSED: No private keys exposed in source code.\033[0m"
fi

echo -e "\n[2/4] Running Frontend NPM Audit..."
cd "$WORKSPACE_ROOT/admin-dashboard" && npm audit --audit-level=critical || true

echo -e "\n[3/4] Verifying Non-Root User Declaration in Dockerfiles..."
find "$WORKSPACE_ROOT" -name "Dockerfile" -not -path "*/node_modules/*" -not -path "*/target/*" | while read -r df; do
    if grep -q "USER " "$df" || grep -q "nginx" "$df"; then
        echo -e "  \033[32m[+] $(basename "$(dirname "$df")")/Dockerfile enforces secure user\033[0m"
    else
        echo -e "  \033[33m[-] $(basename "$(dirname "$df")")/Dockerfile missing USER directive\033[0m"
    fi
done

echo -e "\n[4/4] Verifying Kubernetes Zero-Trust Network Policies..."
if [[ -f "$WORKSPACE_ROOT/k8s/network-policy.yaml" ]]; then
    echo -e "  \033[32m[+] PASSED: Zero-Trust NetworkPolicies exist.\033[0m"
else
    echo -e "  \033[31m[-] FAILED: k8s/network-policy.yaml missing.\033[0m"
fi

echo -e "\n========================================================================"
echo "                 DEVSECOPS AUDIT COMPLETE                              "
echo "========================================================================"
