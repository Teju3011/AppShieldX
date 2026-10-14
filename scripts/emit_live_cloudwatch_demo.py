#!/usr/bin/env python3
import time
import json
import subprocess
from datetime import datetime, timezone

def emit_events(n_allow=5, n_block=3):
    region = "ap-south-1"
    stream_name = f"gateway-stream-{time.strftime('%Y-%m-%d')}"
    
    print(f"[*] Emitting live telemetry to CloudWatch in {region}...")
    print(f"    Log Stream: {stream_name}")

    # Ensure streams exist
    for lg in ["/aws/appshieldx/gateway-decisions", "/aws/appshieldx/threat-events"]:
        subprocess.run([
            "aws", "logs", "create-log-stream",
            "--log-group-name", lg,
            "--log-stream-name", stream_name,
            "--region", region
        ], capture_output=True)

    # 1. Gateway Decisions
    now_ms = int(time.time() * 1000)
    decision_events = []

    # Nominal Allow transactions
    for i in range(n_allow):
        t_ms = now_ms - (n_allow - i) * 10000
        iso_t = datetime.fromtimestamp(t_ms / 1000, tz=timezone.utc).isoformat()
        obj = {
            "timestamp": iso_t,
            "decision": "ALLOW",
            "httpStatus": 200,
            "policy": "NIST_SP_800_207_ZERO_TRUST",
            "riskScore": 12,
            "amountCommitted": 5000.0,
            "recipient": "alice@bank.vault",
            "attestation": "HARDWARE_KEYSTORE_ECDSA_VERIFIED",
            "latencyMs": 4.2
        }
        decision_events.append({"timestamp": t_ms, "message": json.dumps(obj)})

    # Attack Block transactions
    for i in range(n_block):
        t_ms = now_ms - (n_block - i) * 5000
        iso_t = datetime.fromtimestamp(t_ms / 1000, tz=timezone.utc).isoformat()
        obj = {
            "timestamp": iso_t,
            "decision": "RESTRICT_SENSITIVE_ACTIONS",
            "httpStatus": 403,
            "policy": "NIST_SP_800_207_ZERO_TRUST",
            "violation": "USB_DEBUGGING_ADB_ACTIVE",
            "commercialComparison": "HDFC and ICICI allow Skip; AppShieldX enforces non-bypassable HTTP 403",
            "riskScore": 85,
            "amountAttempted": 5000.0,
            "recipient": "alice@bank.vault",
            "latencyMs": 4.8
        }
        decision_events.append({"timestamp": t_ms, "message": json.dumps(obj)})

    # Sort strictly by timestamp
    decision_events.sort(key=lambda x: x["timestamp"])

    res1 = subprocess.run([
        "aws", "logs", "put-log-events",
        "--log-group-name", "/aws/appshieldx/gateway-decisions",
        "--log-stream-name", stream_name,
        "--log-events", json.dumps(decision_events),
        "--region", region
    ], capture_output=True, text=True)

    print("  [+] Gateway decisions push:", "SUCCESS" if res1.returncode == 0 else f"FAILED: {res1.stderr}")

    # 2. Threat Events
    threat_events = [
        {
            "timestamp": now_ms - 20000,
            "message": json.dumps({
                "timestamp": datetime.fromtimestamp((now_ms - 20000)/1000, tz=timezone.utc).isoformat(),
                "eventType": "DEVICE_INTEGRITY_SCAN",
                "deviceId": "motorola-edge-50-fusion",
                "indicators": {"usbDebuggingAdb": False, "rootIntegrity": False, "fridaMemoryHook": False},
                "compositeRiskScore": 12,
                "riskBand": "NOMINAL"
            })
        },
        {
            "timestamp": now_ms - 10000,
            "message": json.dumps({
                "timestamp": datetime.fromtimestamp((now_ms - 10000)/1000, tz=timezone.utc).isoformat(),
                "eventType": "USB_DEBUGGING_ATTACHED",
                "deviceId": "motorola-edge-50-fusion",
                "indicators": {"usbDebuggingAdb": True, "rootIntegrity": False, "fridaMemoryHook": False},
                "compositeRiskScore": 85,
                "riskBand": "RESTRICTED"
            })
        },
        {
            "timestamp": now_ms,
            "message": json.dumps({
                "timestamp": datetime.fromtimestamp(now_ms/1000, tz=timezone.utc).isoformat(),
                "eventType": "FRIDA_HOOK_INJECTION_ATTEMPT",
                "deviceId": "motorola-edge-50-fusion",
                "indicators": {"usbDebuggingAdb": True, "rootIntegrity": False, "fridaMemoryHook": True},
                "compositeRiskScore": 95,
                "riskBand": "CRITICAL"
            })
        }
    ]

    threat_events.sort(key=lambda x: x["timestamp"])

    res2 = subprocess.run([
        "aws", "logs", "put-log-events",
        "--log-group-name", "/aws/appshieldx/threat-events",
        "--log-stream-name", stream_name,
        "--log-events", json.dumps(threat_events),
        "--region", region
    ], capture_output=True, text=True)

    print("  [+] Threat events push:", "SUCCESS" if res2.returncode == 0 else f"FAILED: {res2.stderr}")
    print("[*] Completed real-time ingestion into AWS CloudWatch.")

if __name__ == "__main__":
    emit_events()
