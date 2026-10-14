#!/usr/bin/env python3
"""
================================================================================
AppShieldX — Threat Telemetry & Cross-Layer Correlation Seeding Utility
================================================================================
Simulates realistic RASP security incidents from mobile devices (Android & iOS)
and backend API events, dispatching them to the Threat Detection Service
via the API Gateway or direct service port.
Populates live SOC dashboard feeds, correlation timeline, and risk metrics.
================================================================================
"""

import time
import json
import uuid
from datetime import datetime, timezone
import urllib.request
import urllib.error

# Primary Gateway URL with direct fallback
GATEWAY_URL = "http://localhost:8080/api/security"
DIRECT_URL = "http://localhost:8084/api/security"

COMMON_EVENTS = [
    {
        "eventId": str(uuid.uuid4()),
        "eventTimestamp": datetime.now(timezone.utc).isoformat(),
        "platform": "ANDROID",
        "appVersion": "1.0.0",
        "eventType": "FRIDA_ATTACHED",
        "severity": "HIGH",
        "confidence": 0.95,
        "authenticatedUserReference": "user-uuid-1122-3344",
        "verifiedSessionReference": "session-jwt-live-demo-101",
        "registeredDeviceReference": "android-pixel8-secure-001",
        "correlationId": str(uuid.uuid4()),
        "endpointCategory": "MOBILE_RASP",
        "detectionReason": "Frida gadget and dlsym hooking observed in memory",
        "evidenceSource": "CLIENT_TELEMETRY",
        "verificationStatus": "SERVER_VERIFIED",
        "details": "Frida default port 27042 open and loaded symbols modified"
    },
    {
        "eventId": str(uuid.uuid4()),
        "eventTimestamp": datetime.now(timezone.utc).isoformat(),
        "platform": "API_GATEWAY",
        "appVersion": "1.0.0",
        "eventType": "AUTHZ_DENIED",
        "severity": "HIGH",
        "confidence": 1.0,
        "authenticatedUserReference": "user-uuid-1122-3344",
        "verifiedSessionReference": "session-jwt-live-demo-101",
        "registeredDeviceReference": "android-pixel8-secure-001",
        "correlationId": str(uuid.uuid4()),
        "endpointCategory": "BUSINESS_TX",
        "detectionReason": "Unauthorized cross-tenant resource modification on /api/business/records",
        "evidenceSource": "GATEWAY_FILTER",
        "verificationStatus": "SERVER_VERIFIED",
        "details": "User attempted state modification on resource belonging to another tenant"
    },
    {
        "eventId": str(uuid.uuid4()),
        "eventTimestamp": datetime.now(timezone.utc).isoformat(),
        "platform": "IOS",
        "appVersion": "1.0.0",
        "eventType": "JAILBREAK_DETECTED",
        "severity": "CRITICAL",
        "confidence": 0.98,
        "authenticatedUserReference": "user-uuid-9988-7766",
        "verifiedSessionReference": "session-jwt-ios-demo-202",
        "registeredDeviceReference": "ios-iphone15-jb-003",
        "correlationId": str(uuid.uuid4()),
        "endpointCategory": "MOBILE_RASP",
        "detectionReason": "Dopamine jailbreak sandbox fork permitted and Cydia strings detected",
        "evidenceSource": "CLIENT_TELEMETRY",
        "verificationStatus": "SERVER_VERIFIED",
        "details": "Sandbox integrity compromised; root privileges accessible"
    },
    {
        "eventId": str(uuid.uuid4()),
        "eventTimestamp": datetime.now(timezone.utc).isoformat(),
        "platform": "ANDROID",
        "appVersion": "1.0.0",
        "eventType": "DEVELOPER_OPTIONS_ENABLED",
        "severity": "LOW",
        "confidence": 0.40,
        "authenticatedUserReference": "user-uuid-5544-3322",
        "verifiedSessionReference": "session-jwt-benign-303",
        "registeredDeviceReference": "android-samsung24-clean-002",
        "correlationId": str(uuid.uuid4()),
        "endpointCategory": "MOBILE_RASP",
        "detectionReason": "ADB debugging options toggled by developer",
        "evidenceSource": "CLIENT_TELEMETRY",
        "verificationStatus": "UNVERIFIED_CLIENT",
        "details": "Non-critical developer environment flag observed"
    }
]

def check_endpoint():
    for base in [GATEWAY_URL, DIRECT_URL]:
        try:
            req = urllib.request.Request(f"{base}/threats/summary")
            with urllib.request.urlopen(req, timeout=2) as resp:
                if resp.status == 200:
                    return base
        except Exception:
            continue
    return None

def seed_telemetry():
    print("=" * 80)
    print("  APPSHIELDX TELEMETRY & CROSS-LAYER CORRELATION SEEDER")
    print("=" * 80)

    target_base = check_endpoint()
    if not target_base:
        print("[!] Backend threat service is not currently listening on :8080 or :8084.")
        print("[i] To start backend microservices, run:")
        print("      docker-compose up -d")
        print("    OR start threat-detection-service locally with:")
        print("      mvn spring-boot:run -pl threat-detection-service")
        print("\n[*] Seed telemetry records ready for dispatch once backend is active.")
        return False

    print(f"[*] Target Endpoint Active: {target_base}")
    success_count = 0

    for event in COMMON_EVENTS:
        data = json.dumps(event).encode('utf-8')
        req = urllib.request.Request(
            f"{target_base}/events/common",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status in [200, 201]:
                    res_body = json.loads(resp.read().decode('utf-8'))
                    print(f"  [+] Ingested {event['eventType']} [{event['platform']}] -> "
                          f"Rule: {res_body.get('correlationRuleId')} | "
                          f"Risk: {res_body.get('riskScoreBefore')} -> {res_body.get('riskScoreAfter')} | "
                          f"Action: {res_body.get('finalEnforcedAction')}")
                    success_count += 1
                else:
                    print(f"  [-] Unexpected status {resp.status} for {event['eventType']}")
        except urllib.error.URLError as e:
            print(f"  [!] Failed dispatching {event['eventType']}: {e}")

    print(f"\n[*] Seeding completed: {success_count}/{len(COMMON_EVENTS)} cross-layer events ingested.")
    return True

if __name__ == "__main__":
    seed_telemetry()
