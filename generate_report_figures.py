import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

os.makedirs('report/figures', exist_ok=True)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['font.size'] = 10

# 1. Literature Publication Trend (Figure 2.2)
fig, ax = plt.subplots(figsize=(6, 3.5), dpi=300)
years = ['2021', '2022', '2023', '2024', '2025', '2026']
counts = [2, 0, 0, 2, 4, 2]
bars = ax.bar(years, counts, color='#881337', width=0.55, edgecolor='#4c0519', linewidth=1.2)
for bar in bars:
    yval = bar.get_height()
    if yval > 0:
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, int(yval), ha='center', va='bottom', fontsize=9, fontweight='bold')
ax.set_ylim(0, 5)
ax.set_xlabel('Publication Year', fontsize=11, fontweight='bold')
ax.set_ylabel('Number of Selected Papers', fontsize=11, fontweight='bold')
ax.set_title('Year-wise Distribution of Selected Research Papers (2021–2026)', fontsize=11, fontweight='bold')
ax.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('report/figures/figure2_2_publication_trend.png', dpi=300)
plt.close()

# 2. Literature Search Funnel (Figure 2.1)
fig, ax = plt.subplots(figsize=(7, 3.5), dpi=300)
stages = ['Final Deeply Reviewed', 'Highly Relevant Papers', 'Shortlisted Papers', 'Initial Database Hits']
vals = [10, 18, 32, 120]
colors = ['#881337', '#9f1239', '#be123c', '#e11d48']
y_pos = np.arange(len(stages))
bars = ax.barh(y_pos, vals, color=colors, height=0.55, edgecolor='#4c0519', linewidth=1)
for bar in bars:
    wval = bar.get_width()
    ax.text(wval + 2, bar.get_y() + bar.get_height()/2.0, f"{int(wval)} papers", ha='left', va='center', fontsize=9, fontweight='bold')
ax.set_yticks(y_pos)
ax.set_yticklabels(stages, fontsize=10, fontweight='bold')
ax.set_xlim(0, 145)
ax.set_xlabel('Number of Identified Academic Studies', fontsize=11, fontweight='bold')
ax.set_title('Academic Literature Screening & Selection Funnel (PRISMA Methodology)', fontsize=11, fontweight='bold')
ax.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('report/figures/figure2_1_literature_funnel.png', dpi=300)
plt.close()

# 3. Risk Scoring & Half-Life Decay Function (Figure 4.3)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=300)
# Subplot 1: Response Bands
bands = ['ALLOW\n(Score 0–24)', 'MONITOR\n(Score 25–49)', 'STEP-UP AUTH\n(Score 50–74)', 'RESTRICT ACTIONS\n(Score 75–100)']
band_vals = [24, 25, 25, 26]
band_colors = ['#10b981', '#f59e0b', '#f97316', '#dc2626']
ax1.pie(band_vals, labels=bands, colors=band_colors, autopct='%1.0f%%', startangle=140, 
        wedgeprops=dict(width=0.45, edgecolor='w', linewidth=2), textprops=dict(fontsize=9, fontweight='bold'))
ax1.set_title('Server-Side Adaptive Zero-Trust Bands', fontsize=11, fontweight='bold')

# Subplot 2: Exponential Half-Life Decay Curve
t = np.linspace(0, 60, 200) # minutes
half_life = 15 # minutes
lambda_val = np.log(2) / half_life
initial_score = 88
score_decay = initial_score * np.exp(-lambda_val * t)
ax2.plot(t, score_decay, color='#dc2626', linewidth=2.5, label='Active Decay (T1/2 = 15 min)')
ax2.axhline(75, color='#f97316', linestyle='--', label='Restrict Threshold (75)')
ax2.axhline(50, color='#f59e0b', linestyle='--', label='Step-Up Auth Threshold (50)')
ax2.axhline(25, color='#10b981', linestyle='--', label='Monitor Threshold (25)')
ax2.set_xlabel('Elapsed Time since Last Telemetry Event (Minutes)', fontsize=10, fontweight='bold')
ax2.set_ylabel('Calculated Risk Score (0–100)', fontsize=10, fontweight='bold')
ax2.set_title('Temporal Score Attenuation via Exponential Decay', fontsize=11, fontweight='bold')
ax2.legend(fontsize=8, loc='upper right')
ax2.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('report/figures/figure4_3_risk_scoring_bands.png', dpi=300)
plt.close()

# 4. Experimental Accuracy Across Configurations (Figure 5.1)
fig, ax = plt.subplots(figsize=(8, 4), dpi=300)
configs = ['Config A:\nAPI Only', 'Config B:\nMobile Only', 'Config C:\nIndependent', 'Config D:\nAppShieldX (Full)']
recall = [14.29, 14.29, 57.14, 85.71]
precision = [100.0, 100.0, 100.0, 100.0]
f1 = [25.0, 25.0, 72.73, 92.31]
x = np.arange(len(configs))
width = 0.25
rects1 = ax.bar(x - width, recall, width, label='Recall (%)', color='#0284c7', edgecolor='#0369a1')
rects2 = ax.bar(x, precision, width, label='Precision (%)', color='#10b981', edgecolor='#047857')
rects3 = ax.bar(x + width, f1, width, label='F1-Score (%)', color='#881337', edgecolor='#4c0519')
ax.set_ylabel('Percentage Metric Score (%)', fontsize=11, fontweight='bold')
ax.set_title('Cross-Layer Threat Detection Performance across Architectural Variants', fontsize=11, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(configs, fontsize=10, fontweight='bold')
ax.legend(fontsize=9, loc='lower right')
ax.set_ylim(0, 115)
for rects in [rects1, rects2, rects3]:
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2.0, h + 1.5, f"{h:.1f}%", ha='center', va='bottom', fontsize=8, fontweight='bold')
ax.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('report/figures/figure5_1_detection_accuracy.png', dpi=300)
plt.close()

# 5. Ablation Study Recall & FPR (Figure 5.2)
fig, ax1 = plt.subplots(figsize=(8.5, 4), dpi=300)
variants = ['V1: API Controls\nOnly', 'V2: API + Mobile\nTelemetry', 'V3: API + Correlation\n(No Adaptive)', 'V4: API + Isolated\nAdaptive', 'V5: Full AppShieldX\n(Proposed)']
recalls = [14.3, 14.3, 71.4, 57.1, 85.7]
fprs = [0.0, 0.0, 2.8, 0.0, 0.0]
x = np.arange(len(variants))
color = '#881337'
ax1.set_xlabel('Evaluated Architectural Variant', fontsize=11, fontweight='bold')
ax1.set_ylabel('Detection Recall (%)', color=color, fontsize=11, fontweight='bold')
bars1 = ax1.bar(x - 0.15, recalls, width=0.3, color=color, label='Recall (%)', edgecolor='#4c0519')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_ylim(0, 100)
for bar in bars1:
    h = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, h + 1, f"{h}%", ha='center', va='bottom', fontsize=8, fontweight='bold', color=color)

ax2 = ax1.twinx()
color2 = '#d97706'
ax2.set_ylabel('False Positive Rate (%)', color=color2, fontsize=11, fontweight='bold')
bars2 = ax2.bar(x + 0.15, fprs, width=0.3, color=color2, label='FPR (%)', edgecolor='#b45309')
ax2.tick_params(axis='y', labelcolor=color2)
ax2.set_ylim(0, 5)
for bar in bars2:
    h = bar.get_height()
    if h > 0:
        ax2.text(bar.get_x() + bar.get_width()/2.0, h + 0.1, f"{h}%", ha='center', va='bottom', fontsize=8, fontweight='bold', color=color2)

ax1.set_xticks(x)
ax1.set_xticklabels(variants, fontsize=9, fontweight='bold')
ax1.set_title('Ablation Study: Impact of Correlation & Adaptive Enforcement Components', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('report/figures/figure5_2_ablation_study.png', dpi=300)
plt.close()

# 6. Latency Overhead Distribution (Figure 5.3)
fig, ax = plt.subplots(figsize=(7, 3.8), dpi=300)
categories = ['V1: API Only', 'V2: Telemetry', 'V3: Correlation', 'V4: Isolated Adapt', 'V5: AppShieldX']
p50 = [3.51, 3.98, 1.72, 3.89, 3.76]
p95 = [4.19, 4.87, 2.45, 4.81, 4.71]
p99 = [5.12, 5.91, 3.10, 5.82, 5.64]
x = np.arange(len(categories))
width = 0.25
ax.bar(x - width, p50, width, label='Median (P50) Latency', color='#3b82f6')
ax.bar(x, p95, width, label='95th Percentile (P95)', color='#f59e0b')
ax.bar(x + width, p99, width, label='99th Percentile (P99)', color='#ef4444')
ax.set_ylabel('Latency Overhead (Milliseconds)', fontsize=11, fontweight='bold')
ax.set_title('Processing Latency Overhead Across Pipeline Components', fontsize=11, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=9, fontweight='bold')
ax.legend(fontsize=9, loc='upper right')
ax.set_ylim(0, 7.5)
ax.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('report/figures/figure5_3_latency_overhead.png', dpi=300)
plt.close()

print('Generated publication figures successfully!')
