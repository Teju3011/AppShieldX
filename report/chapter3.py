# -*- coding: utf-8 -*-
"""
Chapter 3: Problem Statement and Methodology Generator for AppShieldX Report
Target: ~8 pages of rigorous mathematical problem definition, threat modeling (MITRE ATT&CK Mobile),
DFD Level 1 trust boundaries, cross-layer hypotheses, and evaluation methodology.
"""

import os
from report_helpers import (
    add_chapter_heading, add_sec_heading, add_subsec_heading,
    add_para, add_bullet, add_fig, add_tbl, add_eq
)

def generate_chapter3(doc, figures_dir):
    add_chapter_heading(doc, 3, "Problem Statement and Methodology")

    # 3.1 FORMAL PROBLEM DEFINITION AND MATHEMATICAL FORMULATION
    add_sec_heading(doc, "3.1", "Formal Problem Definition and Mathematical Formulation")

    add_para(doc,
        "To establish a mathematically rigorous foundation for cross-layer mobile-cloud security, we formally formulate the problem of Continuous Endpoint Attestation and Adaptive Threat Correlation in distributed client-server ecosystems. Let a mobile computing session be defined over a discrete time horizon t in {1, 2, ..., T}. At any given epoch t, the client execution state is represented by an m-dimensional binary and continuous state vector Psi_t in R^m:"
    )

    add_eq(doc, "Ψ_t = [x_debug(t), x_root(t), x_frida(t), x_emul(t), x_integrity(t), τ_heartbeat(t)]^T", "3.1")

    add_para(doc,
        "where x_debug(t) in {0, 1} indicates active kernel ptrace debugging attachment, x_root(t) in {0, 1} denotes the presence of superuser management binaries and privileged execution capabilities, x_frida(t) in {0, 1} flags the detection of dynamic binary instrumentation hooks within /proc/self/maps, x_emul(t) in {0, 1} captures hardware virtualization and hypervisor artifacts, x_integrity(t) in [0, 1] measures the cryptographic hash integrity of the running application package, and τ_heartbeat(t) denotes the elapsed time since the last verified telemetry heartbeat."
    )

    add_para(doc,
        "Simultaneously, the cloud backend ingress gateway processes a stream of synchronous HTTP/REST API transactions. Each incoming transaction request r_k arriving at time t_k is characterized by an n-dimensional feature tuple Φ_k in R^n:"
    )

    add_eq(doc, "Φ_k = [u_k, d_k, e_k, m_k, ν_k, α_k, Δt_k]^T", "3.2")

    add_para(doc,
        "where u_k denotes the authenticated user identifier extracted from the JWT token, d_k represents the cryptographic device fingerprint, e_k indicates the target API resource URI, m_k denotes the HTTP method (GET, POST, PUT, DELETE), ν_k represents the request velocity (requests per second from device d_k), α_k is the authorization claim scope, and Δt_k represents the inter-arrival latency between successive requests."
    )

    add_para(doc,
        "In a conventional disconnected security architecture, the backend policy engine evaluates request validity purely through an isolated server-side authorization function f_S(Φ_k), assuming that the client device state Ψ_t is inherently trusted or static. Consequently, when an adversary compromises the client environment (Ψ_t -> 1) and replays valid credentials (Φ_k with valid JWT), the traditional system incurs a false negative detection failure."
    )

    add_para(doc,
        "In contrast, this research defines the Cross-Layer Threat Correlation Function Γ that operates continuously over the joint product space of client telemetry and server API behavior:"
    )

    add_eq(doc, "Γ: (Ψ_t × Φ_k × R_{t-1}) -> (R_t, Π_t)", "3.3")

    add_para(doc,
        "where R_t in [0, 100] is the continuous dynamic risk score associated with device d_k at time t, and Π_t in {ALLOW, STEP_UP, RESTRICT, TERMINATE} represents the discrete Zero-Trust adaptive enforcement policy band enforced by the ingress gateway filter. The global objective of the AppShieldX framework is to optimize the policy mapping Γ to maximize threat detection recall while strictly bounding false positive rates and runtime latency overhead:"
    )

    add_eq(doc, "max_Γ Recall(Γ)   subject to   FPR(Γ) <= ε   and   ΔL_gateway(Γ) <= 5 ms", "3.4")

    # 3.2 THREAT MODEL AND ADVERSARY CAPABILITIES
    add_sec_heading(doc, "3.2", "Threat Model and Adversary Capabilities")

    add_para(doc,
        "To rigorously benchmark the security guarantees of AppShieldX, we formalize an adversarial threat model grounded in real-world mobile exploitation workflows and mapped directly to the MITRE ATT&CK for Mobile knowledge base. We assume an active, skilled adversary who has acquired physical and root access to an Android device running the client application."
    )

    add_bullet(doc, "Host Environment Dominance: The attacker possesses unrestricted root permissions on the operating system, enabling them to install kernel modules, modify system properties, alter file system permissions, and inspect all processes.", bold_prefix="Adversary Assumption 1: ")
    add_bullet(doc, "Dynamic Memory Access: The adversary can attach dynamic instrumentation toolkits (Frida, Xposed) and interactive debuggers (GDB/LLDB) to inspect, hook, and manipulate process memory, registers, and method execution flow.", bold_prefix="Adversary Assumption 2: ")
    add_bullet(doc, "Network Channel Interception: The attacker controls the local network routing infrastructure (via rogue Wi-Fi APs, VPN tunnels, or proxy software like Burp Suite) and can install custom root CA certificates into the device trust store.", bold_prefix="Adversary Assumption 3: ")
    add_bullet(doc, "Automated Scripting & Tooling: The attacker can execute automated exploitation scripts (using Python, Curl, or Postman) to replay stolen session tokens, manipulate REST parameters, and launch high-frequency API attacks against the cloud backend.", bold_prefix="Adversary Assumption 4: ")

    add_para(doc,
        "Table 3.1 details the specific adversary capabilities modeled in this study, accompanied by their corresponding MITRE ATT&CK for Mobile technique identifiers and the defensive countermeasures implemented within AppShieldX."
    )

    # Table 3.1: MITRE ATT&CK Mapping Table
    t31_headers = ["Adversary Capability", "MITRE ATT&CK ID", "Exploitation Mechanism", "AppShieldX Defense"]
    t31_data = [
        ["Dynamic Hooking", "T1417 (Input Capture)", "Injecting Frida scripts into process memory to hook business and security methods", "Active /proc/self/maps scanning and native instruction prelude integrity auditing"],
        ["Live Debugging", "T1453 (Attestation Bypass)", "Attaching GDB/LLDB debuggers via Linux ptrace to halt and manipulate execution", "Continuous /proc/self/status TracerPid polling and anti-ptrace self-attachment"],
        ["Root Escalation", "T1452 (Privilege Escalation)", "Executing su binary to bypass OS sandboxing and access protected data directories", "Multi-path su binary existence checks, test-keys scanning, and directory write probes"],
        ["Emulator Farming", "T1453 (Attestation Bypass)", "Deploying app on virtualized QEMU/Goldfish emulators for automated account fraud", "Hardware build property inspection (ro.hardware, ro.kernel.qemu) and driver checks"],
        ["MITM Interception", "T1454 (Network Interception)", "Injecting user CA certificates into Android trust store to inspect HTTPS traffic", "Strict TLS 1.3 Subject Public Key Info (SPKI) pinning and cleartext traffic blocking"],
        ["Token Theft & Replay", "T1407 (Client Exploitation)", "Extracting bearer JWTs from device memory and replaying from automated external scripts", "Cross-layer device fingerprint binding and out-of-band telemetry verification"],
        ["BOLA / IDOR Abuse", "T1453 (Attestation Bypass)", "Altering resource IDs in API requests to access unauthorized patient/financial data", "Context-aware gateway ownership attestation and dynamic risk score step-up"],
        ["Volumetric DoS", "T1499 (Endpoint DoS)", "Flooding backend APIs with high-velocity requests using automated botnets", "Redis-backed sliding window rate limiting and immediate quarantine enforcement"]
    ]
    add_tbl(doc, "Table 3.1: Adversary Capability Matrix and Mapping to MITRE ATT&CK for Mobile Techniques.",
            t31_headers, t31_data, col_widths=[1.5, 1.4, 2.0, 1.6])

    # 3.3 DATA FLOW ARCHITECTURE AND TRUST BOUNDARIES
    add_sec_heading(doc, "3.3", "Data Flow Architecture and Trust Boundaries")

    add_para(doc,
        "The AppShieldX architectural framework establishes strict, verifiable trust boundaries across distributed client and cloud environments. Figure 3.1 illustrates the Level 1 Data Flow Diagram (DFD) delineating the data pathways, system components, and security perimeters governing all transactions."
    )

    fig31_path = os.path.join(figures_dir, "figure3_1_data_flow_boundaries.png")
    add_fig(doc, fig31_path, 
            "Figure 3.1: Data Flow Diagram (Level 1) and Security Trust Boundaries Across Ingress Gateways.")

    add_para(doc,
        "As formalized in Figure 3.1 and Table 3.2, the system defines three distinct, progressively secure trust boundaries. Trust Boundary I represents the untrusted mobile host environment. Even when running on an authentic consumer smartphone, the host operating system, memory space, and local storage cannot be inherently trusted by the backend. Trust Boundary II encompasses the public internet communication channel, secured exclusively via cryptographically pinned TLS 1.3 channels. Trust Boundary III encompasses the cloud-native private virtual network, housing the API Gateway, threat correlation services, and data persistence layers."
    )

    # Table 3.2: Trust Boundaries Table
    t32_headers = ["Trust Boundary", "Contained Assets & Components", "Inherent Security Risks", "Enforced Protection Primitives"]
    t32_data = [
        ["Trust Boundary I (Mobile Endpoint)", "Presentation UI, Flutter engine, Native Android RASP probes, EncryptedSharedPreferences", "Root escalation, Frida memory hooking, live debugging, memory extraction", "Kernel-space /proc auditing, anti-debugging, Keystore AES-256-GCM encryption"],
        ["Trust Boundary II (Public Network)", "REST API HTTP request/response payloads, Out-of-band security telemetry stream", "Passive eavesdropping, active packet tampering, SSL stripping, DNS hijacking", "Strict TLS 1.3 encryption, SPKI public key certificate pinning, HMAC-SHA256 signatures"],
        ["Trust Boundary III (Cloud Ingress)", "Spring Cloud Gateway, ZeroTrustSecurityFilter, Redis Distributed Rate Limiter", "Volumetric DDoS, credential stuffing, unverified JWT token replay, BOLA abuse", "Non-blocking reactive gateway filters, token claim validation, device integrity lookup"],
        ["Trust Boundary IV (Cloud Backend)", "Threat Correlation Engine, Risk Scorer, PostgreSQL Event Store, Redis Risk Cache", "Internal privilege escalation, database injection, telemetry repudiation", "Internal VPC isolation, least-privilege RBAC, prepared statements, encrypted at rest"]
    ]
    add_tbl(doc, "Table 3.2: Data Flow Elements, Assets, and Trust Boundary Specifications.",
            t32_headers, t32_data, col_widths=[1.5, 1.8, 1.8, 1.4])

    # 3.4 CROSS-LAYER TELEMETRY AND ADAPTIVE ENFORCEMENT HYPOTHESIS
    add_sec_heading(doc, "3.4", "Cross-Layer Telemetry and Adaptive Enforcement Hypothesis")

    add_para(doc,
        "The core scientific thesis of AppShieldX posits that true runtime security can only be achieved through a synchronized, bidirectional, closed-loop telemetry and enforcement architecture. Traditional security frameworks suffer from unidirectional isolation: client defenses operate blindly without server intelligence, and server defenses process requests blindly without client device verification."
    )

    fig32_path = os.path.join(figures_dir, "figure3_2_feedback_loop.png")
    add_fig(doc, fig32_path, 
            "Figure 3.2: Cross-Layer Closed-Loop Telemetry Ingestion and Adaptive Enforcement Feedback Loop.")

    add_para(doc,
        "As illustrated in Figure 3.2, AppShieldX operationalizes a continuous six-stage closed-loop feedback mechanism: (1) Client RASP probes continuously audit local execution state; (2) Telemetry streams are cryptographically signed and transmitted out-of-band to the cloud gateway; (3) The server-side correlation engine matches client diagnostics against API behavioral patterns; (4) Dynamic risk scores are computed and synchronized to a distributed Redis cache; (5) In-line API gateway filters enforce adaptive policy decisions in real time; and (6) Adaptive enforcement signals are fed back to the client application to freeze sensitive interfaces and revoke local tokens."
    )

    add_subsec_heading(doc, "3.4.1", "Primary Research Hypotheses")
    add_para(doc,
        "To experimentally validate this architectural model, this study tests two central research hypotheses:"
    )

    add_bullet(doc, "A unified cross-layer threat correlation architecture combining client-side Linux kernel RASP diagnostics with server-side API behavioral analytics achieves statistically significant improvements in threat detection Recall and F1-score compared to isolated client-only or server-only defensive architectures, while completely eliminating false positive detections under benign operational conditions.", bold_prefix="Hypothesis 1 (Detection Superiority): ")

    add_bullet(doc, "By implementing non-blocking reactive filter chains in Spring Cloud Gateway coupled with sub-millisecond Redis in-memory risk caching, continuous zero-trust policy enforcement can be achieved with a median (P50) ingress latency overhead of less than 5.0 milliseconds, satisfying real-time enterprise performance requirements.", bold_prefix="Hypothesis 2 (Performance Feasibility): ")

    # 3.5 EXPERIMENTAL METHODOLOGY AND EMPIRICAL EVALUATION FRAMEWORK
    add_sec_heading(doc, "3.5", "Experimental Methodology and Empirical Evaluation Framework")

    add_para(doc,
        "To rigorously evaluate the research hypotheses, an empirical experimental framework was constructed encompassing four architectural configurations, ten canonical threat scenarios, and 400 controlled experimental execution runs across virtualized and physical hardware environments."
    )

    add_subsec_heading(doc, "3.5.1", "Evaluated Architectural Configurations")
    add_para(doc,
        "To establish rigorous comparative benchmarks, four distinct system configurations were deployed and evaluated:"
    )

    add_bullet(doc, "Standard commercial client-server architecture relying solely on HTTPS encryption and static JWT bearer token validation. Possesses no client RASP probes and no dynamic gateway filtering.", bold_prefix="Configuration A (Baseline): ")
    add_bullet(doc, "Mobile client hardened with native RASP detection probes. When an anomaly is detected, the application terminates locally (System.exit), but no telemetry is transmitted to the cloud gateway.", bold_prefix="Configuration B (Client-Only RASP): ")
    add_bullet(doc, "Cloud backend equipped with standard API gateway rate limiting, JWT validation, and WAF inspection. Possesses no awareness of client-side device integrity or RASP telemetry.", bold_prefix="Configuration C (Server-Only API Firewall): ")
    add_bullet(doc, "The complete AppShieldX framework featuring native kernel RASP probes, real-time telemetry streaming, six-rule threat correlation, exponential risk scoring, and in-line ZeroTrustSecurityFilter enforcement.", bold_prefix="Configuration D (AppShieldX Cross-Layer): ")

    add_subsec_heading(doc, "3.5.2", "Evaluation Metrics and Statistical Rigor")
    add_para(doc,
        "Each scenario was executed 10 times across each configuration (totaling 400 runs). Performance was evaluated using standard statistical detection metrics:"
    )

    add_eq(doc, "Recall = TP / (TP + FN),   Precision = TP / (TP + FP),   F1 = 2 · (Precision · Recall) / (Precision + Recall)", "3.5")

    add_para(doc,
        "where True Positives (TP) represent successful attack detection and mitigation, False Negatives (FN) denote undetected attacks, and False Positives (FP) indicate legitimate user requests incorrectly blocked. Additionally, latency overhead was measured at microsecond resolution across 1,000 requests per scenario to evaluate P50, P95, and P99 latency percentiles."
    )

    print("Chapter 3 generated successfully.")
