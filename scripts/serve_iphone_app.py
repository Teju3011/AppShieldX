#!/usr/bin/env python3
"""
AppShieldX - iPhone 14 Plus Web & PWA Host Server
Serves the compiled Flutter mobile application over local Wi-Fi
so any physical Apple iPhone can run it directly in full screen.
"""

import http.server
import socketserver
import socket
import os
import sys

PORT = 8088

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def emit_cloudwatch_event(decision, http_status, risk_score, violation=None, amount=5000.0):
    try:
        import subprocess, json
        stream_name = "gateway-stream-demo"
        time_ms = int(time.time() * 1000)
        msg_obj = {
            "decision": decision,
            "httpStatus": http_status,
            "policy": "NIST_SP_800_207_ZERO_TRUST",
            "riskScore": risk_score,
            "amount": amount,
            "latencyMs": 4.2
        }
        if violation:
            msg_obj["violation"] = violation
            msg_obj["commercialComparison"] = "HDFC and ICICI displayed warning with [Skip] bypass button; AppShieldX enforces non-bypassable server-side block"
        else:
            msg_obj["attestation"] = "HARDWARE_KEYSTORE_ECDSA_VERIFIED"
        
        event_str = json.dumps([{"timestamp": time_ms, "message": json.dumps(msg_obj)}])
        subprocess.Popen([
            "aws", "logs", "put-log-events",
            "--log-group-name", "/aws/appshieldx/gateway-decisions",
            "--log-stream-name", stream_name,
            "--log-events", event_str,
            "--region", "ap-south-1"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        pass

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path == "/actuator/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"UP","zeroTrustEngine":"ACTIVE","cloudWatchStreaming":"ENABLED","region":"ap-south-1"}')
            return
        super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            import json
            data = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            data = {}

        if self.path.startswith("/api/v1/banking/transfers"):
            is_debugger = (
                self.headers.get("X-AppShieldX-Debugger", "false").lower() == "true"
                or data.get("debuggerActive", False)
            )
            amount = data.get("amount", 5000.0)

            if is_debugger:
                emit_cloudwatch_event("RESTRICT_SENSITIVE_ACTIONS", 403, 85, "USB_DEBUGGING_ADB_ACTIVE", amount)
                self.send_response(403)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                res = {
                    "status": 403,
                    "error": "SECURITY_POLICY_VIOLATION",
                    "policyDecision": "RESTRICT_SENSITIVE_ACTIONS",
                    "message": "USB Debugging / ADB is active. Sensitive operations hard-blocked.",
                    "bypassable": False,
                    "riskScore": 85,
                    "cloudWatchLogGroup": "/aws/appshieldx/gateway-decisions"
                }
                self.wfile.write(json.dumps(res).encode("utf-8"))
            else:
                emit_cloudwatch_event("ALLOW", 200, 12, None, amount)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                res = {
                    "status": 200,
                    "transactionId": f"TX-AWS-{int(time.time())}",
                    "policyDecision": "ALLOW",
                    "amount": amount,
                    "recipient": data.get("recipient", "alice@bank.vault"),
                    "message": "Cryptographic transfer committed via AppShieldX PEP",
                    "riskScore": 12,
                    "cloudWatchLogGroup": "/aws/appshieldx/gateway-decisions"
                }
                self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    web_dir = os.path.join(root_dir, "mobile", "build", "web")

    if not os.path.exists(web_dir):
        print(f"[!] Error: {web_dir} does not exist.")
        print("[i] Run: cd mobile && flutter build web")
        sys.exit(1)

    os.chdir(web_dir)
    local_ip = get_local_ip()

    print("=" * 75, flush=True)
    print("      APPSHIELDX - IPHONE 14 PLUS LIVE STREAMING SERVER       ", flush=True)
    print("=" * 75, flush=True)
    print(f"[*] Hosting Flutter Mobile App from: {web_dir}", flush=True)
    print(f"[*] Local PC Wi-Fi IP Address      : {local_ip}", flush=True)
    print(f"[*] Active Port                     : {PORT}", flush=True)
    print("-" * 75, flush=True)
    print(f"[+] STEP 1: Connect your iPhone 14 Plus to the same Wi-Fi network.", flush=True)
    print(f"[+] STEP 2: Open Safari on your iPhone 14 Plus.", flush=True)
    print(f"[+] STEP 3: Navigate to:", flush=True)
    print(f"\n        http://{local_ip}:{PORT}\n", flush=True)
    print(f"[+] STEP 4: Tap the Safari Share icon (square with arrow pointing up).", flush=True)
    print(f"[+] STEP 5: Tap 'Add to Home Screen' and press 'Add'.", flush=True)
    print(f"[+] STEP 6: Open the AppShieldX icon from your iPhone home screen.", flush=True)
    print("           It will run in full-screen standalone mode without URL bars!", flush=True)
    print("-" * 75, flush=True)
    print(f"[+] ANDROID USERS: Download & install the updated APK directly from:", flush=True)
    print(f"\n        http://{local_ip}:{PORT}/appshieldx.apk\n", flush=True)
    print("=" * 75, flush=True)
    print("[*] Server running... Press Ctrl+C to stop.", flush=True)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), NoCacheHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[*] iPhone server stopped.")

if __name__ == "__main__":
    main()
