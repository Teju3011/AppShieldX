# -*- coding: utf-8 -*-
"""
Generate Additional High-Resolution System & Security Diagrams for AppShieldX Report
Outputs to: report/figures/
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Arrow

FIG_DIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIG_DIR, exist_ok=True)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'Liberation Serif']
plt.rcParams['mathtext.fontset'] = 'cm'

def generate_figure1_1():
    """Figure 1.1: Modern Mobile Client-Server Threat Surface and Attack Divergence"""
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_facecolor('#fbfbfc')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Title
    ax.text(5, 5.6, "Modern Mobile Client–Server Threat Surface & Attack Vector Divergence", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1a202c')

    # Client-Side Domain Box
    client_box = FancyBboxPatch((0.5, 0.8), 4.0, 4.3, boxstyle="round,pad=0.2",
                                ec='#b91c1c', fc='#fef2f2', lw=2)
    ax.add_patch(client_box)
    ax.text(2.5, 4.8, "Client-Side Threat Surface (Mobile OS & Binary)", ha='center', fontsize=10.5, fontweight='bold', color='#991b1b')

    client_threats = [
        "• Runtime Code Hooking (Frida, Xposed, Substrate)",
        "• Kernel-Level Debugging (ptrace, TracerPid != 0)",
        "• Root Privilege Escalation (Magisk, SuperSU, KernelSU)",
        "• Sandboxing & Isolation Bypass (VirtualApp, DualSpace)",
        "• Memory Dumping & Live Key Extraction (/proc/self/mem)",
        "• Dynamic Class Loading & Dalvik Bytecode Patching",
        "• TLS Certificate Unpinning via Script Injection"
    ]
    for i, t in enumerate(client_threats):
        ax.text(0.8, 4.3 - i*0.5, t, fontsize=8.5, color='#374151', va='center')

    # Server-Side Domain Box
    server_box = FancyBboxPatch((5.5, 0.8), 4.0, 4.3, boxstyle="round,pad=0.2",
                                ec='#1d4ed8', fc='#eff6ff', lw=2)
    ax.add_patch(server_box)
    ax.text(7.5, 4.8, "Server-Side Threat Surface (Cloud Ingress & APIs)", ha='center', fontsize=10.5, fontweight='bold', color='#1e40af')

    server_threats = [
        "• Broken Object Level Authorization (BOLA / IDOR)",
        "• Token Exfiltration, Replay, & Forgery (JWT Tampering)",
        "• Distributed Credential Stuffing & Rate Limit Bypass",
        "• Ingress Injection (SQLi, NoSQLi, Command Injection)",
        "• API Logic Manipulation & Parameter Tampering",
        "• Cloud Microservice Privilege Escalation (SSRF)",
        "• Asymmetric Ingress Blind Spots (Unverified Device State)"
    ]
    for i, t in enumerate(server_threats):
        ax.text(5.8, 4.3 - i*0.5, t, fontsize=8.5, color='#374151', va='center')

    # Asymmetric Blind Spot Center Bridge
    arrow_left = patches.FancyArrowPatch((4.7, 2.8), (5.3, 2.8), arrowstyle='<->', 
                                         mutation_scale=20, lw=2.5, color='#b45309')
    ax.add_patch(arrow_left)
    ax.text(5.0, 3.2, "ASYMMETRIC VISIBILITY GAP", ha='center', fontsize=8, fontweight='bold', color='#b45309',
            bbox=dict(boxstyle="round,pad=0.2", fc="#fef3c7", ec="#f59e0b", lw=1))
    ax.text(5.0, 2.4, "APIs Blind to Device State\nApp Blind to Server Intel", ha='center', fontsize=7.5, color='#92400e', style='italic')

    out_path = os.path.join(FIG_DIR, "figure1_1_threat_landscape.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")

def generate_figure3_1():
    """Figure 3.1: Data Flow Diagram (Level 1) and Security Trust Boundaries"""
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_facecolor('#f8fafc')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    ax.text(5, 5.6, "Data Flow Diagram (Level 1) & Security Trust Boundaries", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#0f172a')

    # Trust Boundary 1: Untrusted Mobile Endpoint
    tb1 = FancyBboxPatch((0.4, 0.8), 2.8, 4.3, boxstyle="round,pad=0.2",
                         ec='#dc2626', fc='#ffffff', lw=1.8, ls='--')
    ax.add_patch(tb1)
    ax.text(1.8, 4.8, "Trust Boundary I:\nUntrusted Host Environment", ha='center', fontsize=9.5, fontweight='bold', color='#b91c1c')

    # Mobile App Component
    mob_box = FancyBboxPatch((0.7, 1.2), 2.2, 3.1, boxstyle="round,pad=0.15", ec='#475569', fc='#f1f5f9', lw=1.2)
    ax.add_patch(mob_box)
    ax.text(1.8, 3.9, "Mobile Application", ha='center', fontsize=9.5, fontweight='bold', color='#1e293b')
    ax.text(1.8, 3.3, "• Presentation Layer\n• Flutter / Native UI\n• Local Storage (Keystore)\n• RASP Kernel Probes\n• Event Telemetry Client", 
            ha='center', fontsize=8, color='#334155')
    ax.text(1.8, 1.6, "Kernel /proc & Native Libs", ha='center', fontsize=7.5, color='#64748b', style='italic',
            bbox=dict(boxstyle="square,pad=0.2", fc="#e2e8f0", ec="none"))

    # Network Ingress Boundary
    net_line = patches.ConnectionPatch((3.5, 0.5), (3.5, 5.2), "data", "data",
                                       arrowstyle="-", color="#f59e0b", lw=2, ls=':')
    ax.add_artist(net_line)
    ax.text(3.5, 5.35, "Public Internet (TLS 1.3)", ha='center', fontsize=8.5, fontweight='bold', color='#d97706')

    # Trust Boundary 2: Cloud Ingress & Gateway
    tb2 = FancyBboxPatch((3.8, 0.8), 2.7, 4.3, boxstyle="round,pad=0.2",
                         ec='#2563eb', fc='#ffffff', lw=1.8, ls='--')
    ax.add_patch(tb2)
    ax.text(5.15, 4.8, "Trust Boundary II:\nCloud Ingress Perimeter", ha='center', fontsize=9.5, fontweight='bold', color='#1d4ed8')

    gw_box = FancyBboxPatch((4.0, 1.2), 2.3, 3.1, boxstyle="round,pad=0.15", ec='#475569', fc='#f1f5f9', lw=1.2)
    ax.add_patch(gw_box)
    ax.text(5.15, 3.9, "API Gateway Perimeter", ha='center', fontsize=9.5, fontweight='bold', color='#1e293b')
    ax.text(5.15, 3.3, "• Spring Cloud Gateway\n• Zero-Trust Auth Filter\n• Rate Limiting (Redis)\n• Device Integrity Verification\n• Token Attestation Guard", 
            ha='center', fontsize=8, color='#334155')
    ax.text(5.15, 1.6, "Response: 200 / 401 / 403 / 429", ha='center', fontsize=7.5, color='#64748b', style='italic',
            bbox=dict(boxstyle="square,pad=0.2", fc="#e2e8f0", ec="none"))

    # Trust Boundary 3: Internal Microservices & Security Backend
    tb3 = FancyBboxPatch((6.8, 0.8), 2.8, 4.3, boxstyle="round,pad=0.2",
                         ec='#16a34a', fc='#ffffff', lw=1.8, ls='--')
    ax.add_patch(tb3)
    ax.text(8.2, 4.8, "Trust Boundary III:\nProtected Core Backend", ha='center', fontsize=9.5, fontweight='bold', color='#15803d')

    core_box = FancyBboxPatch((7.0, 1.2), 2.4, 3.1, boxstyle="round,pad=0.15", ec='#475569', fc='#f1f5f9', lw=1.2)
    ax.add_patch(core_box)
    ax.text(8.2, 3.9, "Security & Business Tier", ha='center', fontsize=9.5, fontweight='bold', color='#1e293b')
    ax.text(8.2, 3.3, "• Threat Correlation Engine\n• Dynamic Risk Scorer\n• Business Services (Vault)\n• Redis Risk State Cache\n• PostgreSQL Event Audit", 
            ha='center', fontsize=8, color='#334155')
    ax.text(8.2, 1.6, "SOC Telemetry Stream", ha='center', fontsize=7.5, color='#64748b', style='italic',
            bbox=dict(boxstyle="square,pad=0.2", fc="#e2e8f0", ec="none"))

    # Connectors
    c1 = patches.FancyArrowPatch((2.9, 3.2), (4.0, 3.2), arrowstyle='->', mutation_scale=15, lw=2, color='#0f172a')
    ax.add_patch(c1)
    ax.text(3.45, 3.4, "Signed API Req", ha='center', fontsize=7.5, fontweight='bold', color='#0f172a')

    c2 = patches.FancyArrowPatch((6.3, 3.2), (7.0, 3.2), arrowstyle='->', mutation_scale=15, lw=2, color='#0f172a')
    ax.add_patch(c2)
    ax.text(6.65, 3.4, "Filtered Req", ha='center', fontsize=7.5, fontweight='bold', color='#0f172a')

    c3 = patches.FancyArrowPatch((2.9, 2.2), (7.0, 2.2), arrowstyle='->', mutation_scale=15, lw=1.5, color='#dc2626', ls='--')
    ax.add_patch(c3)
    ax.text(5.0, 2.35, "Direct RASP Telemetry Feed (Out-of-Band)", ha='center', fontsize=7.5, fontweight='bold', color='#b91c1c')

    out_path = os.path.join(FIG_DIR, "figure3_1_data_flow_boundaries.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")

def generate_figure3_2():
    """Figure 3.2: Cross-Layer Closed-Loop Telemetry & Adaptive Enforcement Feedback Loop"""
    fig, ax = plt.subplots(figsize=(9.5, 5.2), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    ax.text(5, 5.6, "Cross-Layer Closed-Loop Telemetry & Adaptive Enforcement Feedback Loop", 
            ha='center', va='center', fontsize=12.5, fontweight='bold', color='#0f172a')

    # Step 1: Client RASP Probe
    p1 = FancyBboxPatch((0.6, 3.2), 2.2, 1.6, boxstyle="round,pad=0.15", ec='#0284c7', fc='#f0f9ff', lw=1.8)
    ax.add_patch(p1)
    ax.text(1.7, 4.3, "[1] Client RASP Probing", ha='center', fontsize=9, fontweight='bold', color='#0369a1')
    ax.text(1.7, 3.7, "Continuous inspection:\n• ptrace / TracerPid\n• su / busybox binaries\n• Frida hook artifacts", ha='center', fontsize=7.5, color='#334155')

    # Step 2: Telemetry Egress
    p2 = FancyBboxPatch((3.9, 3.2), 2.2, 1.6, boxstyle="round,pad=0.15", ec='#7c3aed', fc='#f5f3ff', lw=1.8)
    ax.add_patch(p2)
    ax.text(5.0, 4.3, "[2] Ingestion & Parsing", ha='center', fontsize=9, fontweight='bold', color='#6d28d9')
    ax.text(5.0, 3.7, "Telemetry Ingestion:\n• HMAC validation\n• Ingress timestamping\n• Device fingerprinting", ha='center', fontsize=7.5, color='#334155')

    # Step 3: Correlation & Risk Scoring
    p3 = FancyBboxPatch((7.2, 3.2), 2.2, 1.6, boxstyle="round,pad=0.15", ec='#dc2626', fc='#fef2f2', lw=1.8)
    ax.add_patch(p3)
    ax.text(8.3, 4.3, "[3] Correlation Engine", ha='center', fontsize=9, fontweight='bold', color='#b91c1c')
    ax.text(8.3, 3.7, "Stateful Correlation:\n• 6 Cross-layer rules\n• Exponential risk decay\n• Threat band classification", ha='center', fontsize=7.5, color='#334155')

    # Step 4: Redis State Synchronization
    p4 = FancyBboxPatch((7.2, 0.8), 2.2, 1.6, boxstyle="round,pad=0.15", ec='#ea580c', fc='#fff7ed', lw=1.8)
    ax.add_patch(p4)
    ax.text(8.3, 1.9, "[4] Shared Risk Cache", ha='center', fontsize=9, fontweight='bold', color='#c2410c')
    ax.text(8.3, 1.3, "Redis Key-Value Cache:\n• TTL 900s (Half-life)\n• Fast gateway lookup\n• Sub-millisecond read", ha='center', fontsize=7.5, color='#334155')

    # Step 5: Gateway Enforcement
    p5 = FancyBboxPatch((3.9, 0.8), 2.2, 1.6, boxstyle="round,pad=0.15", ec='#16a34a', fc='#f0fdf4', lw=1.8)
    ax.add_patch(p5)
    ax.text(5.0, 1.9, "[5] Gateway Enforcement", ha='center', fontsize=9, fontweight='bold', color='#15803d')
    ax.text(5.0, 1.3, "ZeroTrustSecurityFilter:\n• ALLOW (Normal)\n• STEP-UP (MFA Prompt)\n• RESTRICT (Read-Only)\n• TERMINATE (403 Block)", ha='center', fontsize=7.5, color='#334155')

    # Step 6: Client Adaptive Action
    p6 = FancyBboxPatch((0.6, 0.8), 2.2, 1.6, boxstyle="round,pad=0.15", ec='#059669', fc='#ecfdf5', lw=1.8)
    ax.add_patch(p6)
    ax.text(1.7, 1.9, "[6] Client Response", ha='center', fontsize=9, fontweight='bold', color='#047857')
    ax.text(1.7, 1.3, "App-Side Reaction:\n• Display Warning Banner\n• Re-authenticate token\n• Wipe cached secrets", ha='center', fontsize=7.5, color='#334155')

    # Arrows
    a1 = patches.FancyArrowPatch((2.8, 4.0), (3.9, 4.0), arrowstyle='->', mutation_scale=15, lw=2, color='#2563eb')
    ax.add_patch(a1)
    a2 = patches.FancyArrowPatch((6.1, 4.0), (7.2, 4.0), arrowstyle='->', mutation_scale=15, lw=2, color='#7c3aed')
    ax.add_patch(a2)
    a3 = patches.FancyArrowPatch((8.3, 3.2), (8.3, 2.4), arrowstyle='->', mutation_scale=15, lw=2, color='#dc2626')
    ax.add_patch(a3)
    a4 = patches.FancyArrowPatch((7.2, 1.6), (6.1, 1.6), arrowstyle='->', mutation_scale=15, lw=2, color='#ea580c')
    ax.add_patch(a4)
    a5 = patches.FancyArrowPatch((3.9, 1.6), (2.8, 1.6), arrowstyle='->', mutation_scale=15, lw=2, color='#16a34a')
    ax.add_patch(a5)
    a6 = patches.FancyArrowPatch((1.7, 2.4), (1.7, 3.2), arrowstyle='->', mutation_scale=15, lw=2, color='#059669')
    ax.add_patch(a6)

    out_path = os.path.join(FIG_DIR, "figure3_2_feedback_loop.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")

def generate_figure4_2():
    """Figure 4.2: Native Android RASP Probe Execution Flowchart"""
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')

    ax.text(5, 6.6, "Native Android RASP Probe Execution Flowchart in Linux Kernel Space", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#0f172a')

    # Flowchart Blocks
    start = FancyBboxPatch((3.8, 5.7), 2.4, 0.6, boxstyle="round,pad=0.2", ec='#475569', fc='#e2e8f0', lw=1.5)
    ax.add_patch(start)
    ax.text(5.0, 6.0, "App Launch / Periodic Interval", ha='center', va='center', fontsize=9, fontweight='bold')

    probe1 = FancyBboxPatch((3.5, 4.6), 3.0, 0.7, boxstyle="square,pad=0.15", ec='#0284c7', fc='#f0f9ff', lw=1.5)
    ax.add_patch(probe1)
    ax.text(5.0, 4.95, "Execute Root & Superuser Scan\nCheck /system/bin/su, /system/xbin/su", ha='center', va='center', fontsize=8)

    probe2 = FancyBboxPatch((3.5, 3.5), 3.0, 0.7, boxstyle="square,pad=0.15", ec='#0284c7', fc='#f0f9ff', lw=1.5)
    ax.add_patch(probe2)
    ax.text(5.0, 3.85, "Kernel Debugger Check\nParse /proc/self/status -> TracerPid != 0", ha='center', va='center', fontsize=8)

    probe3 = FancyBboxPatch((3.5, 2.4), 3.0, 0.7, boxstyle="square,pad=0.15", ec='#0284c7', fc='#f0f9ff', lw=1.5)
    ax.add_patch(probe3)
    ax.text(5.0, 2.75, "Emulator & Virtual Machine Scan\nCheck ro.kernel.qemu, ro.hardware=goldfish", ha='center', va='center', fontsize=8)

    probe4 = FancyBboxPatch((3.5, 1.3), 3.0, 0.7, boxstyle="square,pad=0.15", ec='#0284c7', fc='#f0f9ff', lw=1.5)
    ax.add_patch(probe4)
    ax.text(5.0, 1.65, "Hook Framework Check\nInspect /proc/self/maps for frida, xposed", ha='center', va='center', fontsize=8)

    res_box = FancyBboxPatch((3.5, 0.2), 3.0, 0.7, boxstyle="round,pad=0.15", ec='#16a34a', fc='#f0fdf4', lw=1.8)
    ax.add_patch(res_box)
    ax.text(5.0, 0.55, "Aggregate Integrity Payload\nSign HMAC-SHA256 & Stream Telemetry", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#15803d')

    # Connectors
    for y_top, y_bot in [(5.7, 5.3), (4.6, 4.2), (3.5, 3.1), (2.4, 2.0), (1.3, 0.9)]:
        arr = patches.FancyArrowPatch((5.0, y_top), (5.0, y_bot), arrowstyle='->', mutation_scale=12, lw=1.5, color='#475569')
        ax.add_patch(arr)

    # Side Alert Branch
    alert_box = FancyBboxPatch((7.2, 2.7), 2.2, 1.8, boxstyle="round,pad=0.15", ec='#dc2626', fc='#fef2f2', lw=1.8)
    ax.add_patch(alert_box)
    ax.text(8.3, 4.0, "Anomaly Detected", ha='center', fontsize=9, fontweight='bold', color='#b91c1c')
    ax.text(8.3, 3.3, "• Freeze Sensitive Views\n• Invalidate JWT Session\n• Urgent Telemetry POST\n• Log Local Security IOC", ha='center', fontsize=7.5, color='#374151')

    # Side Arrows
    for y in [4.95, 3.85, 2.75, 1.65]:
        side_arr = patches.FancyArrowPatch((6.5, y), (7.2, 3.6), arrowstyle='->', mutation_scale=10, lw=1.2, color='#dc2626', ls=':')
        ax.add_patch(side_arr)

    out_path = os.path.join(FIG_DIR, "figure4_2_rasp_kernel_probes.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")

def generate_figure4_4():
    """Figure 4.4: Deterministic Threat Correlation State Machine Workflow"""
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    ax.text(5, 5.6, "Deterministic Threat Correlation State Machine (RULE-CORR-01 to 06)", 
            ha='center', va='center', fontsize=12.5, fontweight='bold', color='#0f172a')

    # State 1: IDLE / TRUSTED
    s1 = FancyBboxPatch((0.5, 2.4), 2.2, 1.8, boxstyle="round,pad=0.2", ec='#16a34a', fc='#f0fdf4', lw=2)
    ax.add_patch(s1)
    ax.text(1.6, 3.8, "STATE: TRUSTED", ha='center', fontsize=9.5, fontweight='bold', color='#15803d')
    ax.text(1.6, 3.1, "Risk Score: 0 – 24\nDevice Integrity: VERIFIED\nAPI Baseline: NORMAL\nAction: ALLOW", ha='center', fontsize=8, color='#374151')

    # State 2: ELEVATED / SUSPICIOUS
    s2 = FancyBboxPatch((3.9, 2.4), 2.2, 1.8, boxstyle="round,pad=0.2", ec='#f59e0b', fc='#fffbeb', lw=2)
    ax.add_patch(s2)
    ax.text(5.0, 3.8, "STATE: SUSPICIOUS", ha='center', fontsize=9.5, fontweight='bold', color='#b45309')
    ax.text(5.0, 3.1, "Risk Score: 25 – 49\nTrigger: CORR-01/02\nAnomalous Frequency\nAction: STEP-UP MFA", ha='center', fontsize=8, color='#374151')

    # State 3: CRITICAL / COMPROMISED
    s3 = FancyBboxPatch((7.3, 2.4), 2.2, 1.8, boxstyle="round,pad=0.2", ec='#dc2626', fc='#fef2f2', lw=2)
    ax.add_patch(s3)
    ax.text(8.4, 3.8, "STATE: QUARANTINED", ha='center', fontsize=9.5, fontweight='bold', color='#b91c1c')
    ax.text(8.4, 3.1, "Risk Score: 75 – 100\nTrigger: CORR-04/05/06\nActive Frida / Ptrace Hook\nAction: TERMINATE (403)", ha='center', fontsize=8, color='#374151')

    # Transitions
    t1 = patches.FancyArrowPatch((2.7, 3.6), (3.9, 3.6), arrowstyle='->', mutation_scale=15, lw=1.8, color='#d97706')
    ax.add_patch(t1)
    ax.text(3.3, 3.85, "CORR-01\n(Probe Fail)", ha='center', fontsize=7.5, fontweight='bold', color='#b45309')

    t2 = patches.FancyArrowPatch((6.1, 3.6), (7.3, 3.6), arrowstyle='->', mutation_scale=15, lw=1.8, color='#dc2626')
    ax.add_patch(t2)
    ax.text(6.7, 3.85, "CORR-04\n(Hook + API)", ha='center', fontsize=7.5, fontweight='bold', color='#b91c1c')

    # Reverse Transition (Decay)
    t_rev = patches.FancyArrowPatch((4.5, 2.4), (2.0, 2.4), connectionstyle="arc3,rad=-0.4",
                                    arrowstyle='->', mutation_scale=15, lw=1.5, color='#16a34a', ls='--')
    ax.add_patch(t_rev)
    ax.text(3.2, 1.3, "Exponential Decay (Half-life = 15 min)\nNo Subsequent Anomalies", ha='center', fontsize=7.5, color='#15803d', style='italic')

    # Immediate Quarantine Bypass
    t_bypass = patches.FancyArrowPatch((2.0, 4.2), (8.0, 4.2), connectionstyle="arc3,rad=-0.35",
                                       arrowstyle='->', mutation_scale=15, lw=2, color='#991b1b', ls='-.')
    ax.add_patch(t_bypass)
    ax.text(5.0, 5.0, "RULE-CORR-06: Direct Memory Patch + BOLA Attack (Fast Lockdown)", ha='center', fontsize=8, fontweight='bold', color='#991b1b')

    out_path = os.path.join(FIG_DIR, "figure4_4_correlation_state_machine.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")

def generate_figure4_5():
    """Figure 4.5: Relational Database Schema Entity-Relationship (ER) Diagram"""
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    ax.text(5, 5.6, "Relational Database Schema Entity-Relationship (ER) Architecture", 
            ha='center', va='center', fontsize=12.5, fontweight='bold', color='#0f172a')

    # Table 1: users
    u = FancyBboxPatch((0.5, 2.8), 2.5, 2.4, boxstyle="round,pad=0.1", ec='#3b82f6', fc='#eff6ff', lw=1.5)
    ax.add_patch(u)
    ax.text(1.75, 4.9, "TABLE: users", ha='center', fontsize=9, fontweight='bold', color='#1e40af')
    ax.text(1.75, 3.8, "PK  id (UUID)\n      username (VARCHAR)\n      password_hash (VARCHAR)\n      email (VARCHAR)\n      role (VARCHAR)\n      mfa_enabled (BOOLEAN)\n      created_at (TIMESTAMP)", 
            ha='center', fontsize=7.5, color='#334155')

    # Table 2: devices
    d = FancyBboxPatch((3.7, 2.8), 2.6, 2.4, boxstyle="round,pad=0.1", ec='#10b981', fc='#ecfdf5', lw=1.5)
    ax.add_patch(d)
    ax.text(5.0, 4.9, "TABLE: devices", ha='center', fontsize=9, fontweight='bold', color='#065f46')
    ax.text(5.0, 3.8, "PK  device_id (VARCHAR)\nFK  user_id (UUID)\n      platform (VARCHAR)\n      os_version (VARCHAR)\n      device_model (VARCHAR)\n      app_version (VARCHAR)\n      last_heartbeat (TIMESTAMP)", 
            ha='center', fontsize=7.5, color='#334155')

    # Table 3: security_events
    e = FancyBboxPatch((6.9, 2.8), 2.6, 2.4, boxstyle="round,pad=0.1", ec='#ef4444', fc='#fef2f2', lw=1.5)
    ax.add_patch(e)
    ax.text(8.2, 4.9, "TABLE: security_events", ha='center', fontsize=9, fontweight='bold', color='#991b1b')
    ax.text(8.2, 3.8, "PK  event_id (UUID)\nFK  device_id (VARCHAR)\n      event_type (VARCHAR)\n      severity (VARCHAR)\n      raw_payload (JSONB)\n      source_ip (VARCHAR)\n      timestamp (TIMESTAMP)", 
            ha='center', fontsize=7.5, color='#334155')

    # Table 4: risk_assessments
    r = FancyBboxPatch((3.7, 0.2), 2.6, 2.1, boxstyle="round,pad=0.1", ec='#8b5cf6', fc='#f5f3ff', lw=1.5)
    ax.add_patch(r)
    ax.text(5.0, 2.0, "TABLE: risk_assessments", ha='center', fontsize=9, fontweight='bold', color='#5b21b6')
    ax.text(5.0, 1.1, "PK  assessment_id (UUID)\nFK  device_id (VARCHAR)\n      current_score (DOUBLE)\n      response_band (VARCHAR)\n      decay_half_life (INT)\n      last_updated (TIMESTAMP)", 
            ha='center', fontsize=7.5, color='#334155')

    # Relationships
    rel1 = patches.FancyArrowPatch((3.0, 4.0), (3.7, 4.0), arrowstyle='<->', mutation_scale=12, lw=1.5, color='#475569')
    ax.add_patch(rel1)
    ax.text(3.35, 4.2, "1:N", ha='center', fontsize=7.5, fontweight='bold', color='#475569')

    rel2 = patches.FancyArrowPatch((6.3, 4.0), (6.9, 4.0), arrowstyle='<->', mutation_scale=12, lw=1.5, color='#475569')
    ax.add_patch(rel2)
    ax.text(6.6, 4.2, "1:N", ha='center', fontsize=7.5, fontweight='bold', color='#475569')

    rel3 = patches.FancyArrowPatch((5.0, 2.8), (5.0, 2.3), arrowstyle='<->', mutation_scale=12, lw=1.5, color='#475569')
    ax.add_patch(rel3)
    ax.text(5.25, 2.55, "1:1", ha='center', fontsize=7.5, fontweight='bold', color='#475569')

    out_path = os.path.join(FIG_DIR, "figure4_5_database_schema_er.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")

def generate_figure4_6():
    """Figure 4.6: SOC Administrator Dashboard Architecture"""
    fig, ax = plt.subplots(figsize=(9.5, 5.2), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    ax.text(5, 5.6, "SOC Administrator Dashboard Live Telemetry & Threat Intelligence Pipeline", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#0f172a')

    # Component 1: Event Broker / Gateway
    b1 = FancyBboxPatch((0.6, 2.2), 2.4, 2.6, boxstyle="round,pad=0.15", ec='#0284c7', fc='#f0f9ff', lw=1.5)
    ax.add_patch(b1)
    ax.text(1.8, 4.4, "Gateway Ingress Stream", ha='center', fontsize=9, fontweight='bold', color='#0369a1')
    ax.text(1.8, 3.3, "• Server-Sent Events (SSE)\n• WebSocket Telemetry\n• Real-Time Threat Alerts\n• Dynamic Risk Score Feed\n• High-Frequency Ingestion", ha='center', fontsize=7.5, color='#334155')

    # Component 2: Frontend State Manager
    b2 = FancyBboxPatch((3.8, 2.2), 2.4, 2.6, boxstyle="round,pad=0.15", ec='#7c3aed', fc='#f5f3ff', lw=1.5)
    ax.add_patch(b2)
    ax.text(5.0, 4.4, "React / TypeScript Core", ha='center', fontsize=9, fontweight='bold', color='#6d28d9')
    ax.text(5.0, 3.3, "• Redux Toolkit State Store\n• Dynamic Aggregation\n• Filtering & Search Index\n• Live Time-Series Buffer\n• JWT Bearer Auth Guard", ha='center', fontsize=7.5, color='#334155')

    # Component 3: Visualization Panels
    b3 = FancyBboxPatch((7.0, 2.2), 2.4, 2.6, boxstyle="round,pad=0.15", ec='#059669', fc='#ecfdf5', lw=1.5)
    ax.add_patch(b3)
    ax.text(8.2, 4.4, "Analyst Dashboard UI", ha='center', fontsize=9, fontweight='bold', color='#047857')
    ax.text(8.2, 3.3, "• Interactive Incident Feed\n• Live Score Distribution\n• Attack Vector Bar Charts\n• Device Quarantine Switch\n• Audit Export (CSV/PDF)", ha='center', fontsize=7.5, color='#334155')

    # Arrows
    a1 = patches.FancyArrowPatch((3.0, 3.5), (3.8, 3.5), arrowstyle='->', mutation_scale=15, lw=2, color='#0284c7')
    ax.add_patch(a1)
    ax.text(3.4, 3.75, "JSON SSE", ha='center', fontsize=7.5, fontweight='bold', color='#0284c7')

    a2 = patches.FancyArrowPatch((6.2, 3.5), (7.0, 3.5), arrowstyle='->', mutation_scale=15, lw=2, color='#7c3aed')
    ax.add_patch(a2)
    ax.text(6.6, 3.75, "Render", ha='center', fontsize=7.5, fontweight='bold', color='#7c3aed')

    # Analyst Control Loop
    ac_loop = patches.FancyArrowPatch((7.0, 2.6), (1.8, 1.5), connectionstyle="arc3,rad=0.3",
                                      arrowstyle='->', mutation_scale=15, lw=1.5, color='#dc2626', ls='--')
    ax.add_patch(ac_loop)
    ax.text(4.5, 1.2, "Manual Override: Remote Device Blacklist / Revoke Token", ha='center', fontsize=7.5, fontweight='bold', color='#b91c1c')

    out_path = os.path.join(FIG_DIR, "figure4_6_dashboard_architecture.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")

def generate_figure4_7():
    """Figure 4.7: Dual-Domain Reference Client Applications"""
    fig, ax = plt.subplots(figsize=(9.5, 5.2), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    ax.text(5, 5.6, "Dual-Domain Reference Client Applications for Empirical Validation", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#0f172a')

    # App 1: Banking Vault
    b1 = FancyBboxPatch((0.8, 1.0), 3.8, 4.0, boxstyle="round,pad=0.2", ec='#1e3a8a', fc='#eff6ff', lw=1.8)
    ax.add_patch(b1)
    ax.text(2.7, 4.6, "Domain A: FinTech Banking Vault", ha='center', fontsize=10, fontweight='bold', color='#1e3a8a')
    ax.text(2.7, 3.7, "• Target: High-Value Financial Transactions\n• Security Policy: Zero Tolerance for Root/Frida\n• Endpoints:\n    - /api/v1/banking/accounts\n    - /api/v1/banking/transfer\n    - /api/v1/banking/beneficiaries\n• Enforcement: Immediate Transaction Freeze on\n   Debugger Attachment or Memory Tamper", 
            ha='center', fontsize=7.8, color='#1e293b')

    # App 2: Healthcare EHR
    b2 = FancyBboxPatch((5.4, 1.0), 3.8, 4.0, boxstyle="round,pad=0.2", ec='#065f46', fc='#ecfdf5', lw=1.8)
    ax.add_patch(b2)
    ax.text(7.3, 4.6, "Domain B: Healthcare EHR Portal", ha='center', fontsize=10, fontweight='bold', color='#065f46')
    ax.text(7.3, 3.7, "• Target: HIPAA / Confidential Patient Records\n• Security Policy: Broken Object & BOLA Shield\n• Endpoints:\n    - /api/v1/ehr/patients/{id}\n    - /api/v1/ehr/prescriptions\n    - /api/v1/ehr/audit-logs\n• Enforcement: Parameter Sanitization &\n   Object-Level Ownership Attestation", 
            ha='center', fontsize=7.8, color='#1e293b')

    out_path = os.path.join(FIG_DIR, "figure4_7_dual_client_apps.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated: {out_path}")

if __name__ == "__main__":
    generate_figure1_1()
    generate_figure3_1()
    generate_figure3_2()
    generate_figure4_2()
    generate_figure4_4()
    generate_figure4_5()
    generate_figure4_6()
    generate_figure4_7()
    print("All supplementary figures successfully generated.")
