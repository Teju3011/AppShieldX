import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
ax.set_xlim(0, 120)
ax.set_ylim(0, 75)
ax.axis('off')

# Color palette
c_client = '#e0f2fe'
c_client_b = '#0369a1'
c_gw = '#fef3c7'
c_gw_b = '#b45309'
c_ms = '#f3e8ff'
c_ms_b = '#7e22ce'
c_data = '#dcfce7'
c_data_b = '#15803d'
c_sec = '#ffe4e6'
c_sec_b = '#be123c'
c_cloud = '#f1f5f9'
c_cloud_b = '#475569'

def draw_box(x, y, w, h, bg, border, title, items, subtitle=""):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.5",
                                  facecolor=bg, edgecolor=border, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h - 2.5, title, ha='center', va='top', fontsize=9, fontweight='bold', color=border)
    if subtitle:
        ax.text(x + w/2, y + h - 5.0, subtitle, ha='center', va='top', fontsize=7.5, fontstyle='italic', color='#64748b')
    cur_y = y + h - (7.5 if subtitle else 5.5)
    for item in items:
        ax.text(x + 2, cur_y, f"• {item}", ha='left', va='top', fontsize=7.2, color='#1e293b')
        cur_y -= 2.6

# 1. Android Application Box
draw_box(2, 22, 24, 48, c_client, c_client_b, "MOBILE APPLICATION", 
         ["AppShieldX Flutter Core", "Banking Client (Domain 1)", "Healthcare Portal (Domain 2)", "Splash / Auth / Profile", 
          "-------------------------", "[RASP Protection Engine]", "su / Magisk Root Probes", "QEMU / Emulator Tests",
          "TracerPid Debugger Probes", "Frida / Substrate Scanners", "APK Signature Validation", "SPKI Pinning & Token Guard",
          "Encrypted Keystore Storage"], "(Android 16 & iOS 17+)")

# 2. API Gateway
draw_box(28, 26, 21, 44, c_gw, c_gw_b, "API GATEWAY",
         ["Spring Cloud Gateway", "Netty Reactive Runtime", "ZeroTrustSecurityFilter", "Adaptive Band Enforcement",
          "JWT Verification & Claims", "Distributed Rate Limiter", "Input Sanitization Filter", "Security Header Injection",
          "Telemetry Forwarding", "TLS 1.3 Termination"], "(:8080 Edge Perimeter)")

# 3. Backend Microservices
draw_box(51, 26, 23, 44, c_ms, c_ms_b, "BACKEND SERVICES",
         ["Auth Service (:8081)", "User Service (:8082)", "Business Service (:8083)",
          "-------------------------", "[Threat Engine :8084]", "CrossLayerCorrelationEngine",
          "Rules RULE-CORR-01..06", "RiskScoringEngine (0-100)", "Half-Life Decay Attenuation",
          "Session Revocation Service", "Audit & Logging Service"], "(Spring Boot 3.2 Java 21)")

# 4. Data Layer
draw_box(76, 38, 20, 32, c_data, c_data_b, "DATA & STATE LAYER",
         ["PostgreSQL 16 Engine", "Users & RBAC Schema", "Security Events Table", "Correlation Audit Ledger",
          "-------------------------", "Redis 7.2 Cluster", "Token Hash Blacklist", "Sliding Window Rate Limits",
          "Device Risk State Cache"], "(ACID & In-Memory Cache)")

# 5. SOC Dashboard
draw_box(98, 42, 20, 28, '#ecfdf5', '#047857', "SOC ADMIN CONSOLE",
         ["React 18 + TypeScript", "Vite Production Bundle", "Live Incident Feed", "Cross-Layer Correlation View",
          "Adaptive Policy Configurator", "Ablation Analytics Page", "Interactive SOC Matrix"], "(:5173 Web Dashboard)")

# 6. Security & Monitoring Layer
draw_box(76, 20, 42, 16, c_sec, c_sec_b, "SECURITY MONITORING & TELEMETRY",
         ["Centralized Telemetry Pipeline", "Automated Security Event Hashing", "Prometheus Metrics & Micrometer",
          "Grafana Incident Dashboards", "AlertManager Webhook Triggers", "Immutable Security Audit Ledger"], "(SIEM & Telemetry)")

# 7. Cloud Infrastructure (Bottom Bar)
rect_cloud = patches.FancyBboxPatch((2, 3), 116, 14, boxstyle="round,pad=0.5,rounding_size=1.5",
                                   facecolor=c_cloud, edgecolor=c_cloud_b, linewidth=1.5)
ax.add_patch(rect_cloud)
ax.text(60, 15, "CLOUD-NATIVE DEPLOYMENT INFRASTRUCTURE & DEVSECOPS", ha='center', va='top', fontsize=9.5, fontweight='bold', color=c_cloud_b)
cloud_items = [
    "Docker Multi-Stage Containers", "Kubernetes Manifests (K8s)", "AWS ECS / Fargate", "AWS CloudWatch Logs",
    "Terraform IaC Scripts", "GitHub Actions CI/CD Pipeline", "SonarQube Static Analysis", "Trivy Container Scanning"
]
for idx, it in enumerate(cloud_items):
    col = idx % 4
    row = idx // 4
    ax.text(12 + col * 27, 10.5 - row * 3.5, f"✔ {it}", fontsize=7.5, fontweight='bold', color='#334155')

# Connecting Arrows
arrowprops = dict(arrowstyle='->', color='#475569', lw=1.5, mutation_scale=12)
ax.annotate('', xy=(28, 48), xytext=(26, 48), arrowprops=arrowprops)
ax.text(27, 49.5, "TLS 1.3\n+ JWT", ha='center', fontsize=6.5, fontweight='bold', color='#0284c7')

ax.annotate('', xy=(51, 48), xytext=(49, 48), arrowprops=arrowprops)
ax.text(50, 49.5, "Enforced\nProxy", ha='center', fontsize=6.5, fontweight='bold', color='#b45309')

ax.annotate('', xy=(76, 52), xytext=(74, 52), arrowprops=arrowprops)
ax.annotate('', xy=(98, 54), xytext=(96, 54), arrowprops=arrowprops)
ax.annotate('', xy=(76, 28), xytext=(65, 26), arrowprops=arrowprops)

plt.tight_layout()
plt.savefig('report/figures/figure4_1_system_architecture.png', dpi=300, bbox_inches='tight')
plt.close()

print('Generated architecture diagram successfully!')
