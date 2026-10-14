# -*- coding: utf-8 -*-
"""
Chapter 6: Conclusions and Scope for Further Work Generator for AppShieldX Report
Target: ~4 pages synthesizing research contributions, enterprise impact, limitations, and future directions.
"""

from report_helpers import (
    add_chapter_heading, add_sec_heading, add_subsec_heading,
    add_para, add_bullet
)

def generate_chapter6(doc):
    add_chapter_heading(doc, 6, "Conclusions and Scope for Further Work")

    # 6.1 SUMMARY OF RESEARCH CONTRIBUTIONS
    add_sec_heading(doc, "6.1", "Summary of Research Contributions")

    add_para(doc,
        "This project report has presented the comprehensive design, low-level implementation, and rigorous empirical validation of AppShieldX, a pioneering, cloud-native runtime protection and API security framework engineered specifically for modern client-server mobile applications. By addressing the critical Asymmetric Ingress Blind Spot that plagues contemporary enterprise architectures, AppShieldX bridges the historical divide between client-side endpoint protection and cloud-side API perimeter defense."
    )

    add_para(doc,
        "The primary research and engineering contributions delivered through this work are summarized as follows:"
    )

    contribs = [
        ("Conceptualization of Unified Cross-Layer Architecture",
         "Dismantled the architectural silos between mobile endpoint security and cloud API gateways, establishing an end-to-end, bidirectional closed-loop security bridge that continuously correlates client runtime diagnostics with server-side API behavioral telemetry in real time."),

        ("Engineered Low-Level Native Android Kernel RASP Probes",
         "Developed an autonomous, tamper-resistant client inspection engine in native Kotlin/Java that directly interrogates the Linux procfs filesystem (/proc/self/status for TracerPid and /proc/self/maps for dynamic hooking memory signatures), eliminating vulnerabilities inherent in easily hooked high-level Java APIs."),

        ("High-Performance Reactive Cloud Ingress Defense",
         "Designed and implemented the ZeroTrustSecurityFilter within Spring Cloud Gateway, providing non-blocking, asynchronous token validation, distributed rate limiting, and real-time device integrity attestation that adds a negligible median latency overhead of only 3.76 milliseconds."),

        ("Formulation of Deterministic Multi-Event Threat Correlation",
         "Formulated and deployed six formal cross-layer correlation rules (RULE-CORR-01 through RULE-CORR-06) that successfully identify complex, multi-stage attacks that completely bypass isolated defenses, such as token replay from compromised endpoints and automated BOLA exploitation."),

        ("Mathematical Dynamic Risk Scoring with Temporal Decay",
         "Introduced an adaptive, continuous risk-scoring algorithm featuring a mathematically grounded 15-minute half-life exponential decay model, establishing four graduated Zero-Trust policy bands (ALLOW, STEP_UP, RESTRICT, TERMINATE) that prevent permanent penalization of benign transient anomalies."),

        ("Exhaustive Empirical and Hardware Validation",
         "Conducted 400 controlled experimental evaluation runs across ten canonical attack scenarios, proving that AppShieldX achieves 93.33% overall detection recall (85.71% against sophisticated blended attacks) and 100% precision with zero false positives under benign workloads, with verified physical deployment on a Motorola Edge 50 Fusion device running Android 16.")
    ]

    for c_title, c_desc in contribs:
        add_bullet(doc, c_desc, bold_prefix=f"{c_title}: ")

    # 6.2 INDUSTRIAL SIGNIFICANCE AND PRACTICAL FEASIBILITY
    add_sec_heading(doc, "6.2", "Industrial Significance and Practical Feasibility")

    add_para(doc,
        "The architectural paradigm established by AppShieldX possesses direct, transformative relevance for production enterprise systems, particularly within high-assurance verticals such as financial technology (FinTech) and digital healthcare. Regulatory frameworks such as the Payment Card Industry Data Security Standard (PCI-DSS v4.0) and the Health Insurance Portability and Accountability Act (HIPAA) increasingly mandate continuous endpoint attestation and real-time auditability of API transactions."
    )

    add_para(doc,
        "AppShieldX demonstrates that enterprise-grade Zero Trust can be implemented without imposing unacceptable performance penalties or requiring radical rewrites of existing backend microservices. Because the framework encapsulates its ingress defense within a standard Spring Cloud Gateway filter, organizations can deploy AppShieldX transparently in front of legacy microservices. Furthermore, the client-side Flutter SDK integration enables rapid adoption across existing mobile applications with minimal developer overhead."
    )

    # 6.3 TECHNICAL LIMITATIONS
    add_sec_heading(doc, "6.3", "Technical Limitations")

    add_para(doc,
        "Despite its demonstrated efficacy, several technical boundary conditions and limitations must be acknowledged:"
    )

    add_bullet(doc, "The native RASP engine's primary kernel inspection probes rely on the Linux procfs (/proc) virtual filesystem, which is specific to the Android operating system. On Apple iOS, sandboxing restrictions prevent arbitrary /proc access, requiring alternative Mach kernel APIs and ptrace denial calls.", bold_prefix="Platform Specificity: ")
    add_bullet(doc, "While AppShieldX successfully detects user-space root toolkits (Magisk, SuperSU), kernel-level rootkits operating as custom Linux kernel modules or eBPF programs can theoretically hook kernel system call handlers and forge clean /proc outputs.", bold_prefix="Kernel-Space Adversaries: ")
    add_bullet(doc, "The six correlation rules deployed in the Threat Correlation Engine are deterministically specified based on expert cybersecurity heuristics. While highly effective against known attack patterns, static rules require manual updates to address zero-day attack vectors.", bold_prefix="Deterministic Rule Bounds: ")

    # 6.4 SCOPE FOR FUTURE WORK
    add_sec_heading(doc, "6.4", "Scope for Future Work")

    add_para(doc,
        "Building upon the foundational architecture demonstrated in this thesis, future research will explore several promising directions to expand and deepen the AppShieldX framework:"
    )

    add_bullet(doc, "Integrate hardware-backed secure enclaves—such as ARM TrustZone, Google Titan M2, and Apple Secure Enclave—to anchor telemetry signatures within physically tamper-proof hardware, rendering even kernel-level rootkits incapable of forging device attestation tokens.", bold_prefix="Hardware Enclave Attestation: ")
    add_bullet(doc, "Deploy extended Berkeley Packet Filter (eBPF) probes directly within cloud Kubernetes worker nodes to correlate container-level system calls with incoming API gateway traffic, providing end-to-end kernel visibility from the mobile handset to the cloud database container.", bold_prefix="Cloud-Native eBPF Ingress Probing: ")
    add_bullet(doc, "Incorporate online machine learning models (such as autoencoders and reinforcement learning agents) to dynamically tune correlation rule weights and learn emergent threat patterns autonomously without human rule authoring.", bold_prefix="Self-Supervised Machine Learning Correlation: ")
    add_bullet(doc, "Investigate Zero-Knowledge Proofs (ZK-SNARKs) to enable mobile clients to cryptographically prove their device integrity to the cloud gateway without transmitting detailed device configuration metadata, enhancing user privacy under GDPR mandates.", bold_prefix="Privacy-Preserving Attestation: ")

    print("Chapter 6 generated successfully.")
