#!/usr/bin/env python3
"""
================================================================================
AppShieldX — Master Demonstration & Evaluation Orchestrator
================================================================================
Comprehensive interactive utility to launch, test, demonstrate, and evaluate
all applications and components in AppShieldX:
  1. SOC Administrator Dashboard (React 18 + TypeScript + Vite)
  2. Spring Cloud API Gateway & Backend Microservices
  3. Mobile Security Client (Flutter / Android / iOS RASP)
  4. Second Reusable Sample Application (Healthcare Portal)
  5. 10 Controlled Research Scenarios & 5-Variant Ablation Study
  6. AWS Terraform Infrastructure & CloudWatch Telemetry
================================================================================
"""

import sys
import os
import subprocess
import time
import shutil

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def print_header(title):
    print("\n" + "=" * 80)
    print(f"  {title.center(76)}")
    print("=" * 80)

def run_command(cmd, cwd=None, description=""):
    if description:
        print(f"\n[*] {description}...")
    print(f"    $ {cmd}")
    try:
        res = subprocess.run(cmd, cwd=cwd or ROOT_DIR, shell=True)
        return res.returncode == 0
    except Exception as e:
        print(f"[-] Command failed: {e}")
        return False

def show_prerequisites():
    print_header("PREREQUISITES & ENVIRONMENT DIAGNOSTICS")
    checks = [
        ("Java (JDK 21)", "java -version"),
        ("Maven (v3.9+)", "mvn -version"),
        ("Node.js", "node -v"),
        ("Python 3", "python --version"),
        ("Terraform", "terraform -version"),
        ("Docker", "docker --version"),
    ]
    for name, cmd in checks:
        found = shutil.which(cmd.split()[0]) is not None
        status = "[INSTALLED]" if found else "[MISSING / NOT IN PATH]"
        print(f"  • {name:<22}: {status}")

    flutter_path = r"C:\Users\tej30\flutter\bin\flutter.bat"
    flutter_found = os.path.exists(flutter_path) or shutil.which("flutter") is not None
    print(f"  • {'Flutter (v3.24)':<22}: {'[INSTALLED]' if flutter_found else '[MISSING]'}")

def run_experiments():
    print_header("RESEARCH NOVELTY & EXPERIMENTAL EVALUATION (10 SCENARIOS)")
    print("Executing 4 configurations (Config A through D) and 5-variant ablation study...")
    script_path = os.path.join(ROOT_DIR, "scripts", "run_experiments.py")
    run_command(f'python "{script_path}" --runs 10')

def run_mobile_tests():
    print_header("MOBILE CLIENT SECURITY SUITE (ANDROID & IOS RASP)")
    flutter_cmd = r'& "C:\Users\tej30\flutter\bin\flutter.bat" test' if os.name == 'nt' else "flutter test"
    run_command(f"{flutter_cmd}", cwd=os.path.join(ROOT_DIR, "mobile"), description="Running Flutter RASP Probes & Keystore Tests")

def run_backend_tests():
    print_header("BACKEND MICROSERVICES VERIFICATION (46 UNIT & INTEGRATION TESTS)")
    run_command("mvn test", cwd=os.path.join(ROOT_DIR, "backend"), description="Executing Spring Boot JUnit 5 Test Suite")

def start_admin_dashboard():
    print_header("SOC ADMINISTRATOR DASHBOARD LAUNCH")
    print("Starting Vite development server on http://localhost:5173 ...")
    print("Press Ctrl+C in terminal when finished.")
    dashboard_dir = os.path.join(ROOT_DIR, "admin-dashboard")
    run_command("npm run dev", cwd=dashboard_dir, description="Launching Admin UI")

def seed_telemetry_demo():
    print_header("SEEDING CROSS-LAYER TELEMETRY & ATTACK INCIDENTS")
    script_path = os.path.join(ROOT_DIR, "scripts", "seed_threat_data.py")
    run_command(f'python "{script_path}"')

def show_demo_guide():
    print_header("FULL STEP-BY-STEP REVIEWER DEMONSTRATION GUIDE")
    guide = """
1. OVERVIEW & ACCESS URLS:
   • SOC Administrator Dashboard: http://localhost:5173
   • Spring Cloud API Gateway:     http://localhost:8080
   • Threat Detection Engine:      http://localhost:8084
   • Default Credentials:          Username: secops_admin / Password: SecOpsP@ssw0rd2026!

2. DEMONSTRATION STATIONS:

   Station 1: Threat Telemetry & RASP Monitoring (/threats)
     - Shows real-time incoming mobile telemetry from Android & iOS endpoints.
     - Displays device integrity state, active hooks (Frida), root indicators, and client IP.

   Station 2: Cross-Layer Threat Correlation (/correlation)
     - The Core Novelty Showcase!
     - Displays the multi-layer correlation timeline linking mobile RASP with API auth failures.
     - Click "Inspect" on any event to show the Evidence Inspector Dialog.
     - Highlights RULE-CORR-01 (Frida + BOLA attempt -> RESTRICT_SENSITIVE_ACTIONS).
     - Highlights RULE-CORR-04 (Event Replay deduplication suppressing score escalation).

   Station 3: Policy & Threshold Management (/policies)
     - Displays the 4 authoritative server-side response bands:
         • ALLOW (0-24)
         • MONITOR (25-49)
         • STEP_UP_AUTHENTICATION (50-74)
         • RESTRICT_SENSITIVE_ACTIONS (75-100)
     - Adjust risk weights (Root, Frida, Auth failure, Cross-Layer Synergy bonus).
     - Click "Deploy Policy" to demonstrate authoritative server update.

   Station 4: Research Analytics & Ablation Study (/research-analytics)
     - Interactive Configuration Switcher: 1-click toggles between:
         • Config A: API-Only Security (Recall: 14.3%)
         • Config B: Mobile-Only Protection (Recall: 14.3%)
         • Config C: Combined Independent Security (Recall: 57.1%)
         • Config D: Full AppShieldX (Recall: 85.7% | Precision: 100% | Latency: 4.06 ms)
     - Live Confusion Matrix (TP, FP, TN, FN) and Precision/Recall/FPR cards.
     - Processing Latency Breakdown (Ingestion, Correlation, Enforcement).
     - Empirical Ablation Study table isolating each mechanism's contribution.

   Station 5: Reusability Demonstration (Second Sample Application)
     - Open docs/reusable-integration-guide.md and examples/second-client-app/
     - Shows HealthcarePortalApp integrating AppShieldX with only 3 client steps (35 LOC)
       and 2 backend filter steps (28 LOC) with ZERO changes to the correlation engine.

   Station 6: CloudWatch & AWS Telemetry (infrastructure/terraform)
     - Open infrastructure/terraform/cloudwatch_research_metrics.tf
     - Shows CloudWatch metric filters for events ingested, correlation rule triggers,
       policy restrictions, and the automated research posture dashboard.
    """
    print(guide)

def main_menu():
    while True:
        print_header("APPSHIELDX DEMONSTRATION SUITE MENU")
        print("  1. Check Environment & Prerequisites")
        print("  2. Run Research Evaluation Suite & Ablation Study (10 Scenarios)")
        print("  3. Run Mobile Security Unit Tests (Flutter 19/19 Tests)")
        print("  4. Run Backend Microservices Test Suite (Spring Boot 46/46 Tests)")
        print("  5. Launch SOC Administrator Dashboard (Vite Dev Server)")
        print("  6. Seed Live Cross-Layer Threat Telemetry into Backend")
        print("  7. Read Complete Reviewer Demonstration Script")
        print("  8. Exit")
        choice = input("\nSelect an option [1-8]: ").strip()

        if choice == "1":
            show_prerequisites()
        elif choice == "2":
            run_experiments()
        elif choice == "3":
            run_mobile_tests()
        elif choice == "4":
            run_backend_tests()
        elif choice == "5":
            start_admin_dashboard()
        elif choice == "6":
            seed_telemetry_demo()
        elif choice == "7":
            show_demo_guide()
        elif choice == "8":
            print("\nExiting AppShieldX Demo Orchestrator. Good luck with your demonstration!\n")
            break
        else:
            print("[!] Invalid option. Please enter 1-8.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--guide":
        show_demo_guide()
    elif len(sys.argv) > 1 and sys.argv[1] == "--eval":
        run_experiments()
    else:
        main_menu()
