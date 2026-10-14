# -*- coding: utf-8 -*-
"""
Chapter 1: Introduction Generator for AppShieldX Report
Target: ~8 pages of rigorous academic text, figures, and structured analysis.
"""

import os
from report_helpers import (
    add_chapter_heading, add_sec_heading, add_subsec_heading,
    add_para, add_bullet, add_fig, add_tbl, add_eq
)

def generate_chapter1(doc, figures_dir):
    add_chapter_heading(doc, 1, "Introduction")

    # 1.1 BACKGROUND AND INDUSTRY CONTEXT
    add_sec_heading(doc, "1.1", "Background and Industry Context")

    add_para(doc,
        "Over the past decade, enterprise computing has undergone an unprecedented paradigm transition away from monolithic, perimeter-bound desktop architectures toward decentralized, cloud-native client-server ecosystems. In modern enterprises across financial technology (FinTech), digital healthcare, e-governance, and critical supply chains, mobile applications running on Android and iOS have become the de facto primary interaction interface for hundreds of millions of users worldwide. These mobile endpoints no longer function as isolated computational silos; instead, they serve as lightweight, highly dynamic presentation tiers that continuously interface with distributed backend microservices orchestrated across public, private, and hybrid cloud infrastructures."
    )

    add_para(doc,
        "This architectural revolution is fundamentally underpinned by Representational State Transfer (REST) APIs, GraphQL gateways, and asynchronous messaging queues. Every user action—ranging from biometric account authentication, balance queries, and peer-to-peer fund transfers to the retrieval of highly sensitive electronic health records (EHR)—triggers a high-frequency cascade of HTTPS requests terminating at cloud ingress controllers. According to recent cloud telemetry reports, mobile-originated API requests account for well over seventy percent of all ingress traffic observed at enterprise web application firewalls and cloud gateways. Furthermore, the operational flexibility offered by containerized orchestration platforms, notably Kubernetes, has accelerated the deployment velocity of backend services, allowing organizations to release features at microsecond granularity."
    )

    add_para(doc,
        "However, this ubiquitous connectivity and rapid architectural decentralization have fundamentally dismantled the traditional castle-and-moat security perimeter. In legacy enterprise paradigms, corporate endpoints operated within physically controlled corporate local area networks behind monolithic firewalls, intrusion detection appliances, and enterprise proxies. In stark contrast, modern client-server mobile applications operate in an inherently untrusted, zero-trust reality: mobile client software binaries are distributed publicly via commercial application marketplaces (such as Google Play Store and Apple App Store) and execute directly on heterogeneous consumer-grade smartphones. These client devices operate beyond corporate control, within user-administered operating system environments that are persistently exposed to hostile adversaries, local privilege escalation exploits, malicious application co-habitation, and intrusive inspection toolkits."
    )

    fig1_path = os.path.join(figures_dir, "figure1_1_threat_landscape.png")
    add_fig(doc, fig1_path, 
            "Figure 1.1: Modern Mobile Client-Server Threat Surface and Vector Attack Divergence.")

    add_para(doc,
        "As illustrated in Figure 1.1, the attack surface in contemporary client-server architectures has experienced a profound structural divergence. On the client side, adversaries possess unconstrained physical access to the executing endpoint, enabling arbitrary static and dynamic manipulation. Attackers routinely employ sophisticated dynamic binary instrumentation (DBI) frameworks, such as Frida and Xposed, to hook runtime functions, tamper with memory states, manipulate boolean return values of security checks, and bypass cryptographically enforced access control logic. Simultaneously, kernel-level root kits (including Magisk, SuperSU, and KernelSU) leverage system-level privilege escalation to grant arbitrary applications superuser access, completely evading standard Android sandbox isolation mechanisms."
    )

    add_para(doc,
        "On the server side, backend cloud microservices face an unrelenting barrage of automated API exploitation, including Broken Object Level Authorization (BOLA/IDOR), token exfiltration, credential stuffing, parameter tampering, and denial-of-service volumetric spikes. Because traditional backend services are architecturally decoupled from mobile clients, they evaluate incoming requests purely on the basis of cryptographic bearer tokens (such as JSON Web Tokens, or JWTs) without possessing any real-time awareness of whether the originating client device is operating in a secure, authentic state or under active debugger control. This profound divergence creates an acute security imbalance that legacy defensive paradigms cannot remediate."
    )

    # 1.2 MOTIVATION AND SECURITY PARADIGM SHIFT
    add_sec_heading(doc, "1.2", "Motivation and Security Paradigm Shift")

    add_para(doc,
        "The motivation behind this research stems from the dangerous escalation of sophisticated client-side exploitation techniques and their direct correlation with catastrophic enterprise data breaches. In conventional development practice, mobile application security has historically relied upon static compilation-time hardening techniques. Organizations invest heavily in source code obfuscation (e.g., ProGuard, R8, DexGuard), binary string encryption, and basic static packaging integrity checks. While static obfuscation increases the reverse engineering friction for amateur attackers, it provides negligible resistance against modern dynamic analysis."
    )

    add_para(doc,
        "Dynamic instrumentation frameworks, most notably Frida, operate by injecting a Google V8 JavaScript engine directly into the target process's memory space via Linux ptrace system calls or dynamic linker (dlopen) hooks. Once injected, an attacker can dynamically intercept native C/C++ method invocations, hook Dalvik/ART virtual machine methods, inspect unencrypted memory buffers, and arbitrarily rewrite function arguments and return values at runtime. For example, a financial application's local pin verification routine, root detection boolean method, or biometric validation check can be permanently neutralized with fewer than five lines of Frida JavaScript hooking script, completely independent of how heavily the underlying bytecode was obfuscated at build time."
    )

    add_bullet(doc, "Dynamic Instrumentation Dominance: Adversaries bypass all static bytecode hardening and code obfuscation by dynamically injecting scripts into live process memory using Frida, Xposed, and Substrate.", bold_prefix="Runtime Hooking: ")
    add_bullet(doc, "Automated Root Cloaking: Advanced root masking utilities (e.g., Magisk DenyList, Shamiko, Zygisk modules) hook kernel mount namespaces and system calls, presenting an entirely benign environment to naive detection libraries.", bold_prefix="Kernel-Level Evasion: ")
    add_bullet(doc, "Cryptographic Token Exfiltration: Once an application process is hooked or memory is dumped via /proc/self/mem, active JWT bearer tokens and OAuth refresh secrets are extracted and transferred to external attack toolkits.", bold_prefix="Credential Hijacking: ")
    add_bullet(doc, "Transport Layer Tampering: Attackers deploy custom root Certificate Authorities (CAs) into user trust stores and utilize dynamic scripts to unpin SSL/TLS certificates, permitting transparent Man-in-the-Middle (MITM) inspection.", bold_prefix="TLS Interception: ")

    add_para(doc,
        "Crucially, existing enterprise security solutions treat mobile security and cloud security as two completely distinct, non-communicating functional silos. On one hand, commercial client-side Runtime Application Self-Protection (RASP) solutions operate autonomously on the mobile handset. When a RASP engine detects an anomaly—such as a debugger attachment or a root binary—its standard programmed response is to trigger an immediate, ungraceful client application crash (e.g., invoking System.exit(0) or raising an unhandled SIGKILL exception). While this halts local execution, it utterly fails to notify the cloud backend of the ongoing attack. The compromised session tokens, active API keys, and authenticated session state remain fully valid within cloud identity caches."
    )

    add_para(doc,
        "On the other hand, server-side API gateways and Web Application Firewalls (WAFs) operate in complete blindness regarding client-side endpoint integrity. When an attacker exfiltrates an active OAuth2 or JWT session token from a hooked device and replays it through an automated Postman script or custom Python botnet to extract sensitive records, the backend API gateway inspects the incoming HTTP request, validates the cryptographic signature of the JWT against its RSA public key, observes valid claims, and dutifully fulfills the unauthorized request. The backend possesses zero visibility into the reality that the token was harvested from a compromised, hooked client process."
    )

    add_para(doc,
        "Consequently, there is an urgent, compelling necessity to execute a fundamental security paradigm shift: moving from disjointed, isolated, static perimeter defenses toward a unified, cross-layer, zero-trust runtime framework. In this new paradigm, client-side runtime security diagnostics must be continuously correlated with server-side API behavioral metrics in real time, establishing a closed-loop security bridge capable of dynamically enforcing adaptive countermeasures across the entire client-server transaction lifecycle."
    )

    # 1.3 PROBLEM FORMULATION: ASYMMETRIC INGRESS BLIND SPOTS
    add_sec_heading(doc, "1.3", "Problem Formulation: Asymmetric Ingress Blind Spots")

    add_para(doc,
        "To rigorously conceptualize the core vulnerability addressed in this thesis, we formulate the challenge of Asymmetric Ingress Blind Spots in distributed mobile-cloud architectures. Let a client-server transaction be denoted as a tuple T = (C, N, S), where C represents the client execution environment, N denotes the untrusted network transit channel, and S represents the cloud backend service infrastructure. In a conventional cloud-native implementation, the security enforcement function E applied at the cloud ingress perimeter is defined strictly over the network payload and identity headers:"
    )

    add_eq(doc, "E(T) = f(Req_{headers}, Req_{payload}, Token_{JWT})", "1.1")

    add_para(doc,
        "Under Equation (1.1), the enforcement decision is completely independent of the physical and virtual integrity state of the client environment, denoted as Psi(C). Specifically, Psi(C) is a high-dimensional state vector encompassing operating system attributes, kernel debugging indicators, process memory layout integrity, root privilege elevation markers, and emulator virtualization artifacts:"
    )

    add_eq(doc, "Ψ(C) = [ψ_debug, ψ_root, ψ_hook, ψ_emul, ψ_integrity]^T", "1.2")

    add_para(doc,
        "Because existing cloud ingress gateways enforce access control based strictly on Equation (1.1) while ignoring Equation (1.2), an adversary who achieves partial compromise of C—such as attaching a debugger (ψ_debug = 1) or injecting Frida hooking hooks (ψ_hook = 1)—can easily satisfy E(T) = ALLOW as long as the cryptographic token Token_{JWT} remains structurally and mathematically valid. We denote this systemic architectural discrepancy as the Asymmetric Visibility Gap (Δ_V):"
    )

    add_eq(doc, "Δ_V = |Ψ(C)_actual - Ψ(C)_server_perceived| >> 0", "1.3")

    add_para(doc,
        "When Delta_V is non-zero, an attacker exploits this blind spot to carry out multi-stage blended cyber attacks. The primary manifestations of these asymmetric blind spots include:"
    )

    add_subsec_heading(doc, "1.3.1", "Decoupled Autonomous Client Termination Vulnerability")
    add_para(doc,
        "When traditional client-side RASP libraries detect a tampering event, their unilateral termination of the local application process provides an attacker with immediate feedback during the reverse-engineering cycle. The attacker systematically modifies their hooking scripts (e.g., patching the RASP check function) until the application no longer crashes. Because the cloud backend is never notified of these successive failed tampering attempts, the adversary can iteratively probe the application's client-side defenses indefinitely without triggering account lockouts, IP blacklisting, or threat intelligence alerting at the enterprise Security Operations Center (SOC)."
    )

    add_subsec_heading(doc, "1.3.2", "Token Replay and Broken Object Exploitation Under Compromised States")
    add_para(doc,
        "In modern microservice architectures, authorization tokens typically have lifetimes ranging from 15 minutes to several days. Once an attacker extracts a bearer token from device memory or an unpinned TLS stream, they replay that token from outside the mobile application using automated exploitation frameworks. These tools systematically enumerate object identifiers (targeting OWASP API1:2023 Broken Object Level Authorization) or attempt administrative endpoints (OWASP API5:2023 Broken Function Level Authorization). To the cloud API gateway, these requests appear perfectly legitimate because they contain valid signatures, originating from what the server assumes is a trusted mobile client."
    )

    add_subsec_heading(doc, "1.3.3", "Lack of Adaptive, Risk-Proportional Enforcement Mechanisms")
    add_para(doc,
        "Traditional security mechanisms enforce binary access decisions: either an incoming request is completely permitted (HTTP 200 OK) or completely rejected (HTTP 403 Forbidden). However, real-world operational environments exhibit complex, nuanced shades of risk. For instance, a mobile device running in an Android emulator during authorized QA testing, or a user device with developer options enabled for legitimate USB debugging, may represent elevated risk without necessarily indicating malicious compromise. A rigid binary enforcement model results in either unacceptable business friction (high false positive blocks against legitimate customers) or severe security exposure (tolerating high-risk environments to avoid user complaints). What is critically missing is an adaptive, multi-tier risk-scoring framework that dynamically adjusts enforcement rigor based on continuous cross-layer threat correlation."
    )

    # 1.4 RESEARCH OBJECTIVES
    add_sec_heading(doc, "1.4", "Research Objectives")

    add_para(doc,
        "To resolve the aforementioned architectural limitations and eliminate the asymmetric visibility gap, this research project establishes eight comprehensive engineering and research objectives:"
    )

    objs = [
        ("Objective 1: Cloud-Native Security Framework Architecture",
         "To conceptualize, design, and implement AppShieldX, a unified, cloud-native runtime protection and API security framework for client-server Android applications that bridges client endpoint diagnostics with cloud microservice defenses."),
        ("Objective 2: Kernel-Level Native Client Runtime Protection (RASP)",
         "To engineer a native Android RASP engine utilizing Linux kernel inspection probes (/proc/self/status TracerPid, /proc/self/maps, system binaries, build properties) via a robust Flutter MethodChannel to detect debugging, root elevation, emulators, and dynamic instrumentation in real time."),
        ("Objective 3: Cryptographically Attested End-to-End Transport Security",
         "To establish an impenetrable client-server communication channel leveraging TLS 1.3, Subject Public Key Info (SPKI) certificate pinning, ephemeral JWT session handling, and HMAC-SHA256 signature attestation for all out-of-band security telemetry."),
        ("Objective 4: Cloud Ingress Protection and Reactive Gateway Security",
         "To develop a high-throughput, reactive API Gateway filter (ZeroTrustSecurityFilter in Spring Cloud Gateway) that intercepts all incoming API requests, performs distributed token validation, enforces Redis-backed rate limiting, and validates real-time client integrity before upstream routing."),
        ("Objective 5: Centralized Threat Event Ingestion and Multi-Stage Correlation",
         "To design a high-performance security telemetry ingestion pipeline and a stateful Threat Correlation Engine capable of correlating asynchronous client runtime alerts with synchronous API request anomalies against six deterministic cross-layer security rules (RULE-CORR-01 to 06)."),
        ("Objective 6: Dynamic Server-Side Risk Scoring and Adaptive Enforcement",
         "To formulate and implement a mathematical risk-scoring algorithm with exponential half-life temporal decay (half-life of 15 minutes) that categorizes client threat states into four progressive operational bands (ALLOW, STEP_UP, RESTRICT, TERMINATE) and dynamically throttles permissions."),
        ("Objective 7: Real-Time SOC Administrator Dashboard and Threat Intelligence",
         "To develop a responsive, modern web-based Security Operations Center (SOC) dashboard utilizing React, TypeScript, and Server-Sent Events (SSE) that provides security analysts with real-time incident visualization, risk score heatmaps, attack vector analytics, and remote device quarantine overrides."),
        ("Objective 8: Empirical Validation Across Multi-Domain Applications and Physical Hardware",
         "To rigorously evaluate the framework through 400 experimental attack scenarios across dual reference applications (FinTech Banking Vault and Healthcare EHR Portal), validating threat detection recall, precision, false positive rates, gateway latency overhead, and empirical efficacy on a physical Motorola Edge 50 Fusion device running Android 16.")
    ]

    for o_title, o_desc in objs:
        add_bullet(doc, o_desc, bold_prefix=f"{o_title}: ")

    # 1.5 SCOPE AND BOUNDARY CONDITIONS
    add_sec_heading(doc, "1.5", "Scope and Boundary Conditions")

    add_para(doc,
        "The scope of this project encompasses the complete engineering and empirical evaluation of the AppShieldX framework across both mobile client operating environments and cloud-native backend infrastructures. Specifically, the boundary conditions and operational scope of this research are delineated as follows:"
    )

    add_subsec_heading(doc, "1.5.1", "Client-Side Platform and Execution Scope")
    add_para(doc,
        "The client-side implementation targets modern mobile platforms, with primary low-level kernel probe engineering focused on the Android operating system (specifically Android API levels 28 through 36, encompassing Android 9.0 up to Android 16). Cross-platform architectural integration is achieved via the Flutter SDK (Dart runtime) interfacing through custom Java/Kotlin native platform channels. While cross-platform architectural hooks for Apple iOS (integrating App Transport Security, fork checks, and ptrace anti-attachment) are formally specified, empirical kernel-level probe validation is concentrated on Linux kernel /proc filesystems and Android Dalvik/ART runtimes. Testing is executed across both Quick Emulator (QEMU) virtualized environments and physical Android consumer hardware."
    )

    add_subsec_heading(doc, "1.5.2", "Backend Cloud Infrastructure and Gateway Scope")
    add_para(doc,
        "The backend infrastructure is engineered adhering strictly to cloud-native principles. The service tier is built on Spring Boot 3.x and Java 17, utilizing the non-blocking, reactive Spring Cloud Gateway framework for ingress traffic management. Persistence and caching tiers are realized using PostgreSQL 15 for relational ACID compliance and audit event logging, and Redis 7.x for ultra-low-latency in-memory session caching, distributed rate limiting, and dynamic risk-score state management. Containerization is implemented via Docker and Docker Compose, with Kubernetes (K8s) deployment manifests configured for multi-replica horizontal pod autoscaling."
    )

    add_subsec_heading(doc, "1.5.3", "Adversarial Threat Scope")
    add_para(doc,
        "The adversarial threat model assumes a capable, motivated attacker who possesses physical and logical access to the client mobile device. The threat scope explicitly encompasses: (1) user-space dynamic binary instrumentation and method hooking via Frida and Xposed; (2) process memory dumping and live debugging attachment via GDB, LLDB, and IDA Pro; (3) operating system privilege elevation via Magisk, SuperSU, and KernelSU root toolkits; (4) virtualization evasion and automated botnet farming via Android emulators; and (5) network-level Man-in-the-Middle (MITM) proxy interception and SSL stripping via tools such as Burp Suite and OWASP ZAP. Physical hardware extraction attacks requiring electron microscopy, fault injection, or side-channel power analysis of secure elements are explicitly outside the scope of this software-focused framework."
    )

    # 1.6 THESIS ORGANIZATION
    add_sec_heading(doc, "1.6", "Thesis Organization")

    add_para(doc,
        "The remainder of this academic project report is systematically organized into five subsequent chapters, followed by references and technical appendices, structured as follows:"
    )

    add_para(doc,
        "Chapter 2: Literature Review presents an exhaustive survey of modern mobile and cloud security literature from 2021 through 2026. It formalizes a taxonomy of client-server attack vectors, traces the evolution of Runtime Application Self-Protection (RASP), analyzes cloud-native ingress defense models, and examines Zero-Trust Architecture principles. It presents a PRISMA-compliant literature selection methodology, delivers a rigorous comparative critique of 20 foundational peer-reviewed studies, and articulates six major research gaps that motivate the AppShieldX framework."
    )

    add_para(doc,
        "Chapter 3: Problem Statement and Methodology provides a formal mathematical formulation of cross-layer threat correlation. It details the adversarial threat model mapped against the MITRE ATT&CK for Mobile framework, defines Data Flow Diagrams (DFD Level 1) and trust boundaries, formulates the core cross-layer correlation research hypotheses, and outlines the multi-scenario empirical evaluation methodology."
    )

    add_para(doc,
        "Chapter 4: System Design provides an in-depth architectural blueprint of the AppShieldX framework. It details the six-tier distributed architecture, the native Linux kernel RASP inspection engine, TLS 1.3 cryptographic pinning, the Spring Cloud Gateway ZeroTrustSecurityFilter, the six deterministic cross-layer correlation rules, the mathematical risk scoring engine with exponential decay, the relational and in-memory persistence schemas, the SOC administrator dashboard, and the dual reference client applications."
    )

    add_para(doc,
        "Chapter 5: Results and Discussions delivers an extensive empirical analysis based on 400 experimental attack runs across ten canonical threat scenarios. It presents detection accuracy confusion matrices, a five-variant ablation study, ingress latency and runtime performance overhead benchmarks, empirical validation on a physical Motorola Edge 50 Fusion device running Android 16, and an analysis of security threats to validity."
    )

    add_para(doc,
        "Chapter 6: Conclusions and Scope for Further Work summarizes the principal research contributions, evaluates enterprise and industrial significance, acknowledges technical limitations, and charts future research directions, including hardware enclave integration and kernel-space eBPF telemetry."
    )

    add_para(doc,
        "References and Appendices provide a comprehensive bibliography of peer-reviewed literature cited throughout this report in IEEE format, followed by formal documentation encompassing plagiarism evaluation certificates, production-grade source code listings, rule specifications, and experimental metric datasets."
    )

    print("Chapter 1 generated successfully.")
