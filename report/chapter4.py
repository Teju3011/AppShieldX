# -*- coding: utf-8 -*-
"""
Chapter 4: System Design Generator for AppShieldX Report
Target: ~18 pages of comprehensive architectural blueprints, native kernel RASP details,
gateway filters, correlation rules, mathematical risk scoring, ER schemas, and dashboard pipelines.
"""

import os
from report_helpers import (
    add_chapter_heading, add_sec_heading, add_subsec_heading, add_subsubsec_heading,
    add_para, add_bullet, add_fig, add_tbl, add_eq, add_code_block
)

def generate_chapter4(doc, figures_dir):
    add_chapter_heading(doc, 4, "System Design")

    # 4.1 ARCHITECTURAL OVERVIEW: SIX-TIER DISTRIBUTED FRAMEWORK
    add_sec_heading(doc, "4.1", "Architectural Overview: Six-Tier Distributed Framework")

    add_para(doc,
        "The AppShieldX framework is architected as an enterprise-grade, distributed, cloud-native security framework that establishes a continuous, bidirectional protection bridge between mobile client applications and cloud-hosted microservices. Rather than treating client protection and API security as isolated defensive disciplines, AppShieldX organizes defensive capabilities into six tightly integrated architectural tiers. Figure 4.1 illustrates the comprehensive six-tier system architecture, depicting the flow of user transactions, out-of-band security telemetry, and real-time policy feedback loops."
    )

    fig41_path = os.path.join(figures_dir, "figure4_1_system_architecture.png")
    add_fig(doc, fig41_path, 
            "Figure 4.1: AppShieldX Six-Tier Cloud-Native Architecture and Telemetry Processing Pipeline.")

    add_para(doc,
        "The structural responsibilities and boundary characteristics of each tier within the AppShieldX framework are systematically delineated as follows:"
    )

    tiers = [
        ("Tier 1: Mobile Client Presentation & Logic Layer",
         "Constructed using the cross-platform Flutter framework (Dart runtime), this tier hosts the end-user presentation interface and business application logic. It communicates with device operating system peripherals through native platform channels and manages secure local cryptographic key storage using platform-specific hardware-backed keystores (Android Keystore and iOS Keychain via EncryptedSharedPreferences)."),

        ("Tier 2: Client-Side Runtime Application Self-Protection (RASP) Engine",
         "Compiled as native Kotlin/Java Android code and native Swift/C iOS code, this tier operates directly within the application process address space. It executes low-level kernel inspections, querying Linux procfs (/proc) virtual files, inspecting process memory mappings, detecting superuser binaries, identifying emulator hypervisors, and verifying code signature invariants."),

        ("Tier 3: Cryptographic Transport & API Gateway Ingress Perimeter",
         "Serving as the single entry point for all external network ingress traffic, this tier combines Transport Layer Security (TLS 1.3) with Subject Public Key Info (SPKI) certificate pinning. Ingress routing is orchestrated by a high-throughput, non-blocking Spring Cloud Gateway equipped with a custom reactive ZeroTrustSecurityFilter that enforces dynamic access policies before forwarding requests to internal services."),

        ("Tier 4: Threat Detection, Telemetry Ingestion & Stateful Correlation Tier",
         "This tier operates within the secure cloud virtual network, housing an asynchronous telemetry ingestion endpoint and the core Stateful Threat Correlation Engine. It parses cryptographic telemetry payloads transmitted out-of-band by client RASP probes and matches them against synchronous API gateway transaction logs using six deterministic cross-layer security rules."),

        ("Tier 5: Persistence, State Synchronization & In-Memory Caching Tier",
         "The persistence layer combines relational database management via PostgreSQL 15 for immutable security audit logging, user credentials, and device asset tracking, alongside an ultra-low-latency Redis 7.x in-memory cache. Redis maintains active session tokens, distributed rate-limiting sliding windows, and real-time device risk scores accessible in sub-millisecond lookups."),

        ("Tier 6: Security Operations Center (SOC) Administration Dashboard",
         "Constructed with React 18, TypeScript, and modern responsive CSS, this tier delivers real-time visibility and threat analytics to security administrators. Connected to the backend via Server-Sent Events (SSE), it visualizes live attack streams, displays risk score heatmaps, provides detailed forensic payloads, and enables manual emergency device quarantines.")
    ]

    for t_name, t_desc in tiers:
        add_bullet(doc, t_desc, bold_prefix=f"{t_name}: ")

    # 4.2 CLIENT-SIDE SECURITY LAYER: KERNEL-LEVEL RASP ENGINE
    add_sec_heading(doc, "4.2", "Client-Side Security Layer: Kernel-Level RASP Engine")

    add_para(doc,
        "The client-side defense in AppShieldX is engineered to operate autonomously in hostile host environments without introducing perceptible user interface stutter or excessive battery consumption. To ensure absolute resistance against dynamic hooking toolkits that intercept high-level Java APIs, the RASP engine bypasses the standard Android framework classes (such as android.os.Debug) wherever possible, directly interrogating the underlying Linux kernel."
    )

    fig42_path = os.path.join(figures_dir, "figure4_2_rasp_kernel_probes.png")
    add_fig(doc, fig42_path, 
            "Figure 4.2: Native Android RASP Probe Execution Flowchart in Linux Kernel Space.")

    add_para(doc,
        "As depicted in the flowchart in Figure 4.2, the RASP probe execution sequence is triggered both at application launch and at periodic, randomized intervals (defaulting to every 10 seconds) during active user sessions. Table 4.1 catalogs the primary native kernel diagnostic probes implemented within the AppShieldX Android client engine."
    )

    # Table 4.1: RASP Probes Table
    t41_headers = ["Diagnostic Probe", "Target Kernel / OS Artifact", "Detection Mechanism & Algorithm", "Target Threat Vector"]
    t41_data = [
        ["Kernel Tracer Probe", "/proc/self/status", "Parses line starting with 'TracerPid:'. If integer value is non-zero, active ptrace debugger is detected.", "Live GDB, LLDB, and IDA Pro debugger attachment"],
        ["Root Binary Probe", "/system/bin/su, /system/xbin/su, /sbin/su", "Verifies physical file existence and tests executable permissions via standard POSIX stat() calls.", "Magisk, SuperSU, and KernelSU privilege escalation"],
        ["Mount Namespace Probe", "/proc/mounts, /system directory", "Attempts write operation on read-only mount points; checks for Magisk overlay mount markers.", "Root cloaking and mount namespace spoofing"],
        ["Hook Signature Probe", "/proc/self/maps", "Iterates virtual memory segment mappings; checks for strings 'frida-agent', 'xposed', or 'substrate'.", "Frida dynamic instrumentation and Xposed framework"],
        ["Debugger Port Probe", "TCP Ports 27042, 27043", "Attempts local socket connection to default Frida-server inspection listening ports.", "Remote dynamic debugging and instrumentation servers"],
        ["Hypervisor VM Probe", "Build.HARDWARE, Build.FINGERPRINT", "Evaluates system properties for 'goldfish', 'ranchu', 'qemu', 'vbox', or 'generic' strings.", "Virtualized QEMU emulators and automated bot farms"],
        ["Package Signature Probe", "PackageManager GET_SIGNING_CERTIFICATES", "Computes SHA-256 digest of signing certificate; compares against embedded cryptographic anchor.", "Application repacking, patching, and binary cracking"]
    ]
    add_tbl(doc, "Table 4.1: Core RASP Diagnostic Probes Implemented Across Native Kernel Channels.",
            t41_headers, t41_data, col_widths=[1.5, 1.5, 2.0, 1.5])

    add_subsec_heading(doc, "4.2.1", "Native MethodChannel Bridge Architecture")
    add_para(doc,
        "To connect the native Android RASP engine with the cross-platform Flutter presentation layer, AppShieldX implements a dedicated, bidirectional MethodChannel named 'com.appshieldx/security_channel'. When the Flutter application boots, the Dart SecurityManager invokes the native getSecurityDiagnostics method. The native Kotlin layer executes the full diagnostic suite asynchronously on a dedicated background thread pool, preventing any frame drops on the main UI thread. Listing 4.1 provides an extract of the native kernel diagnostic implementation."
    )

    code_rasp = """
// Native Kotlin Android Kernel Diagnostic Probe Implementation
fun performKernelSecurityAudit(): SecurityDiagnostics {
    var tracerPid = 0
    var debuggerAttached = false
    try {
        val statusFile = File("/proc/self/status")
        if (statusFile.exists()) {
            statusFile.forEachLine { line ->
                if (line.startsWith("TracerPid:")) {
                    tracerPid = line.substring(10).trim().toIntOrNull() ?: 0
                    if (tracerPid > 0) debuggerAttached = true
                }
            }
        }
    } catch (e: Exception) { /* Handle procfs access restriction */ }

    val rootPaths = arrayOf("/system/bin/su", "/system/xbin/su", "/sbin/su", "/system/app/Superuser.apk")
    val isRooted = rootPaths.any { File(it).exists() } || Build.TAGS?.contains("test-keys") == true

    var hookDetected = false
    try {
        val mapsFile = File("/proc/self/maps")
        if (mapsFile.exists()) {
            mapsFile.forEachLine { line ->
                if (line.contains("frida-agent") || line.contains("xposed") || line.contains("substrate")) {
                    hookDetected = true
                }
            }
        }
    } catch (e: Exception) { }

    val isEmulator = Build.FINGERPRINT.startsWith("generic") || Build.MODEL.contains("google_sdk") ||
                     Build.HARDWARE.contains("goldfish") || Build.HARDWARE.contains("ranchu")

    return SecurityDiagnostics(isRooted, debuggerAttached, tracerPid, hookDetected, isEmulator)
}
"""
    add_code_block(doc, code_rasp, "Listing 4.1: Native Kotlin Implementation of Kernel-Level Security Diagnostic Probes.")

    # 4.3 SECURE COMMUNICATION LAYER: TLS 1.3 AND PINNING
    add_sec_heading(doc, "4.3", "Secure Communication Layer: TLS 1.3 and Pinning")

    add_para(doc,
        "Network communication between the mobile client and the cloud API gateway is fortified using Transport Layer Security (TLS 1.3, RFC 8446) coupled with rigorous public key certificate pinning. In conventional mobile applications, the operating system's default network stack trusts any Certificate Authority (CA) installed in the system or user trust store. This design is highly vulnerable to Man-in-the-Middle (MITM) attacks: an attacker can install a malicious root CA certificate onto the device (via Magisk modules or user installation) and decrypt, inspect, and modify all HTTPS traffic using proxies such as Burp Suite."
    )

    add_para(doc,
        "AppShieldX eliminates this vulnerability by enforcing Subject Public Key Info (SPKI) certificate pinning within the client HTTP client. During cryptographic connection establishment, the client extracts the SHA-256 digest of the server's public key certificate and compares it against hardcoded, cryptographically anchored public key hashes. Even if an attacker successfully forces the operating system to accept a counterfeit root CA, the TLS handshake terminates immediately with a certificate validation exception, completely thwarting cleartext interception."
    )

    add_para(doc,
        "Furthermore, to protect out-of-band security telemetry transmitted from the client to the cloud backend (/api/v1/telemetry/report), AppShieldX introduces an additional cryptographic attestation envelope. Every telemetry payload is serialized into a canonical JSON representation and digitally signed using a keyed Hash-based Message Authentication Code (HMAC-SHA256) using a unique per-device shared secret established during initial enrollment. The payload includes a monotonic sequence counter and a millisecond-precision timestamp to prevent replay attacks."
    )

    # 4.4 CLOUD INGRESS AND API GATEWAY: ZEROTRUSTSECURITYFILTER
    add_sec_heading(doc, "4.4", "Cloud Ingress and API Gateway: ZeroTrustSecurityFilter")

    add_para(doc,
        "The cloud ingress perimeter of AppShieldX is anchored by Spring Cloud Gateway, a modern, non-blocking, asynchronous reverse proxy built on Project Reactor and Netty. To eliminate the performance bottlenecks documented by Gomez et al. [18] in synchronous gateways, AppShieldX implements a custom reactive GlobalFilter designated as the ZeroTrustSecurityFilter."
    )

    add_para(doc,
        "When an incoming HTTP request arrives at the gateway, the ZeroTrustSecurityFilter intercepts the exchange before routing it to downstream microservices. The filter executes four sequential, asynchronous validation phases:"
    )

    add_bullet(doc, "Header & Token Extraction: Extracts the Authorization Bearer JWT token, the unique client device identifier (X-Device-Id), and request metadata. Unauthenticated requests targeting protected endpoints are immediately rejected with HTTP 401 Unauthorized.", bold_prefix="Phase 1: ")
    add_bullet(doc, "Distributed Token & Claim Verification: Validates the cryptographic RSA/ECDSA signature of the JWT against the identity provider's public key, checks expiration timestamps (exp claim), and parses the user role (role claim).", bold_prefix="Phase 2: ")
    add_bullet(doc, "Redis Distributed Rate Limiting: Queries the Redis in-memory cache to evaluate the request frequency against a sliding window rate-limiting algorithm. High-velocity bursts exceeding threshold limits are throttled with HTTP 429 Too Many Requests.", bold_prefix="Phase 3: ")
    add_bullet(doc, "Real-Time Device Integrity Attestation: Executes an asynchronous, non-blocking Redis lookup for the device identifier X-Device-Id to retrieve the device's real-time dynamic risk score and active response band. If the device is marked as TERMINATED or QUARANTINED, the request is blocked immediately with HTTP 403 Forbidden.", bold_prefix="Phase 4: ")

    code_gateway = """
// Spring Cloud Gateway Reactive ZeroTrustSecurityFilter Extract
@Component
public class ZeroTrustSecurityFilter implements GlobalFilter, Ordered {
    @Autowired private ReactiveRedisTemplate<String, String> redisTemplate;
    @Autowired private JwtTokenValidator jwtValidator;

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        ServerHttpRequest request = exchange.getRequest();
        String path = request.getPath().value();
        if (isPublicEndpoint(path)) return chain.filter(exchange);

        String authHeader = request.getHeaders().getFirst("Authorization");
        String deviceId = request.getHeaders().getFirst("X-Device-Id");

        if (authHeader == null || !authHeader.startsWith("Bearer ") || deviceId == null) {
            exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
            return exchange.getResponse().setComplete();
        }

        String token = authHeader.substring(7);
        Claims claims = jwtValidator.validateAndExtractClaims(token);
        if (claims == null) {
            exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
            return exchange.getResponse().setComplete();
        }

        // Asynchronous Redis lookup for real-time device risk band
        return redisTemplate.opsForValue().get("risk:device:" + deviceId)
            .defaultIfEmpty("0.0")
            .flatMap(scoreStr -> {
                double riskScore = Double.parseDouble(scoreStr);
                if (riskScore >= 75.0) { // TERMINATE Band
                    exchange.getResponse().setStatusCode(HttpStatus.FORBIDDEN);
                    return exchange.getResponse().setComplete();
                } else if (riskScore >= 50.0 && isMutationMethod(request.getMethod())) { // RESTRICT Band
                    exchange.getResponse().setStatusCode(HttpStatus.FORBIDDEN);
                    return exchange.getResponse().setComplete();
                }
                // Forward request downstream with enriched security headers
                ServerHttpRequest mutatedRequest = request.mutate()
                    .header("X-Security-Risk-Score", String.valueOf(riskScore))
                    .build();
                return chain.filter(exchange.mutate().request(mutatedRequest).build());
            });
    }
}
"""
    add_code_block(doc, code_gateway, "Listing 4.2: Spring Cloud Gateway Reactive ZeroTrustSecurityFilter Implementation.")

    # 4.5 THREAT DETECTION AND STATEFUL EVENT CORRELATION ENGINE
    add_sec_heading(doc, "4.5", "Threat Detection and Stateful Event Correlation Engine")

    add_para(doc,
        "The scientific core of the AppShieldX framework is the Stateful Threat Correlation Engine. Rather than treating client RASP telemetry alerts and server API anomalies as disjointed data points, the correlation engine aggregates these heterogeneous event streams across a shared temporal sliding window (W = 30 seconds). By cross-referencing client endpoint diagnostics with server API transaction logs, AppShieldX evaluates threat state transitions against a deterministic finite state machine, as depicted in Figure 4.4."
    )

    fig44_path = os.path.join(figures_dir, "figure4_4_correlation_state_machine.png")
    add_fig(doc, fig44_path, 
            "Figure 4.4: Deterministic Threat Correlation State Machine Workflow (RULE-CORR-01 to 06).")

    add_para(doc,
        "The correlation engine is governed by six formal deterministic correlation rules (RULE-CORR-01 through RULE-CORR-06). Each rule defines a specific multi-condition trigger pattern, calculates a compounded risk score increment, and specifies an immediate adaptive enforcement action. Table 4.2 presents the formal specifications of all six correlation rules."
    )

    # Table 4.2: Correlation Rules Table
    t42_headers = ["Rule ID", "Rule Name", "Cross-Layer Trigger Conditions", "Risk Score Delta", "Enforcement Action"]
    t42_data = [
        ["RULE-CORR-01", "Dynamic Hooking & API Abuse", "Client reports Frida/Xposed hooks present AND gateway detects > 10 req/sec on business endpoints", "+50 points (Score -> 75)", "Immediate session quarantine, revoke active JWT, HTTP 403"],
        ["RULE-CORR-02", "Debugger & Token Exfiltration", "Client reports TracerPid > 0 AND token is used from external or non-matching IP subnet", "+45 points (Score -> 70)", "Require Step-Up MFA authentication, freeze sensitive wire transfers"],
        ["RULE-CORR-03", "Root Escalation & Admin Probe", "Client reports su binary detected AND request attempts admin endpoint (/api/v1/admin/*)", "+60 points (Score -> 85)", "Immediate account freeze, invalidate session, log SOC critical alert"],
        ["RULE-CORR-04", "Virtualization & Burst Attack", "Client reports QEMU/emulator detected AND gateway detects registration/login velocity > 5/min", "+40 points (Score -> 60)", "Enforce CAPTCHA step-up verification, rate-limit device to 0.2 req/sec"],
        ["RULE-CORR-05", "Telemetry Heartbeat Evasion", "Device issues high-value API request while telemetry heartbeat is missing (> 60s silence)", "+35 points (Score -> 50)", "Downgrade session to RESTRICT (read-only mode), request heartbeat sync"],
        ["RULE-CORR-06", "Memory Tamper & BOLA Abuse", "Client reports package hash mismatch AND request modifies resource ID (BOLA / IDOR pattern)", "+75 points (Score -> 95)", "Permanent device blacklist, immediate connection termination (HTTP 403)"]
    ]
    add_tbl(doc, "Table 4.2: AppShieldX Deterministic Cross-Layer Correlation Rule Definitions (RULE-CORR-01 to 06).",
            t42_headers, t42_data, col_widths=[1.3, 1.6, 2.0, 1.2, 1.4])

    # 4.6 SERVER-SIDE DYNAMIC RISK SCORING ENGINE AND DECAY MECHANICS
    add_sec_heading(doc, "4.6", "Server-Side Dynamic Risk Scoring Engine and Decay Mechanics")

    add_para(doc,
        "To provide nuanced, adaptive protection that avoids the disruptive false-positive penalties of rigid binary defenses, AppShieldX introduces a dynamic, continuous risk-scoring model. Every registered client device d is assigned a continuous risk score R_t in [0, 100]. When security anomalies are correlated, the score increases proportionally to the severity weight of the violated rules. Simultaneously, in the absence of subsequent hostile activity, the risk score decays exponentially over time toward a baseline trusted state."
    )

    fig43_path = os.path.join(figures_dir, "figure4_3_risk_scoring_bands.png")
    add_fig(doc, fig43_path, 
            "Figure 4.3: Server-Side Zero-Trust Adaptive Response Bands and Temporal Score Decay Curve.")

    add_subsec_heading(doc, "4.6.1", "Mathematical Risk Formulation and Exponential Temporal Decay")
    add_para(doc,
        "When an anomalous security event e_i is correlated at time t_i, the instantaneous risk score is updated by accumulating the severity weights w_i of all active threat indicators:"
    )

    add_eq(doc, "R_raw(t) = R(t^-) + Σ_i (w_i · I_i(t))", "4.1")

    add_para(doc,
        "where I_i(t) in {0, 1} is an indicator variable denoting the triggering of correlation rule i, and w_i is the severity weight assigned in Table 4.3. The raw score is bounded within the closed interval [0, 100]:"
    )

    add_eq(doc, "R(t) = min(100.0, max(0.0, R_raw(t)))", "4.2")

    add_para(doc,
        "To prevent transient, benign anomalies (such as a temporary USB debugging connection during authorized testing) from permanently penalizing legitimate users, AppShieldX applies an exponential temporal decay function. Between consecutive transaction epochs, the risk score decays according to:"
    )

    add_eq(doc, "R(t + Δt) = R(t) · e^(-λ · Δt)", "4.3")

    add_para(doc,
        "where Δt is the elapsed time in minutes since the last recorded anomaly, and λ is the decay constant calibrated to a configurable half-life t_{1/2} (established empirically at 15 minutes, or 900 seconds):"
    )

    add_eq(doc, "λ = ln(2) / t_{1/2} = 0.69315 / 15 ≈ 0.04621 min^-1", "4.4")

    # Table 4.3: Threat Severity Weights Table
    t43_headers = ["Threat Category", "Associated Severity Weight (w_i)", "Mathematical Decay Half-Life", "Clinical Risk Impact"]
    t43_data = [
        ["Active Frida Hook / Injection", "w = 50.0 points", "t_1/2 = 15 minutes", "Critical: Immediate risk of runtime method tampering and secret theft"],
        ["Kernel TracerPid != 0 (Debugger)", "w = 45.0 points", "t_1/2 = 15 minutes", "High: Active process halting, memory inspection, and reverse engineering"],
        ["Root / Superuser Binary Found", "w = 40.0 points", "t_1/2 = 15 minutes", "High: Complete loss of local operating system sandbox guarantees"],
        ["Emulator / Virtual Machine", "w = 30.0 points", "t_1/2 = 15 minutes", "Medium: Potential automated bot farm, mass credential testing, or fraud"],
        ["Rate Limit Burst Violation", "w = 25.0 points", "t_1/2 = 10 minutes", "Medium: Denial of service or brute-force credential stuffing attempt"],
        ["Missing Telemetry Heartbeat", "w = 20.0 points", "t_1/2 = 10 minutes", "Low-Medium: Unverified client execution state or network interference"],
        ["Package Certificate Mismatch", "w = 60.0 points", "t_1/2 = 30 minutes", "Critical: Repackaged, cracked, or pirated application binary"]
    ]
    add_tbl(doc, "Table 4.3: Threat Severity Weight Matrix and Mathematical Score Calculations.",
            t43_headers, t43_data, col_widths=[1.8, 1.6, 1.4, 2.2])

    add_subsec_heading(doc, "4.6.2", "Server-Side Zero-Trust Adaptive Response Bands")
    add_para(doc,
        "Based on the instantaneous risk score R_t, the ingress gateway classifies the client session into one of four distinct Zero-Trust policy bands, as formalized in Table 4.4:"
    )

    # Table 4.4: Response Bands Table
    t44_headers = ["Risk Band", "Risk Score Range", "Session Trust Classification", "Automated Gateway Enforcement Policy Action"]
    t44_data = [
        ["Band 1: ALLOW", "0 <= R_t < 25", "Trusted / Healthy", "Permit all standard API requests unconditionally. Log standard access metrics."],
        ["Band 2: STEP_UP", "25 <= R_t < 50", "Suspicious / Elevated", "Require Step-Up Multi-Factor Authentication (MFA) on sensitive endpoints. Challenge device with biometric verification."],
        ["Band 3: RESTRICT", "50 <= R_t < 75", "High Risk / Compromised", "Enforce read-only mode. Completely block state-mutating requests (POST, PUT, DELETE, transfers). Return HTTP 403 on write attempts."],
        ["Band 4: TERMINATE", "75 <= R_t <= 100", "Critical Threat / Malicious", "Immediately revoke active JWT tokens, purge Redis session cache, return HTTP 403 Forbidden on all requests, trigger SOC incident."]
    ]
    add_tbl(doc, "Table 4.4: Server-Side Zero-Trust Adaptive Response Bands and Policy Actions.",
            t44_headers, t44_data, col_widths=[1.4, 1.3, 1.6, 2.7])

    # 4.7 PERSISTENCE AND SHARED CACHING ARCHITECTURE
    add_sec_heading(doc, "4.7", "Persistence and Shared Caching Architecture")

    add_para(doc,
        "To support both high-throughput in-line gateway decision making and long-term historical forensic auditing, AppShieldX implements a dual-tier persistence architecture. Figure 4.5 displays the Entity-Relationship (ER) schema governing relational data modeling in PostgreSQL, while Table 4.5 details the schema table structures."
    )

    fig45_path = os.path.join(figures_dir, "figure4_5_database_schema_er.png")
    add_fig(doc, fig45_path, 
            "Figure 4.5: Relational Database Schema Entity-Relationship (ER) Diagram.")

    # Table 4.5: Database Schema Table
    t45_headers = ["Database Table", "Primary Key", "Foreign Keys", "Core Stored Attributes & Indexing Strategy"]
    t45_data = [
        ["users", "id (UUID)", "None", "username, email, password_hash (BCrypt), role (ADMIN/USER), mfa_enabled, created_at. Indexed on username, email."],
        ["devices", "device_id (VARCHAR)", "user_id -> users(id)", "platform (ANDROID/IOS), os_version, device_model, app_version, enrollment_date, last_seen. Indexed on device_id."],
        ["security_events", "event_id (UUID)", "device_id -> devices(device_id)", "event_type, severity, raw_payload (JSONB), source_ip, tracer_pid, is_rooted, timestamp. Indexed on device_id, timestamp."],
        ["risk_assessments", "assessment_id (UUID)", "device_id -> devices(device_id)", "current_score (DOUBLE), response_band (VARCHAR), decay_half_life, last_evaluated. Indexed on device_id (Unique)."],
        ["audit_logs", "log_id (UUID)", "None", "actor_id, action_type, target_resource, response_status, execution_latency_ms, created_at. Partitioned by created_at month."]
    ]
    add_tbl(doc, "Table 4.5: Relational Database Schema Table Specifications and Indexing Strategy.",
            t45_headers, t45_data, col_widths=[1.5, 1.3, 1.5, 2.7])

    # 4.8 SECURITY OPERATIONS CENTER (SOC) ADMINISTRATOR DASHBOARD
    add_sec_heading(doc, "4.8", "Security Operations Center (SOC) Administrator Dashboard")

    add_para(doc,
        "Enterprise incident response requires rapid, intuitive threat triage. AppShieldX provides an administrative web application designed specifically for Security Operations Center (SOC) analysts. As shown in Figure 4.6, the dashboard connects to the cloud backend via a high-performance Server-Sent Events (SSE) stream (/api/v1/telemetry/stream)."
    )

    fig46_path = os.path.join(figures_dir, "figure4_6_dashboard_architecture.png")
    add_fig(doc, fig46_path, 
            "Figure 4.6: SOC Administrator Dashboard Live Telemetry and Threat Intelligence Architecture.")

    add_para(doc,
        "The dashboard frontend is implemented in React 18 and TypeScript, featuring a dark-themed, glassmorphic cybersecurity aesthetic. It provides four specialized analyst views: (1) Live Incident Triage Stream, displaying incoming security alerts in real time with millisecond timestamps, device fingerprints, and rule triggers; (2) Fleet Risk Score Distribution, displaying interactive charts of device population across the four response bands; (3) Threat Vector Analytics, displaying historical breakdowns of detected attacks; and (4) Device Management & Quarantine Console, allowing analysts to manually blacklist rogue devices or reset false-positive penalty scores with a single click."
    )

    # 4.9 DUAL-DOMAIN REFERENCE CLIENT APPLICATIONS
    add_sec_heading(doc, "4.9", "Dual-Domain Reference Client Applications")

    add_para(doc,
        "To empirically demonstrate that AppShieldX is a generic, reusable framework capable of protecting distinct enterprise business domains, two complete reference mobile client applications were implemented and evaluated, as illustrated in Figure 4.7."
    )

    fig47_path = os.path.join(figures_dir, "figure4_7_dual_client_apps.png")
    add_fig(doc, fig47_path, 
            "Figure 4.7: Dual-Domain Reference Client Applications (Banking Vault & Healthcare EHR Portal).")

    add_subsec_heading(doc, "4.9.1", "Domain A: FinTech Banking Vault Application")
    add_para(doc,
        "The Banking Vault application simulates a high-assurance consumer banking client. It exposes sensitive financial endpoints, including account balance retrieval (/api/v1/banking/accounts), wire transfers (/api/v1/banking/transfer), and beneficiary management. The application enforces zero tolerance for root elevation and dynamic hook injection: any detected debugger attachment or Frida hook immediately freezes the transaction UI and triggers a STEP_UP or TERMINATE enforcement signal at the gateway."
    )

    add_subsec_heading(doc, "4.9.2", "Domain B: Healthcare EHR Portal Application")
    add_para(doc,
        "The Healthcare EHR application simulates a clinical portal managing Protected Health Information (PHI) compliant with the Health Insurance Portability and Accountability Act (HIPAA). It interfaces with endpoints including patient medical records (/api/v1/ehr/patients/{id}), electronic prescription issuance, and clinical audit logs. The application is configured to validate object-level authorization strictly, demonstrating AppShieldX's ability to correlate parameter tampering and BOLA attacks against live device integrity states."
    )

    print("Chapter 4 generated successfully.")
