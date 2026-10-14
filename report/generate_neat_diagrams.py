# -*- coding: utf-8 -*-
"""
AppShieldX Master Clean & High-Resolution Diagram Generator
Generates pixel-perfect, publication-grade security diagrams with:
- Zero text overlap
- Generous padding and clean typography
- Distinct title banners and bullet alignments
- Cohesive modern color palettes (300 DPI)

Outputs all standalone images to: neat_diagrams/
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "neat_diagrams"))
os.makedirs(OUT_DIR, exist_ok=True)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'Liberation Serif']
plt.rcParams['mathtext.fontset'] = 'cm'

# =============================================================================
# 1. FIGURE 4.7: DUAL-DOMAIN REFERENCE CLIENT APPLICATIONS
# =============================================================================
def generate_figure4_7():
    fig, ax = plt.subplots(figsize=(13, 7.5), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.5)
    ax.axis('off')

    # Main Title Header
    ax.text(6.5, 7.1, "Dual-Domain Reference Client Applications for Empirical Validation", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0f172a')
    ax.text(6.5, 6.75, "Comparative Architectural Profiles of High-Assurance Mobile Implementations", 
            ha='center', va='center', fontsize=10, fontstyle='italic', color='#64748b')

    # ------------------ DOMAIN A: BANKING VAULT ------------------
    # Outer Card
    card_a = FancyBboxPatch((0.7, 0.6), 5.5, 5.8, boxstyle="round,pad=0.05,rounding_size=0.25",
                            ec='#1e3a8a', fc='#f8fafc', lw=2)
    ax.add_patch(card_a)
    
    # Header Banner
    hdr_a = FancyBboxPatch((0.7, 5.65), 5.5, 0.75, boxstyle="round,pad=0.05,rounding_size=0.25",
                           ec='#1e3a8a', fc='#1e3a8a', lw=1)
    ax.add_patch(hdr_a)
    ax.text(3.45, 6.1, "DOMAIN A: FINTECH BANKING VAULT", ha='center', va='center',
            fontsize=11, fontweight='bold', color='#ffffff')
    ax.text(3.45, 5.8, "[High-Assurance Consumer Finance Tier]", ha='center', va='center',
            fontsize=8.5, fontstyle='italic', color='#bfdbfe')

    # Inner Content Sections
    sections_a = [
        ("Target Workload Profile", "High-value wire transfers, account balance queries, real-time fund settlement"),
        ("Enforced Threat Policy", "Strict Zero Tolerance for root privileges, kernel debuggers, or Frida hooks"),
        ("Exposed REST Endpoints", "• POST /api/v1/banking/transfer (Financial wire execution)\n• GET   /api/v1/banking/accounts (Real-time balance lookup)\n• GET   /api/v1/banking/beneficiaries (Payee registry management)"),
        ("Automated RASP Reaction", "• Immediate UI execution freeze upon TracerPid != 0\n• Session token invalidation upon dynamic memory hook\n• Android Keystore AES-256-GCM secret wipe on tampering"),
        ("Zero-Trust Response Band", "TERMINATE (HTTP 403 Forbidden) on critical indicators; Step-Up MFA on elevation")
    ]

    y_pos = 5.35
    for title, desc in sections_a:
        ax.text(1.0, y_pos, title.upper(), ha='left', va='top', fontsize=8.5, fontweight='bold', color='#1e3a8a')
        y_pos -= 0.28
        ax.text(1.0, y_pos, desc, ha='left', va='top', fontsize=8, color='#334155', linespacing=1.3)
        # Calculate offset based on number of lines
        line_count = desc.count('\n') + 1
        y_pos -= (line_count * 0.24 + 0.18)

    # ------------------ DOMAIN B: HEALTHCARE EHR PORTAL ------------------
    # Outer Card
    card_b = FancyBboxPatch((6.8, 0.6), 5.5, 5.8, boxstyle="round,pad=0.05,rounding_size=0.25",
                            ec='#065f46', fc='#f8fafc', lw=2)
    ax.add_patch(card_b)

    # Header Banner
    hdr_b = FancyBboxPatch((6.8, 5.65), 5.5, 0.75, boxstyle="round,pad=0.05,rounding_size=0.25",
                           ec='#065f46', fc='#065f46', lw=1)
    ax.add_patch(hdr_b)
    ax.text(9.55, 6.1, "DOMAIN B: HEALTHCARE EHR CLINICAL PORTAL", ha='center', va='center',
            fontsize=11, fontweight='bold', color='#ffffff')
    ax.text(9.55, 5.8, "[HIPAA / PHI Confidential Clinical Records]", ha='center', va='center',
            fontsize=8.5, fontstyle='italic', color='#a7f3d0')

    # Inner Content Sections
    sections_b = [
        ("Target Workload Profile", "Protected Health Information (PHI), diagnostic lab records, e-prescriptions"),
        ("Enforced Threat Policy", "Granular Object-Level Ownership Attestation & Parameter Sanitization"),
        ("Exposed REST Endpoints", "• GET   /api/v1/ehr/patients/{patient_id} (Clinical health records)\n• POST /api/v1/ehr/prescriptions (Electronic prescription issuance)\n• GET   /api/v1/ehr/audit-logs (HIPAA compliance access logs)"),
        ("Automated RASP Reaction", "• Context-aware Broken Object Level Authorization (BOLA) shielding\n• Parameter tampering detection on clinical patient ID modification\n• Downgrade session to RESTRICT (read-only) upon missing telemetry"),
        ("Zero-Trust Response Band", "RESTRICT (Mutation blocked) on parameter anomalies; STEP_UP MFA on telemetry delay")
    ]

    y_pos = 5.35
    for title, desc in sections_b:
        ax.text(7.1, y_pos, title.upper(), ha='left', va='top', fontsize=8.5, fontweight='bold', color='#065f46')
        y_pos -= 0.28
        ax.text(7.1, y_pos, desc, ha='left', va='top', fontsize=8, color='#334155', linespacing=1.3)
        line_count = desc.count('\n') + 1
        y_pos -= (line_count * 0.24 + 0.18)

    out_file = os.path.join(OUT_DIR, "Figure_4_7_Dual_Domain_Client_Applications.png")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated clean: {out_file}")

# =============================================================================
# 2. FIGURE 4.6: SOC ADMINISTRATOR DASHBOARD ARCHITECTURE
# =============================================================================
def generate_figure4_6():
    fig, ax = plt.subplots(figsize=(20.0, 11.2), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 20.0)
    ax.set_ylim(0, 11.2)
    ax.axis('off')

    # Main Title Header
    ax.text(10.0, 10.65, "SOC Administrator Dashboard Live Telemetry, Monitoring & Threat Intelligence Pipeline", 
            ha='center', va='center', fontsize=21.0, fontweight='bold', color='#0f172a')
    ax.text(10.0, 10.15, "Dual-Track Observability: Prometheus/Grafana Time-Series Metrics & React Real-Time Closed-Loop Remediation", 
            ha='center', va='center', fontsize=14.0, fontstyle='italic', color='#475569')

    # Layout bounds
    y_box = 2.0
    h_full = 7.7

    # =========================================================================
    # 1. TIER 1: INGRESS & TELEMETRY GATEWAY
    # =========================================================================
    x1, w1 = 0.8, 3.8
    card1 = FancyBboxPatch((x1, y_box), w1, h_full, boxstyle="round,pad=0.05,rounding_size=0.2",
                           ec='#0284c7', fc='#f0f9ff', lw=2)
    ax.add_patch(card1)
    hdr1 = FancyBboxPatch((x1, y_box + h_full - 0.95), w1, 0.95, boxstyle="round,pad=0.05,rounding_size=0.2",
                          ec='#0284c7', fc='#0284c7', lw=1)
    ax.add_patch(hdr1)
    ax.text(x1 + w1/2, y_box + h_full - 0.48, "1. INGRESS GATEWAY", ha='center', va='center',
            fontsize=15.5, fontweight='bold', color='#ffffff')
    ax.text(x1 + w1/2, y_box + h_full - 1.30, "(Spring Cloud Perimeter)", ha='center', va='center',
            fontsize=13.0, fontstyle='italic', fontweight='bold', color='#0369a1')

    items1 = [
        "Spring Cloud Gateway Perimeter",
        "Server-Sent Events (SSE) Hub",
        "Micrometer Actuator Exporter",
        "Millisecond Ingress Clock",
        "HMAC-SHA256 Payload Check",
        "Redis Real-Time Risk Eval",
        "Ingress Header Enrichment",
        "Active Device Threat Tagging"
    ]
    cur_y = y_box + h_full - 1.82
    for it in items1:
        ax.text(x1 + 0.22, cur_y, f"• {it}", ha='left', va='top', fontsize=13.0, color='#1e293b')
        cur_y -= 0.68

    # =========================================================================
    # TRACK A (TOP): PROMETHEUS 2.52 & GRAFANA 10.4 OBSERVABILITY
    # =========================================================================
    y_top, h_top = 5.9, 3.8
    x_prom, w_prom = 5.8, 3.7
    x_graf, w_graf = 10.5, 3.7

    # Container box for Prometheus
    card_prom = FancyBboxPatch((x_prom, y_top), w_prom, h_top, boxstyle="round,pad=0.05,rounding_size=0.2",
                               ec='#ea580c', fc='#fff7ed', lw=2)
    ax.add_patch(card_prom)
    hdr_prom = FancyBboxPatch((x_prom, y_top + h_top - 0.90), w_prom, 0.90, boxstyle="round,pad=0.05,rounding_size=0.2",
                              ec='#ea580c', fc='#ea580c', lw=1)
    ax.add_patch(hdr_prom)
    ax.text(x_prom + w_prom/2, y_top + h_top - 0.45, "PROMETHEUS 2.52 (:9090)", ha='center', va='center',
            fontsize=14.5, fontweight='bold', color='#ffffff')
    ax.text(x_prom + w_prom/2, y_top + h_top - 1.25, "(Time-Series Metrics Scraping)", ha='center', va='center',
            fontsize=12.2, fontstyle='italic', fontweight='bold', color='#c2410c')

    items_prom = [
        "15s Pull Scraper via /actuator",
        "threat_detections_total Metric",
        "gateway_latency_ms Histograms",
        "rate_limit_rejected Counters",
        "JVM Memory & Thread Telemetry"
    ]
    cur_y = y_top + h_top - 1.70
    for it in items_prom:
        ax.text(x_prom + 0.20, cur_y, f"• {it}", ha='left', va='top', fontsize=12.5, color='#1e293b')
        cur_y -= 0.49

    # Container box for Grafana
    card_graf = FancyBboxPatch((x_graf, y_top), w_graf, h_top, boxstyle="round,pad=0.05,rounding_size=0.2",
                               ec='#f97316', fc='#fffaf0', lw=2)
    ax.add_patch(card_graf)
    hdr_graf = FancyBboxPatch((x_graf, y_top + h_top - 0.90), w_graf, 0.90, boxstyle="round,pad=0.05,rounding_size=0.2",
                              ec='#f97316', fc='#f97316', lw=1)
    ax.add_patch(hdr_graf)
    ax.text(x_graf + w_graf/2, y_top + h_top - 0.45, "GRAFANA 10.4 BOARDS (:3000)", ha='center', va='center',
            fontsize=14.5, fontweight='bold', color='#ffffff')
    ax.text(x_graf + w_graf/2, y_top + h_top - 1.25, "(Real-Time SOC Observability)", ha='center', va='center',
            fontsize=12.2, fontstyle='italic', fontweight='bold', color='#ea580c')

    items_graf = [
        "Pre-Provisioned Threat Boards",
        "Attack Velocity Spike Graphs",
        "P95 / P99 Latency Percentiles",
        "Multi-Vector Heatmap Panels",
        "AlertManager Webhook Triggers"
    ]
    cur_y = y_top + h_top - 1.70
    for it in items_graf:
        ax.text(x_graf + 0.20, cur_y, f"• {it}", ha='left', va='top', fontsize=12.5, color='#1e293b')
        cur_y -= 0.49

    # Arrow: Prometheus -> Grafana
    arr_pg = patches.FancyArrowPatch((x_prom + w_prom + 0.05, 7.8), (x_graf - 0.05, 7.8),
                                     arrowstyle='->', mutation_scale=16, lw=2.2, color='#ea580c')
    ax.add_patch(arr_pg)
    ax.text((x_prom + w_prom + x_graf)/2, 7.8, "PromQL\nMetrics Feed", ha='center', va='center',
            fontsize=11.2, fontweight='bold', color='#ea580c',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#ffffff', edgecolor='#ea580c', lw=1.2))

    # =========================================================================
    # TRACK B (BOTTOM): REACT / TYPESCRIPT STATE CORE
    # =========================================================================
    y_bot, h_bot = 2.0, 3.6
    x_react, w_react = 5.8, 8.4
    card_react = FancyBboxPatch((x_react, y_bot), w_react, h_bot, boxstyle="round,pad=0.05,rounding_size=0.2",
                                ec='#7c3aed', fc='#f5f3ff', lw=2)
    ax.add_patch(card_react)
    hdr_react = FancyBboxPatch((x_react, y_bot + h_bot - 0.90), w_react, 0.90, boxstyle="round,pad=0.05,rounding_size=0.2",
                               ec='#7c3aed', fc='#7c3aed', lw=1)
    ax.add_patch(hdr_react)
    ax.text(x_react + w_react/2, y_bot + h_bot - 0.45, "2. REACT / TYPESCRIPT CLIENT CORE", ha='center', va='center',
            fontsize=16.0, fontweight='bold', color='#ffffff')
    ax.text(x_react + w_react/2, y_bot + h_bot - 1.25, "(Sub-Second In-Memory Security State Machine)", ha='center', va='center',
            fontsize=13.2, fontstyle='italic', fontweight='bold', color='#6d28d9')

    items_r1 = [
        "Redux Toolkit Normalized State",
        "Live Time-Series Ring Buffer",
        "Asynchronous Event Sorter"
    ]
    items_r2 = [
        "JWT Bearer Authentication Guard",
        "Incident Filter & Search Index",
        "Sub-Second State Reconciliation"
    ]
    cur_y = y_bot + h_bot - 1.76
    for it in items_r1:
        ax.text(x_react + 0.40, cur_y, f"• {it}", ha='left', va='top', fontsize=13.2, color='#1e293b')
        cur_y -= 0.65
    cur_y = y_bot + h_bot - 1.76
    for it in items_r2:
        ax.text(x_react + 4.35, cur_y, f"• {it}", ha='left', va='top', fontsize=13.2, color='#1e293b')
        cur_y -= 0.65

    # =========================================================================
    # 3. UNIFIED SOC ANALYST CONSOLE UI
    # =========================================================================
    x3, w3 = 15.4, 3.8
    card3 = FancyBboxPatch((x3, y_box), w3, h_full, boxstyle="round,pad=0.05,rounding_size=0.2",
                           ec='#059669', fc='#ecfdf5', lw=2)
    ax.add_patch(card3)
    hdr3 = FancyBboxPatch((x3, y_box + h_full - 0.95), w3, 0.95, boxstyle="round,pad=0.05,rounding_size=0.2",
                          ec='#059669', fc='#059669', lw=1)
    ax.add_patch(hdr3)
    ax.text(x3 + w3/2, y_box + h_full - 0.48, "3. ANALYST CONSOLE UI", ha='center', va='center',
            fontsize=15.5, fontweight='bold', color='#ffffff')
    ax.text(x3 + w3/2, y_box + h_full - 1.30, "(Unified Command Center)", ha='center', va='center',
            fontsize=13.0, fontstyle='italic', fontweight='bold', color='#047857')

    items3 = [
        "Embedded Grafana Metric Boards",
        "Live Incident Triage Stream Feed",
        "Risk Score Distribution Heatmap",
        "Multi-Vector Attack Bar Analytics",
        "Forensic Raw Payload Inspector",
        "Device Quarantine Action Console",
        "Emergency Token Revoke Switch",
        "Automated Export Engine (CSV/PDF)"
    ]
    cur_y = y_box + h_full - 1.82
    for it in items3:
        ax.text(x3 + 0.22, cur_y, f"• {it}", ha='left', va='top', fontsize=13.0, color='#1e293b')
        cur_y -= 0.68

    # =========================================================================
    # FLOW CONNECTORS
    # =========================================================================
    # Gateway -> Prometheus
    arr_gw_prom = patches.FancyArrowPatch((x1 + w1 + 0.05, 7.8), (x_prom - 0.05, 7.8), arrowstyle='->',
                                          mutation_scale=16, lw=2.2, color='#ea580c')
    ax.add_patch(arr_gw_prom)
    ax.text((x1 + w1 + x_prom)/2, 7.8, "Actuator\nMetrics Pull", ha='center', va='center',
            fontsize=11.2, fontweight='bold', color='#ea580c',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#ffffff', edgecolor='#ea580c', lw=1.2))

    # Gateway -> React Core
    arr_gw_react = patches.FancyArrowPatch((x1 + w1 + 0.05, 3.8), (x_react - 0.05, 3.8), arrowstyle='->',
                                           mutation_scale=16, lw=2.2, color='#0284c7')
    ax.add_patch(arr_gw_react)
    ax.text((x1 + w1 + x_react)/2, 3.8, "JSON SSE\nEvent Stream", ha='center', va='center',
            fontsize=11.2, fontweight='bold', color='#0284c7',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#ffffff', edgecolor='#0284c7', lw=1.2))

    # Grafana -> Analyst Console UI
    arr_graf_ui = patches.FancyArrowPatch((x_graf + w_graf + 0.05, 7.8), (x3 - 0.05, 7.8), arrowstyle='->',
                                          mutation_scale=16, lw=2.2, color='#f97316')
    ax.add_patch(arr_graf_ui)
    ax.text((x_graf + w_graf + x3)/2, 7.8, "Embedded\nDashboards", ha='center', va='center',
            fontsize=11.2, fontweight='bold', color='#f97316',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#ffffff', edgecolor='#f97316', lw=1.2))

    # React Core -> Analyst Console UI
    arr_react_ui = patches.FancyArrowPatch((x_react + w_react + 0.05, 3.8), (x3 - 0.05, 3.8), arrowstyle='->',
                                           mutation_scale=16, lw=2.2, color='#7c3aed')
    ax.add_patch(arr_react_ui)
    ax.text((x_react + w_react + x3)/2, 3.8, "Reactive\nUI Render", ha='center', va='center',
            fontsize=11.2, fontweight='bold', color='#7c3aed',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#ffffff', edgecolor='#7c3aed', lw=1.2))

    # =========================================================================
    # BOTTOM DEDICATED REMEDIATION CHANNEL (REVERSE FEEDBACK BUS)
    # =========================================================================
    bot_card = FancyBboxPatch((0.8, 0.35), 18.4, 1.30, boxstyle="round,pad=0.05,rounding_size=0.2",
                              ec='#dc2626', fc='#fef2f2', lw=2.0, ls='--')
    ax.add_patch(bot_card)
    ax.text(10.0, 1.20, "ANALYST REMEDIATION & EMERGENCY CONTROL CHANNEL (REVERSE FEEDBACK BUS)",
            ha='center', va='center', fontsize=14.5, fontweight='bold', color='#991b1b')
    ax.text(10.0, 0.68, "Remote Device Blacklist   •   Session Token Purge   •   Threshold Tuning   •   False-Positive Penalty Reset   •   Sub-50ms Policy Propagation",
            ha='center', va='center', fontsize=12.0, fontweight='bold', color='#b91c1c')

    # Downward connector from Tier 3 to Bottom Bus
    arr_down = patches.FancyArrowPatch((x3 + w3/2, y_box), (x3 + w3/2, 1.65), arrowstyle='->',
                                       mutation_scale=15, lw=2.2, color='#dc2626')
    ax.add_patch(arr_down)

    # Return connector from Bottom Bus to Tier 1
    arr_ret = patches.FancyArrowPatch((x1 + w1/2, 1.65), (x1 + w1/2, y_box), arrowstyle='->',
                                      mutation_scale=15, lw=2.2, color='#dc2626')
    ax.add_patch(arr_ret)

    out_file = os.path.join(OUT_DIR, "Figure_4_6_SOC_Dashboard_Architecture.png")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated clean: {out_file}")

# =============================================================================
# 3. FIGURE 4.4: DETERMINISTIC THREAT CORRELATION STATE MACHINE
# =============================================================================
def generate_figure4_4():
    fig, ax = plt.subplots(figsize=(13.5, 7.8), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 13.5)
    ax.set_ylim(0, 7.8)
    ax.axis('off')

    # Main Title Header
    ax.text(6.75, 7.4, "Deterministic Threat Correlation State Machine Workflow (RULE-CORR-01 to 06)", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0f172a')
    ax.text(6.75, 7.05, "Dynamic Zero-Trust State Transitions Governed by Cross-Layer Event Ingestion", 
            ha='center', va='center', fontsize=10, fontstyle='italic', color='#64748b')

    # 3 Primary States
    s_w = 3.6
    s_h = 3.2
    y_s = 2.4

    # State 1: TRUSTED
    x1 = 0.7
    box1 = FancyBboxPatch((x1, y_s), s_w, s_h, boxstyle="round,pad=0.05,rounding_size=0.2",
                          ec='#16a34a', fc='#f0fdf4', lw=2)
    ax.add_patch(box1)
    hdr1 = FancyBboxPatch((x1, y_s + s_h - 0.65), s_w, 0.65, boxstyle="round,pad=0.05,rounding_size=0.2",
                          ec='#16a34a', fc='#16a34a', lw=1)
    ax.add_patch(hdr1)
    ax.text(x1 + s_w/2, y_s + s_h - 0.32, "STATE 1: TRUSTED (ALLOW)", ha='center', va='center',
            fontsize=10.5, fontweight='bold', color='#ffffff')

    ax.text(x1 + 0.3, y_s + s_h - 0.95, "Risk Score: 0 – 24 points", fontsize=9, fontweight='bold', color='#15803d')
    items1 = [
        "Device Integrity: Verified authentic",
        "Kernel Probes: TracerPid = 0, su Absent",
        "Memory Layout: Clean procfs maps",
        "API Baseline: Normal velocity (< 5 rps)",
        "Action: Permit API requests (200 OK)"
    ]
    cur_y = y_s + s_h - 1.3
    for it in items1:
        ax.text(x1 + 0.3, cur_y, f"• {it}", fontsize=8, color='#1e293b')
        cur_y -= 0.34

    # State 2: SUSPICIOUS
    x2 = 4.95
    box2 = FancyBboxPatch((x2, y_s), s_w, s_h, boxstyle="round,pad=0.05,rounding_size=0.2",
                          ec='#f59e0b', fc='#fffbeb', lw=2)
    ax.add_patch(box2)
    hdr2 = FancyBboxPatch((x2, y_s + s_h - 0.65), s_w, 0.65, boxstyle="round,pad=0.05,rounding_size=0.2",
                          ec='#f59e0b', fc='#f59e0b', lw=1)
    ax.add_patch(hdr2)
    ax.text(x2 + s_w/2, y_s + s_h - 0.32, "STATE 2: SUSPICIOUS (STEP-UP)", ha='center', va='center',
            fontsize=10.5, fontweight='bold', color='#ffffff')

    ax.text(x2 + 0.3, y_s + s_h - 0.95, "Risk Score: 25 – 49 points", fontsize=9, fontweight='bold', color='#b45309')
    items2 = [
        "Trigger: RULE-CORR-01 / CORR-02",
        "Anomalous API request burst velocity",
        "TracerPid detected on non-matching IP",
        "Telemetry heartbeat delayed (> 60s)",
        "Action: Require Step-Up Biometric MFA"
    ]
    cur_y = y_s + s_h - 1.3
    for it in items2:
        ax.text(x2 + 0.3, cur_y, f"• {it}", fontsize=8, color='#1e293b')
        cur_y -= 0.34

    # State 3: QUARANTINED
    x3 = 9.2
    box3 = FancyBboxPatch((x3, y_s), s_w, s_h, boxstyle="round,pad=0.05,rounding_size=0.2",
                          ec='#dc2626', fc='#fef2f2', lw=2)
    ax.add_patch(box3)
    hdr3 = FancyBboxPatch((x3, y_s + s_h - 0.65), s_w, 0.65, boxstyle="round,pad=0.05,rounding_size=0.2",
                          ec='#dc2626', fc='#dc2626', lw=1)
    ax.add_patch(hdr3)
    ax.text(x3 + s_w/2, y_s + s_h - 0.32, "STATE 3: QUARANTINED (TERMINATE)", ha='center', va='center',
            fontsize=10.5, fontweight='bold', color='#ffffff')

    ax.text(x3 + 0.3, y_s + s_h - 0.95, "Risk Score: 75 – 100 points", fontsize=9, fontweight='bold', color='#991b1b')
    items3 = [
        "Trigger: RULE-CORR-04 / 05 / 06",
        "Active Frida / Xposed dynamic hooks",
        "BOLA unauthorized resource access",
        "Package digital signature mismatch",
        "Action: Invalidate JWT, HTTP 403 Block"
    ]
    cur_y = y_s + s_h - 1.3
    for it in items3:
        ax.text(x3 + 0.3, cur_y, f"• {it}", fontsize=8, color='#1e293b')
        cur_y -= 0.34

    # Forward Transition 1 -> 2
    arr1 = patches.FancyArrowPatch((x1 + s_w, 4.0), (x2, 4.0), arrowstyle='->',
                                  mutation_scale=16, lw=2, color='#f59e0b')
    ax.add_patch(arr1)
    ax.text((x1 + s_w + x2)/2, 4.35, "CORR-01 / 02\n(Probe Alert)", ha='center', va='bottom',
            fontsize=8, fontweight='bold', color='#b45309')

    # Forward Transition 2 -> 3
    arr2 = patches.FancyArrowPatch((x2 + s_w, 4.0), (x3, 4.0), arrowstyle='->',
                                  mutation_scale=16, lw=2, color='#dc2626')
    ax.add_patch(arr2)
    ax.text((x2 + s_w + x3)/2, 4.35, "CORR-04 / 05\n(Active Tamper)", ha='center', va='bottom',
            fontsize=8, fontweight='bold', color='#b91c1c')

    # Top Fast-Lockdown Bypass (1 -> 3)
    # High clearance arch
    arr_top = patches.FancyArrowPatch((2.5, y_s + s_h), (11.0, y_s + s_h),
                                      connectionstyle="arc3,rad=-0.22",
                                      arrowstyle='->', mutation_scale=16, lw=2.2, color='#991b1b', ls='-.')
    ax.add_patch(arr_top)
    
    # Safe top badge completely above arc peak
    top_badge = FancyBboxPatch((3.2, 6.35), 7.1, 0.45, boxstyle="round,pad=0.05,rounding_size=0.15",
                               ec='#991b1b', fc='#fee2e2', lw=1.2)
    ax.add_patch(top_badge)
    ax.text(6.75, 6.57, "RULE-CORR-06: Direct Memory Patch + BOLA Attack (Instant Fast Lockdown Bypass)",
            ha='center', va='center', fontsize=8.2, fontweight='bold', color='#991b1b')

    # Bottom Recovery Transition (2 -> 1)
    arr_bot = patches.FancyArrowPatch((5.8, y_s), (3.4, y_s),
                                      connectionstyle="arc3,rad=-0.35",
                                      arrowstyle='->', mutation_scale=16, lw=1.8, color='#16a34a', ls='--')
    ax.add_patch(arr_bot)

    bot_badge = FancyBboxPatch((2.0, 0.8), 7.5, 0.65, boxstyle="round,pad=0.05,rounding_size=0.15",
                               ec='#16a34a', fc='#f0fdf4', lw=1.2)
    ax.add_patch(bot_badge)
    ax.text(5.75, 1.25, "TEMPORAL RISK SCORE DECAY ATTENUATION", ha='center', va='center',
            fontsize=8.5, fontweight='bold', color='#15803d')
    ax.text(5.75, 0.98, "R(t) = R_0 · e^(-λ · Δt)   (Half-life t_1/2 = 15 min, In Absence of Subsequent Hostile Anomalies)",
            ha='center', va='center', fontsize=7.8, color='#166534')

    out_file = os.path.join(OUT_DIR, "Figure_4_4_Threat_Correlation_State_Machine.png")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated clean: {out_file}")

# =============================================================================
# 4. FIGURE 4.1: APPSHIELDX SIX-TIER CLOUD-NATIVE ARCHITECTURE
# =============================================================================
def generate_figure4_1():
    fig, ax = plt.subplots(figsize=(15, 9.5), dpi=300)
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 95)
    ax.axis('off')

    # Main Canvas Header
    ax.text(75, 91.5, "AppShieldX: A Cloud-Native Runtime Protection and API Security Framework", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='#0f172a')
    ax.text(75, 88.0, "End-to-End Six-Tier Architecture Across Mobile Clients, Cloud Ingress, Microservices, and SOC Operations", 
            ha='center', va='center', fontsize=10.5, fontstyle='italic', color='#64748b')

    def draw_pillar(x, y, w, h, bg, border, title, subtitle, items, items_col2=None):
        # Card Body
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=2.0",
                              facecolor=bg, edgecolor=border, linewidth=1.8)
        ax.add_patch(rect)
        # Card Header
        hdr = FancyBboxPatch((x, y + h - 7.0), w, 7.0, boxstyle="round,pad=0.5,rounding_size=2.0",
                             facecolor=border, edgecolor=border, linewidth=1.0)
        ax.add_patch(hdr)
        ax.text(x + w/2, y + h - 3.0, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#ffffff')
        if subtitle:
            ax.text(x + w/2, y + h - 5.5, subtitle, ha='center', va='center', fontsize=7.5, fontstyle='italic', color='#e2e8f0')

        if items_col2:
            cur_y = y + h - 10.0
            for item in items:
                ax.text(x + 3, cur_y, f"• {item}", ha='left', va='top', fontsize=7.5, color='#1e293b')
                cur_y -= 2.7
            cur_y2 = y + h - 10.0
            for item in items_col2:
                ax.text(x + w/2 + 2, cur_y2, f"• {item}", ha='left', va='top', fontsize=7.5, color='#1e293b')
                cur_y2 -= 2.7
        else:
            cur_y = y + h - 9.5
            for item in items:
                if item.startswith("---"):
                    ax.plot([x + 2, x + w - 2], [cur_y + 1, cur_y + 1], color=border, lw=0.8, ls=':')
                    cur_y -= 1.8
                elif item.startswith("["):
                    ax.text(x + 2, cur_y, item, ha='left', va='top', fontsize=7.5, fontweight='bold', color=border)
                    cur_y -= 2.6
                else:
                    ax.text(x + 2, cur_y, f"• {item}", ha='left', va='top', fontsize=7.2, color='#1e293b')
                    cur_y -= 2.5

    # 1. Mobile Application Box
    draw_pillar(3, 27, 28, 57, '#e0f2fe', '#0369a1', "MOBILE APPLICATION", "(Android 16 & iOS 17+)",
                ["AppShieldX Flutter Core", "Banking Client (Domain 1)", "Healthcare Portal (Domain 2)", "Splash / Auth / Profile",
                 "-------------------------", "[RASP Protection Engine]", "su / Magisk Root Probes", "QEMU / Emulator Tests",
                 "TracerPid Debugger Probes", "Frida / Substrate Scanners", "APK Signature Validation", "SPKI Pinning & Token Guard",
                 "Encrypted Keystore Storage"])

    # 2. API Gateway
    draw_pillar(34, 27, 27, 57, '#fef3c7', '#b45309', "API GATEWAY", "(:8080 Edge Perimeter)",
                ["Spring Cloud Gateway", "Netty Reactive Runtime", "ZeroTrustSecurityFilter", "Adaptive Band Enforcement",
                 "JWT Verification & Claims", "Distributed Rate Limiter", "Input Sanitization Filter", "Security Header Injection",
                 "Telemetry Forwarding", "TLS 1.3 Termination", "Sliding Window Throttling"])

    # 3. Backend Microservices
    draw_pillar(64, 27, 28, 57, '#f3e8ff', '#7e22ce', "BACKEND SERVICES", "(Spring Boot 3.2 Java 21)",
                ["Auth Service (:8081)", "User Service (:8082)", "Business Service (:8083)",
                 "-------------------------", "[Threat Engine :8084]", "CrossLayerCorrelationEngine",
                 "Rules RULE-CORR-01..06", "RiskScoringEngine (0-100)", "Half-Life Decay Attenuation",
                 "Session Revocation Service", "Audit & Logging Service"])

    # 4. Data Layer (Top Right)
    draw_pillar(95, 48, 25, 36, '#dcfce7', '#15803d', "DATA & STATE LAYER", "(PostgreSQL 16 & Redis 7)",
                ["PostgreSQL 16 ACID Engine", "Users & RBAC Schema", "Security Events Table", "Correlation Audit Ledger",
                 "-------------------------", "Redis 7.2 Cache Cluster", "Token Hash Blacklist", "Device Risk State Cache"])

    # 5. SOC Dashboard (Far Top Right)
    draw_pillar(123, 48, 24, 36, '#ecfdf5', '#047857', "SOC ADMIN CONSOLE", "(:5173 Web Dashboard)",
                ["React 18 + TypeScript", "Vite Production Bundle", "Live Incident Feed", "Cross-Layer Correlation View",
                 "Adaptive Policy Configurator", "Ablation Analytics Page", "Interactive SOC Matrix"])

    # 6. Security Monitoring & Telemetry (Middle Right) - Generous 2-column layout
    draw_pillar(95, 26, 52, 19, '#ffe4e6', '#be123c', "SECURITY MONITORING & TELEMETRY", "(Centralized Telemetry Pipeline)",
                ["Automated Security Event Hashing", "Prometheus Metrics & Micrometer Ingestion", "Grafana Real-Time SOC Dashboards"],
                ["AlertManager P1 Webhook Integration", "Immutable Forensic Audit Logging Ledger", "SIEM Dynamic Alert Forwarding"])

    # 7. Cloud Infrastructure (Bottom Bar) - Y from 4 to 21 (Separated cleanly by 6 units)
    rect_cloud = FancyBboxPatch((3, 4), 144, 17, boxstyle="round,pad=0.5,rounding_size=2.0",
                                facecolor='#f1f5f9', edgecolor='#475569', linewidth=1.8)
    ax.add_patch(rect_cloud)
    
    hdr_cloud = FancyBboxPatch((3, 16), 144, 5, boxstyle="round,pad=0.5,rounding_size=2.0",
                               facecolor='#475569', edgecolor='#475569', linewidth=1.0)
    ax.add_patch(hdr_cloud)
    ax.text(75, 18.5, "CLOUD-NATIVE DEPLOYMENT INFRASTRUCTURE & DEVSECOPS PIPELINE",
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='#ffffff')

    cloud_items = [
        "Docker Multi-Stage Containers", "Kubernetes Manifests (K8s)", "AWS ECS / Fargate Deployment", "AWS CloudWatch Real-Time Logs",
        "Terraform IaC Infrastructure", "GitHub Actions CI/CD Pipeline", "SonarQube Static Security Analysis", "Trivy Container Vulnerability Scan"
    ]
    for idx, it in enumerate(cloud_items):
        col = idx % 4
        row = idx // 4
        ax.text(12 + col * 35, 12.0 - row * 4.5, f"•  {it}", fontsize=8.2, fontweight='bold', color='#1e293b')

    # Flow Connectors with Distinct Badges
    # 1 -> 2
    arr1 = patches.FancyArrowPatch((31, 55), (34, 55), arrowstyle='->', color='#0284c7', lw=2, mutation_scale=14)
    ax.add_patch(arr1)
    ax.text(32.5, 57.5, "TLS 1.3\n+ JWT", ha='center', va='bottom', fontsize=7, fontweight='bold', color='#0284c7')

    # 2 -> 3
    arr2 = patches.FancyArrowPatch((61, 55), (64, 55), arrowstyle='->', color='#b45309', lw=2, mutation_scale=14)
    ax.add_patch(arr2)
    ax.text(62.5, 57.5, "Enforced\nProxy", ha='center', va='bottom', fontsize=7, fontweight='bold', color='#b45309')

    # 3 -> 4
    arr3 = patches.FancyArrowPatch((92, 66), (95, 66), arrowstyle='->', color='#15803d', lw=2, mutation_scale=14)
    ax.add_patch(arr3)

    # 4 -> 5
    arr4 = patches.FancyArrowPatch((120, 66), (123, 66), arrowstyle='->', color='#047857', lw=2, mutation_scale=14)
    ax.add_patch(arr4)

    # 3 -> 6
    arr5 = patches.FancyArrowPatch((92, 36), (95, 36), arrowstyle='->', color='#be123c', lw=2, mutation_scale=14)
    ax.add_patch(arr5)

    out_file = os.path.join(OUT_DIR, "Figure_4_1_Six_Tier_System_Architecture.png")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated clean: {out_file}")

# =============================================================================
# 5. FIGURE 3.2: CROSS-LAYER CLOSED-LOOP TELEMETRY FEEDBACK LOOP
# =============================================================================
def generate_figure3_2():
    fig, ax = plt.subplots(figsize=(13.5, 8.2), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 13.5)
    ax.set_ylim(0, 8.2)
    ax.axis('off')

    # Main Title Header
    ax.text(6.75, 7.7, "Cross-Layer Closed-Loop Telemetry Ingestion & Adaptive Enforcement Feedback Loop", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0f172a')
    ax.text(6.75, 7.3, "Continuous Bidirectional Feedback Between Mobile Handset Diagnostics and Cloud Ingress Filters", 
            ha='center', va='center', fontsize=10, fontstyle='italic', color='#64748b')

    b_w = 3.6
    b_h = 2.4

    # Top Row: Y = 4.4
    # Bottom Row: Y = 0.8
    y_top = 4.4
    y_bot = 0.8

    def draw_loop_node(x, y, border, bg, step_title, bullets):
        box = FancyBboxPatch((x, y), b_w, b_h, boxstyle="round,pad=0.05,rounding_size=0.2",
                             ec=border, fc=bg, lw=2)
        ax.add_patch(box)
        hdr = FancyBboxPatch((x, y + b_h - 0.55), b_w, 0.55, boxstyle="round,pad=0.05,rounding_size=0.2",
                             ec=border, fc=border, lw=1)
        ax.add_patch(hdr)
        ax.text(x + b_w/2, y + b_h - 0.28, step_title, ha='center', va='center',
                fontsize=9.5, fontweight='bold', color='#ffffff')

        cur_y = y + b_h - 0.85
        for b in bullets:
            ax.text(x + 0.3, cur_y, f"• {b}", ha='left', va='top', fontsize=7.8, color='#1e293b')
            cur_y -= 0.35

    # [1] Client RASP Probing (Top-Left)
    draw_loop_node(0.6, y_top, '#0284c7', '#f0f9ff', "[1] Client RASP Probing",
                   ["Continuous /proc/self/status inspection", "Debugger ptrace & TracerPid polling",
                    "su & Magisk root binary existence checks", "Frida / Xposed memory map signature scan"])

    # [2] Ingestion & Parsing (Top-Center)
    draw_loop_node(4.95, y_top, '#7c3aed', '#f5f3ff', "[2] Ingestion & Parsing",
                   ["Asynchronous out-of-band telemetry stream", "HMAC-SHA256 digital signature validation",
                    "Device hardware fingerprint verification", "Millisecond timestamp replay prevention"])

    # [3] Correlation Engine (Top-Right)
    draw_loop_node(9.3, y_top, '#dc2626', '#fef2f2', "[3] Correlation Engine",
                   ["Stateful cross-layer event correlation", "Execution of 6 deterministic rules (CORR-01..06)",
                    "Exponential risk decay calculation (t_1/2 = 15m)", "Four Zero-Trust policy bands classification"])

    # [4] Shared Risk Cache (Bottom-Right)
    draw_loop_node(9.3, y_bot, '#ea580c', '#fff7ed', "[4] Shared Risk Cache",
                   ["Redis in-memory key-value state store", "Key: risk:device:{id} with 900s TTL",
                    "Sub-millisecond reactive Mono query lookup", "Centralized multi-gateway state synchronization"])

    # [5] Gateway Enforcement (Bottom-Center)
    draw_loop_node(4.95, y_bot, '#15803d', '#f0fdf4', "[5] Gateway Enforcement",
                   ["Reactive ZeroTrustSecurityFilter execution", "ALLOW: Normal traffic pass-through (200 OK)",
                    "STEP_UP: Biometric / MFA challenge prompt", "RESTRICT: Read-only mode / TERMINATE: 403 block"])

    # [6] Client Adaptive Response (Bottom-Left)
    draw_loop_node(0.6, y_bot, '#047857', '#ecfdf5', "[6] Client Adaptive Response",
                   ["In-app security warning banner display", "Sensitive transaction UI freeze & lockdown",
                    "Volatile session token memory revocation", "Hardware keystore secret wipe on compromise"])

    # Connecting Arrows
    # 1 -> 2
    a1 = patches.FancyArrowPatch((0.6 + b_w, y_top + b_h/2), (4.95, y_top + b_h/2),
                                 arrowstyle='->', mutation_scale=16, lw=2.2, color='#0284c7')
    ax.add_patch(a1)

    # 2 -> 3
    a2 = patches.FancyArrowPatch((4.95 + b_w, y_top + b_h/2), (9.3, y_top + b_h/2),
                                 arrowstyle='->', mutation_scale=16, lw=2.2, color='#7c3aed')
    ax.add_patch(a2)

    # 3 -> 4
    a3 = patches.FancyArrowPatch((9.3 + b_w/2, y_top), (9.3 + b_w/2, y_bot + b_h),
                                 arrowstyle='->', mutation_scale=16, lw=2.2, color='#dc2626')
    ax.add_patch(a3)

    # 4 -> 5
    a4 = patches.FancyArrowPatch((9.3, y_bot + b_h/2), (4.95 + b_w, y_bot + b_h/2),
                                 arrowstyle='->', mutation_scale=16, lw=2.2, color='#ea580c')
    ax.add_patch(a4)

    # 5 -> 6
    a5 = patches.FancyArrowPatch((4.95, y_bot + b_h/2), (0.6 + b_w, y_bot + b_h/2),
                                 arrowstyle='->', mutation_scale=16, lw=2.2, color='#15803d')
    ax.add_patch(a5)

    # 6 -> 1
    a6 = patches.FancyArrowPatch((0.6 + b_w/2, y_bot + b_h), (0.6 + b_w/2, y_top),
                                 arrowstyle='->', mutation_scale=16, lw=2.2, color='#047857')
    ax.add_patch(a6)

    out_file = os.path.join(OUT_DIR, "Figure_3_2_Closed_Loop_Feedback_Loop.png")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated clean: {out_file}")

# =============================================================================
# 6. FIGURE 3.1: DATA FLOW DIAGRAM (LEVEL 1) & SECURITY TRUST BOUNDARIES
# =============================================================================
def generate_figure3_1():
    fig, ax = plt.subplots(figsize=(15, 8.8), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 90)
    ax.axis('off')

    # Main Title Header
    ax.text(75, 86.8, "Data Flow Diagram (Level 1) & Security Trust Boundaries", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='#0f172a')
    ax.text(75, 83.2, "Delineation of Client-Side Runtime, Cloud Edge Ingress, and Isolated Core Persistence Tiers", 
            ha='center', va='center', fontsize=10.5, fontstyle='italic', color='#64748b')

    # ------------------ ZONE 1: TRUST BOUNDARY I (UNTRUSTED HOST) ------------------
    # Outer Red Dashed Box
    tb1 = FancyBboxPatch((4, 6), 42, 69, boxstyle="round,pad=0.5,rounding_size=2.0",
                         ec='#dc2626', fc='#fffafa', lw=2.0, ls='--')
    ax.add_patch(tb1)
    
    # Header Pill for Boundary I
    hdr_b1 = FancyBboxPatch((6, 68.5), 38, 4.8, boxstyle="round,pad=0.3,rounding_size=1.2",
                            facecolor='#fee2e2', edgecolor='#dc2626', lw=1.2)
    ax.add_patch(hdr_b1)
    ax.text(25, 71.7, "TRUST BOUNDARY I: UNTRUSTED HOST", ha='center', va='center',
            fontsize=9.2, fontweight='bold', color='#991b1b')
    ax.text(25, 69.7, "(Consumer Device, Host OS & Memory Space)", ha='center', va='center',
            fontsize=7.5, fontstyle='italic', color='#b91c1c')

    # Inner Card: Mobile Application
    card1 = FancyBboxPatch((8, 10), 34, 55, boxstyle="round,pad=0.4,rounding_size=1.5",
                           facecolor='#f8fafc', edgecolor='#334155', lw=1.6)
    ax.add_patch(card1)
    
    # Inner Card Header
    c1_hdr = FancyBboxPatch((8, 58.5), 34, 6.5, boxstyle="round,pad=0.3,rounding_size=1.2",
                            facecolor='#1e293b', edgecolor='#1e293b', lw=1.0)
    ax.add_patch(c1_hdr)
    ax.text(25, 62.6, "MOBILE APPLICATION", ha='center', va='center',
            fontsize=10.0, fontweight='bold', color='#ffffff')
    ax.text(25, 60.1, "(Flutter Core & Native Client)", ha='center', va='center',
            fontsize=7.8, fontstyle='italic', color='#94a3b8')

    # Bullets for Mobile Application
    c1_items = [
        "Presentation & Flutter UI Layer",
        "Local Secure Storage (Keystore / Keyring)",
        "Native RASP Probing Engine",
        "Kernel /proc/self Status Scanner",
        "Event Telemetry Streaming Client"
    ]
    cur_y = 55.0
    for it in c1_items:
        ax.text(10.5, cur_y, f"•  {it}", ha='left', va='top', fontsize=8.2, color='#1e293b')
        cur_y -= 4.0

    # Bottom Sub-box inside Card 1
    sub1 = FancyBboxPatch((10, 13.5), 30, 5.0, boxstyle="round,pad=0.3,rounding_size=1.0",
                          facecolor='#e2e8f0', edgecolor='#94a3b8', lw=1.0)
    ax.add_patch(sub1)
    ax.text(25, 16.0, "Kernel /proc & Native Libs", ha='center', va='center',
            fontsize=8.0, fontweight='bold', fontstyle='italic', color='#334155')

    # ------------------ DIVIDER 1: PUBLIC INTERNET (TLS 1.3) ------------------
    net_line = patches.ConnectionPatch((50, 6), (50, 74), "data", "data",
                                       arrowstyle="-", color="#f59e0b", lw=2.2, ls=':')
    ax.add_artist(net_line)
    
    # Internet Badge Pill
    net_pill = FancyBboxPatch((36, 75.0), 28, 4.2, boxstyle="round,pad=0.3,rounding_size=1.0",
                              facecolor='#fef3c7', edgecolor='#d97706', lw=1.2)
    ax.add_patch(net_pill)
    ax.text(50, 77.1, "Public Internet (TLS 1.3)", ha='center', va='center',
            fontsize=8.2, fontweight='bold', color='#b45309')

    # ------------------ ZONE 2: TRUST BOUNDARY II (CLOUD INGRESS) ------------------
    # Outer Blue Dashed Box
    tb2 = FancyBboxPatch((54, 6), 42, 69, boxstyle="round,pad=0.5,rounding_size=2.0",
                         ec='#2563eb', fc='#f8faff', lw=2.0, ls='--')
    ax.add_patch(tb2)
    
    # Header Pill for Boundary II
    hdr_b2 = FancyBboxPatch((56, 68.5), 38, 4.8, boxstyle="round,pad=0.3,rounding_size=1.2",
                            facecolor='#dbeafe', edgecolor='#2563eb', lw=1.2)
    ax.add_patch(hdr_b2)
    ax.text(75, 71.7, "TRUST BOUNDARY II: CLOUD INGRESS", ha='center', va='center',
            fontsize=9.2, fontweight='bold', color='#1d4ed8')
    ax.text(75, 69.7, "(Edge Security, Reverse Proxy & Rate Limiter)", ha='center', va='center',
            fontsize=7.5, fontstyle='italic', color='#2563eb')

    # Inner Card: API Gateway Perimeter
    card2 = FancyBboxPatch((58, 10), 34, 55, boxstyle="round,pad=0.4,rounding_size=1.5",
                           facecolor='#f8fafc', edgecolor='#334155', lw=1.6)
    ax.add_patch(card2)
    
    # Inner Card Header
    c2_hdr = FancyBboxPatch((58, 58.5), 34, 6.5, boxstyle="round,pad=0.3,rounding_size=1.2",
                            facecolor='#1e40af', edgecolor='#1e40af', lw=1.0)
    ax.add_patch(c2_hdr)
    ax.text(75, 62.6, "API GATEWAY PERIMETER", ha='center', va='center',
            fontsize=10.0, fontweight='bold', color='#ffffff')
    ax.text(75, 60.1, "(Spring Cloud Gateway :8080)", ha='center', va='center',
            fontsize=7.8, fontstyle='italic', color='#bfdbfe')

    # Bullets for API Gateway
    c2_items = [
        "Spring Cloud Gateway Edge Ingress",
        "Zero-Trust Auth & Claims Filter",
        "Distributed Rate Limiter (Redis)",
        "Device Integrity Attestation Guard",
        "Token Blacklist Validation Check"
    ]
    cur_y = 55.0
    for it in c2_items:
        ax.text(60.5, cur_y, f"•  {it}", ha='left', va='top', fontsize=8.2, color='#1e293b')
        cur_y -= 4.0

    # Bottom Sub-box inside Card 2
    sub2 = FancyBboxPatch((60, 13.5), 30, 5.0, boxstyle="round,pad=0.3,rounding_size=1.0",
                          facecolor='#e2e8f0', edgecolor='#94a3b8', lw=1.0)
    ax.add_patch(sub2)
    ax.text(75, 16.0, "Response: 200 / 401 / 403 / 429", ha='center', va='center',
            fontsize=8.0, fontweight='bold', fontstyle='italic', color='#334155')

    # ------------------ ZONE 3: TRUST BOUNDARY III (PROTECTED CORE) ------------------
    # Outer Green Dashed Box
    tb3 = FancyBboxPatch((104, 6), 42, 69, boxstyle="round,pad=0.5,rounding_size=2.0",
                         ec='#16a34a', fc='#f8fdf9', lw=2.0, ls='--')
    ax.add_patch(tb3)
    
    # Header Pill for Boundary III
    hdr_b3 = FancyBboxPatch((106, 68.5), 38, 4.8, boxstyle="round,pad=0.3,rounding_size=1.2",
                            facecolor='#dcfce7', edgecolor='#16a34a', lw=1.2)
    ax.add_patch(hdr_b3)
    ax.text(125, 71.7, "TRUST BOUNDARY III: PROTECTED BACKEND", ha='center', va='center',
            fontsize=9.2, fontweight='bold', color='#15803d')
    ax.text(125, 69.7, "(Threat Engine, Microservices & Data State)", ha='center', va='center',
            fontsize=7.5, fontstyle='italic', color='#16a34a')

    # Inner Card: Security & Business Tier
    card3 = FancyBboxPatch((108, 10), 34, 55, boxstyle="round,pad=0.4,rounding_size=1.5",
                           facecolor='#f8fafc', edgecolor='#334155', lw=1.6)
    ax.add_patch(card3)
    
    # Inner Card Header
    c3_hdr = FancyBboxPatch((108, 58.5), 34, 6.5, boxstyle="round,pad=0.3,rounding_size=1.2",
                            facecolor='#065f46', edgecolor='#065f46', lw=1.0)
    ax.add_patch(c3_hdr)
    ax.text(125, 62.6, "SECURITY & BUSINESS TIER", ha='center', va='center',
            fontsize=10.0, fontweight='bold', color='#ffffff')
    ax.text(125, 60.1, "(Spring Boot Core Services)", ha='center', va='center',
            fontsize=7.8, fontstyle='italic', color='#a7f3d0')

    # Bullets for Security & Business Tier
    c3_items = [
        "Cross-Layer Threat Correlation Engine",
        "Dynamic Risk Scorer (0-100 Bands)",
        "Business Services (Vault & EHR)",
        "Redis Real-Time Risk State Cache",
        "PostgreSQL Immutable Audit Ledger"
    ]
    cur_y = 55.0
    for it in c3_items:
        ax.text(110.5, cur_y, f"•  {it}", ha='left', va='top', fontsize=8.2, color='#1e293b')
        cur_y -= 4.0

    # Bottom Sub-box inside Card 3
    sub3 = FancyBboxPatch((110, 13.5), 30, 5.0, boxstyle="round,pad=0.3,rounding_size=1.0",
                          facecolor='#e2e8f0', edgecolor='#94a3b8', lw=1.0)
    ax.add_patch(sub3)
    ax.text(125, 16.0, "SOC Telemetry Stream", ha='center', va='center',
            fontsize=8.0, fontweight='bold', fontstyle='italic', color='#334155')

    # ------------------ CONNECTORS & FLOW ARROWS ------------------
    # 1. Signed API Req: Card 1 -> Card 2 at y = 46.0
    arr1 = patches.FancyArrowPatch((42, 46.0), (58, 46.0), arrowstyle='->',
                                   mutation_scale=16, lw=2.2, color='#0f172a')
    ax.add_patch(arr1)
    
    pill1 = FancyBboxPatch((43.5, 47.5), 13.0, 4.0, boxstyle="round,pad=0.2,rounding_size=0.8",
                           facecolor='#ffffff', edgecolor='#0f172a', lw=1.2)
    ax.add_patch(pill1)
    ax.text(50.0, 49.5, "Signed API Req", ha='center', va='center',
            fontsize=7.8, fontweight='bold', color='#0f172a')

    # 2. Filtered Req: Card 2 -> Card 3 at y = 46.0
    arr2 = patches.FancyArrowPatch((92, 46.0), (108, 46.0), arrowstyle='->',
                                   mutation_scale=16, lw=2.2, color='#0f172a')
    ax.add_patch(arr2)
    
    pill2 = FancyBboxPatch((93.5, 47.5), 13.0, 4.0, boxstyle="round,pad=0.2,rounding_size=0.8",
                           facecolor='#ffffff', edgecolor='#0f172a', lw=1.2)
    ax.add_patch(pill2)
    ax.text(100.0, 49.5, "Filtered Req", ha='center', va='center',
            fontsize=7.8, fontweight='bold', color='#0f172a')

    # 3. Direct RASP Telemetry Feed (Out-of-Band): Card 1 -> Card 3 at y = 26.5
    arr3 = patches.FancyArrowPatch((42, 26.5), (108, 26.5), arrowstyle='->',
                                   mutation_scale=16, lw=2.0, color='#dc2626', ls='--')
    ax.add_patch(arr3)
    
    pill3 = FancyBboxPatch((52.0, 24.2), 46.0, 4.6, boxstyle="round,pad=0.3,rounding_size=1.0",
                           facecolor='#ffffff', edgecolor='#dc2626', lw=1.4)
    ax.add_patch(pill3)
    ax.text(75.0, 26.5, "Direct RASP Telemetry Feed (Out-of-Band)", ha='center', va='center',
            fontsize=8.2, fontweight='bold', color='#b91c1c')

    out_file = os.path.join(OUT_DIR, "Figure_3_1_Data_Flow_Trust_Boundaries.png")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated clean: {out_file}")

# =============================================================================
# ALSO COPY / RE-GENERATE OTHER CLEAN FIGURES TO THE SAME FOLDER
# =============================================================================
def copy_existing_figures():
    import shutil
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "figures"))
    mapping = {
        "figure1_1_threat_landscape.png": "Figure_1_1_Threat_Landscape_Divergence.png",
        "figure2_1_literature_funnel.png": "Figure_2_1_PRISMA_Literature_Funnel.png",
        "figure2_2_publication_trend.png": "Figure_2_2_Publication_Trend_2021_2026.png",
        "figure4_2_rasp_kernel_probes.png": "Figure_4_2_Native_Kernel_RASP_Flowchart.png",
        "figure4_3_risk_scoring_bands.png": "Figure_4_3_Zero_Trust_Risk_Scoring_Bands.png",
        "figure4_5_database_schema_er.png": "Figure_4_5_Database_Schema_ER_Diagram.png",
        "figure5_1_detection_accuracy.png": "Figure_5_1_Threat_Detection_Accuracy_Comparison.png",
        "figure5_2_ablation_study.png": "Figure_5_2_Ablation_Study_Metrics.png",
        "figure5_3_latency_overhead.png": "Figure_5_3_Gateway_Latency_Overhead.png",
        "figure5_6_mobile_verified.png": "Figure_5_4_Motorola_Edge_50_Fusion_Verified.png"
    }
    for src_name, dst_name in mapping.items():
        src_path = os.path.join(src_dir, src_name)
        dst_path = os.path.join(OUT_DIR, dst_name)
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
            print(f"Copied clean asset: {dst_name}")

if __name__ == "__main__":
    print(f"Generating clean, high-resolution diagrams to: {OUT_DIR}")
    generate_figure4_7()
    generate_figure4_6()
    generate_figure4_4()
    generate_figure4_1()
    generate_figure3_2()
    generate_figure3_1()
    copy_existing_figures()
    print("All neat diagrams generated successfully!")
