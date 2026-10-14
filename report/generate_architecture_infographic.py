# -*- coding: utf-8 -*-
"""
AppShieldX Architecture Infographic Generator
Matches the user's reference diagram with:
- Authentic smartphone client mockup with screen UI & RASP badges
- API Gateway with modular capability cards & blue icons
- Backend Services with Spring Boot microservices & purple icons
- Data Layer with PostgreSQL 3D cylinder & Redis layered cache
- Security & Monitoring Layer (ELK, Analytics, AlertManager, SIEM)
- Desktop Admin Console monitor mockup with live charts
- Cloud Native Infrastructure linear pipeline at bottom
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, Arc, Rectangle

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "neat_diagrams"))
os.makedirs(OUT_DIR, exist_ok=True)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'Helvetica']

def draw_icon_box(ax, cx, cy, size, bg='#f8fafc', border='#cbd5e1'):
    """Draws a neat rounded container for an icon."""
    box = FancyBboxPatch((cx - size/2, cy - size/2), size, size,
                         boxstyle="round,pad=0.08,rounding_size=0.3",
                         facecolor=bg, edgecolor=border, lw=0.9)
    ax.add_patch(box)

def draw_shield(ax, cx, cy, r=1.0, color='#15803d', check=True):
    # Shield polygon
    pts = [
        [cx - r*0.7, cy + r*0.6],
        [cx + r*0.7, cy + r*0.6],
        [cx + r*0.7, cy],
        [cx, cy - r*0.8],
        [cx - r*0.7, cy]
    ]
    shield = Polygon(pts, closed=True, facecolor=color, edgecolor=color, lw=1)
    ax.add_patch(shield)
    if check:
        ax.plot([cx - r*0.35, cx - r*0.05, cx + r*0.4], [cy + r*0.05, cy - r*0.3, cy + r*0.35],
                color='#ffffff', lw=1.8, solid_capstyle='round')

def draw_lock(ax, cx, cy, r=1.0, color='#15803d'):
    # Shackle
    arc = Arc((cx, cy + r*0.25), r*0.7, r*0.8, angle=0, theta1=0, theta2=180, color=color, lw=1.8)
    ax.add_patch(arc)
    # Body
    body = FancyBboxPatch((cx - r*0.45, cy - r*0.55), r*0.9, r*0.7,
                          boxstyle="round,pad=0.04,rounding_size=0.15",
                          facecolor=color, edgecolor=color)
    ax.add_patch(body)
    # Keyhole
    ax.add_patch(Circle((cx, cy - r*0.15), r*0.12, facecolor='#ffffff', edgecolor='#ffffff'))

def draw_hash(ax, cx, cy, r=1.0, color='#15803d'):
    ax.text(cx, cy, "#", ha='center', va='center', fontsize=12, fontweight='bold', color=color)

def draw_phone_icon(ax, cx, cy, r=1.0, color='#15803d'):
    ph = FancyBboxPatch((cx - r*0.35, cy - r*0.65), r*0.7, r*1.3,
                        boxstyle="round,pad=0.04,rounding_size=0.15",
                        facecolor='none', edgecolor=color, lw=1.6)
    ax.add_patch(ph)
    # Screen inner line
    ax.plot([cx - r*0.2, cx + r*0.2], [cy + r*0.45, cy + r*0.45], color=color, lw=1)
    ax.add_patch(Circle((cx, cy - r*0.48), r*0.08, facecolor=color, edgecolor=color))

def draw_alien_mask(ax, cx, cy, r=1.0, color='#15803d'):
    # Stylized Frida alien/mask
    head = FancyBboxPatch((cx - r*0.6, cy - r*0.6), r*1.2, r*1.2,
                          boxstyle="round,pad=0.05,rounding_size=0.4",
                          facecolor=color, edgecolor=color)
    ax.add_patch(head)
    # Eyes
    ax.add_patch(Circle((cx - r*0.25, cy), r*0.15, facecolor='#ffffff'))
    ax.add_patch(Circle((cx + r*0.25, cy), r*0.15, facecolor='#ffffff'))
    # Horns/Antennae
    ax.plot([cx - r*0.4, cx - r*0.5], [cy + r*0.5, cy + r*0.75], color=color, lw=1.8)
    ax.plot([cx + r*0.4, cx + r*0.5], [cy + r*0.5, cy + r*0.75], color=color, lw=1.8)

def draw_bug_icon(ax, cx, cy, r=1.0, color='#15803d'):
    # Bug body
    ax.add_patch(Circle((cx, cy - r*0.1), r*0.4, facecolor=color, edgecolor=color))
    # Head
    ax.add_patch(Circle((cx, cy + r*0.35), r*0.22, facecolor=color, edgecolor=color))
    # Legs
    for dy in [-0.2, 0.0, 0.2]:
        ax.plot([cx - r*0.6, cx + r*0.6], [cy + dy, cy + dy], color=color, lw=1.5)
    # Antennae
    ax.plot([cx - r*0.1, cx - r*0.3], [cy + r*0.5, cy + r*0.75], color=color, lw=1.3)
    ax.plot([cx + r*0.1, cx + r*0.3], [cy + r*0.5, cy + r*0.75], color=color, lw=1.3)

def draw_code_icon(ax, cx, cy, r=1.0, color='#15803d'):
    ax.text(cx, cy, "</>", ha='center', va='center', fontsize=10, fontweight='bold', color=color)

def draw_routing_icon(ax, cx, cy, r=1.0, color='#2563eb'):
    # Split arrows
    ax.plot([cx, cx], [cy - r*0.5, cy], color=color, lw=1.8)
    ax.plot([cx - r*0.5, cx, cx + r*0.5], [cy + r*0.4, cy, cy + r*0.4], color=color, lw=1.8)
    ax.add_patch(Circle((cx, cy - r*0.5), r*0.12, facecolor=color))
    ax.add_patch(Circle((cx - r*0.5, cy + r*0.4), r*0.12, facecolor=color))
    ax.add_patch(Circle((cx + r*0.5, cy + r*0.4), r*0.12, facecolor=color))

def draw_gauge_icon(ax, cx, cy, r=1.0, color='#2563eb'):
    # Speedometer
    arc = Arc((cx, cy - r*0.1), r*1.2, r*1.2, angle=0, theta1=0, theta2=180, color=color, lw=1.8)
    ax.add_patch(arc)
    ax.plot([cx, cx + r*0.35], [cy - r*0.1, cy + r*0.25], color=color, lw=1.8)
    ax.add_patch(Circle((cx, cy - r*0.1), r*0.12, facecolor=color))

def draw_clipboard_icon(ax, cx, cy, r=1.0, color='#2563eb'):
    board = FancyBboxPatch((cx - r*0.45, cy - r*0.6), r*0.9, r*1.2,
                           boxstyle="round,pad=0.03,rounding_size=0.15",
                           facecolor='none', edgecolor=color, lw=1.6)
    ax.add_patch(board)
    clip = FancyBboxPatch((cx - r*0.25, cy + r*0.45), r*0.5, r*0.25,
                          boxstyle="round,pad=0.02,rounding_size=0.08",
                          facecolor=color, edgecolor=color)
    ax.add_patch(clip)
    # Checkmark inside
    ax.plot([cx - r*0.2, cx - r*0.05, cx + r*0.25], [cy, cy - r*0.2, cy + r*0.15],
            color=color, lw=1.5)

def draw_barchart_icon(ax, cx, cy, r=1.0, color='#2563eb'):
    # 3 vertical bars
    ax.add_patch(Rectangle((cx - r*0.45, cy - r*0.5), r*0.22, r*0.5, facecolor=color, edgecolor=color))
    ax.add_patch(Rectangle((cx - r*0.12, cy - r*0.5), r*0.22, r*0.9, facecolor=color, edgecolor=color))
    ax.add_patch(Rectangle((cx + r*0.21, cy - r*0.5), r*0.22, r*0.7, facecolor=color, edgecolor=color))

def draw_users_icon(ax, cx, cy, r=1.0, color='#9333ea'):
    # Front user
    ax.add_patch(Circle((cx - r*0.15, cy + r*0.2), r*0.22, facecolor=color))
    arc1 = Arc((cx - r*0.15, cy - r*0.3), r*0.6, r*0.6, angle=0, theta1=0, theta2=180, color=color, lw=2.2)
    ax.add_patch(arc1)
    # Back user
    ax.add_patch(Circle((cx + r*0.25, cy + r*0.3), r*0.18, facecolor=color, alpha=0.7))
    arc2 = Arc((cx + r*0.25, cy - r*0.2), r*0.5, r*0.5, angle=0, theta1=0, theta2=180, color=color, lw=1.8, alpha=0.7)
    ax.add_patch(arc2)

def draw_single_user_icon(ax, cx, cy, r=1.0, color='#9333ea'):
    ax.add_patch(Circle((cx, cy + r*0.25), r*0.26, facecolor=color))
    arc = Arc((cx, cy - r*0.3), r*0.75, r*0.75, angle=0, theta1=0, theta2=180, color=color, lw=2.5)
    ax.add_patch(arc)

def draw_briefcase_icon(ax, cx, cy, r=1.0, color='#9333ea'):
    # Handle
    arc = Arc((cx, cy + r*0.3), r*0.4, r*0.35, angle=0, theta1=0, theta2=180, color=color, lw=1.6)
    ax.add_patch(arc)
    # Case body
    case = FancyBboxPatch((cx - r*0.6, cy - r*0.45), r*1.2, r*0.8,
                          boxstyle="round,pad=0.04,rounding_size=0.15",
                          facecolor=color, edgecolor=color)
    ax.add_patch(case)
    ax.plot([cx - r*0.6, cx + r*0.6], [cy, cy], color='#ffffff', lw=1.0)

def draw_warning_icon(ax, cx, cy, r=1.0, color='#dc2626'):
    # Warning triangle
    pts = [[cx, cy + r*0.7], [cx - r*0.7, cy - r*0.5], [cx + r*0.7, cy - r*0.5]]
    tri = Polygon(pts, closed=True, facecolor=color, edgecolor=color)
    ax.add_patch(tri)
    ax.text(cx, cy - r*0.05, "!", ha='center', va='center', fontsize=11, fontweight='bold', color='#ffffff')

def draw_doc_icon(ax, cx, cy, r=1.0, color='#9333ea'):
    doc = FancyBboxPatch((cx - r*0.4, cy - r*0.6), r*0.8, r*1.2,
                         boxstyle="round,pad=0.03,rounding_size=0.1",
                         facecolor=color, edgecolor=color)
    ax.add_patch(doc)
    # Lines
    for dy in [-0.2, 0.0, 0.2]:
        ax.plot([cx - r*0.22, cx + r*0.22], [cy + dy, cy + dy], color='#ffffff', lw=1.2)

def draw_database_3d(ax, cx, cy, w=4.5, h=5.5, color='#0284c7'):
    # 3 stacked cylinders
    for i, dy in enumerate([-h*0.3, 0, h*0.3]):
        # Cylinder body
        rect = Rectangle((cx - w/2, cy + dy - h*0.15), w, h*0.22, facecolor=color, edgecolor=color)
        ax.add_patch(rect)
        # Bottom ellipse arc
        arc = Arc((cx, cy + dy - h*0.15), w, h*0.25, angle=0, theta1=180, theta2=360, color='#0369a1', lw=1.5)
        ax.add_patch(arc)
        # Top ellipse cap
        top_cap = patches.Ellipse((cx, cy + dy + h*0.07), w, h*0.25, facecolor='#38bdf8', edgecolor='#0369a1', lw=1.2)
        ax.add_patch(top_cap)

def draw_redis_layers(ax, cx, cy, w=4.5, h=5.5, color='#dc2626'):
    # 3 stacked red diamond layers
    for i, dy in enumerate([-h*0.28, 0, h*0.28]):
        pts = [
            [cx, cy + dy + h*0.16],
            [cx + w/2, cy + dy],
            [cx, cy + dy - h*0.16],
            [cx - w/2, cy + dy]
        ]
        poly = Polygon(pts, closed=True, facecolor='#ef4444' if i==2 else color, edgecolor='#b91c1c', lw=1.2)
        ax.add_patch(poly)

def draw_elk_emblem(ax, cx, cy, r=1.0):
    colors = ['#f59e0b', '#06b6d4', '#10b981', '#ec4899']
    for i, col in enumerate(colors):
        theta1 = i * 90
        theta2 = (i + 1) * 90
        wedge = patches.Wedge((cx, cy), r*0.6, theta1, theta2, width=r*0.3, facecolor=col, edgecolor='#ffffff')
        ax.add_patch(wedge)

def draw_trend_icon(ax, cx, cy, r=1.0, color='#0f172a'):
    # Graph axes + zigzag line
    ax.plot([cx - r*0.5, cx - r*0.5, cx + r*0.5], [cy + r*0.5, cy - r*0.5, cy - r*0.5], color=color, lw=1.3)
    ax.plot([cx - r*0.4, cx - r*0.1, cx + r*0.1, cx + r*0.4], [cy - r*0.3, cy + r*0.1, cy - r*0.1, cy + r*0.4],
            color='#dc2626', lw=1.6)

def draw_bell_icon(ax, cx, cy, r=1.0, color='#dc2626'):
    # Bell dome
    pts = [
        [cx - r*0.5, cy - r*0.3],
        [cx - r*0.35, cy + r*0.3],
        [cx + r*0.35, cy + r*0.3],
        [cx + r*0.5, cy - r*0.3]
    ]
    ax.add_patch(Polygon(pts, closed=True, facecolor=color, edgecolor=color))
    # Clapper
    ax.add_patch(Circle((cx, cy - r*0.42), r*0.14, facecolor=color))

def draw_docker_whale(ax, cx, cy, r=1.5, color='#0284c7'):
    # Whale body
    body = patches.Ellipse((cx, cy - r*0.2), r*1.6, r*0.9, facecolor=color, edgecolor=color)
    ax.add_patch(body)
    # Tail
    ax.plot([cx + r*0.7, cx + r*1.1, cx + r*0.9], [cy - r*0.1, cy + r*0.4, cy - r*0.1], color=color, lw=2.5)
    # Containers on back (3x2 blocks)
    for bx in [-r*0.5, -r*0.2, r*0.1]:
        ax.add_patch(Rectangle((cx + bx, cy + r*0.1), r*0.24, r*0.22, facecolor='#38bdf8', edgecolor='#0284c7', lw=0.8))
        ax.add_patch(Rectangle((cx + bx, cy + r*0.35), r*0.24, r*0.22, facecolor='#38bdf8', edgecolor='#0284c7', lw=0.8))

def draw_k8s_wheel(ax, cx, cy, r=1.5, color='#2563eb'):
    # Helm wheel hub
    ax.add_patch(Circle((cx, cy), r*0.7, facecolor='none', edgecolor=color, lw=2.2))
    ax.add_patch(Circle((cx, cy), r*0.25, facecolor=color, edgecolor=color))
    # Spokes
    for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
        x2 = cx + r*0.9 * np.cos(angle)
        y2 = cy + r*0.9 * np.sin(angle)
        ax.plot([cx, x2], [cy, y2], color=color, lw=2.0)

def draw_cloud_icon(ax, cx, cy, r=1.5, color='#0284c7'):
    # Fluffy cloud composed of 3 overlapping circles
    ax.add_patch(Circle((cx - r*0.4, cy - r*0.1), r*0.5, facecolor='#38bdf8', edgecolor=color, lw=1.5))
    ax.add_patch(Circle((cx + r*0.4, cy - r*0.1), r*0.5, facecolor='#38bdf8', edgecolor=color, lw=1.5))
    ax.add_patch(Circle((cx, cy + r*0.2), r*0.65, facecolor='#38bdf8', edgecolor=color, lw=1.5))
    ax.add_patch(Rectangle((cx - r*0.6, cy - r*0.5), r*1.2, r*0.5, facecolor='#38bdf8', edgecolor='#38bdf8'))
    ax.plot([cx - r*0.6, cx + r*0.6], [cy - r*0.5, cy - r*0.5], color=color, lw=1.5)

def draw_cicd_pipeline(ax, cx, cy, r=1.5, color='#2563eb'):
    # 3 interconnected nodes
    p1 = (cx - r*0.6, cy)
    p2 = (cx, cy + r*0.4)
    p3 = (cx + r*0.6, cy)
    ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color=color, lw=2.0)
    ax.plot([p1[0], p3[0]], [p1[1], p3[1]], color=color, lw=2.0)
    for p in [p1, p2, p3]:
        ax.add_patch(Circle(p, r*0.22, facecolor='#38bdf8', edgecolor=color, lw=1.8))

def draw_flame_icon(ax, cx, cy, r=1.5, color='#ea580c'):
    # Prometheus flame
    pts = [
        [cx, cy + r*0.8],
        [cx + r*0.6, cy],
        [cx + r*0.4, cy - r*0.6],
        [cx, cy - r*0.4],
        [cx - r*0.4, cy - r*0.6],
        [cx - r*0.6, cy]
    ]
    ax.add_patch(Polygon(pts, closed=True, facecolor=color, edgecolor=color))
    # Inner flame
    pts_in = [
        [cx, cy + r*0.3],
        [cx + r*0.25, cy - r*0.1],
        [cx, cy - r*0.3],
        [cx - r*0.25, cy - r*0.1]
    ]
    ax.add_patch(Polygon(pts_in, closed=True, facecolor='#fde047', edgecolor='#fde047'))


def generate_architecture_infographic():
    fig, ax = plt.subplots(figsize=(19, 12.5), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 105)
    ax.axis('off')

    # =========================================================================
    # MAIN HEADER
    # =========================================================================
    ax.text(80, 101.5, "A Cloud Native Runtime Protection and API Security Framework",
            ha='center', va='center', fontsize=18, fontweight='bold', color='#0f172a')
    ax.text(80, 98.0, "for Client-Server Android Applications",
            ha='center', va='center', fontsize=15, fontweight='bold', color='#1e293b')

    # =========================================================================
    # 1. ANDROID APPLICATION CONTAINER (GREEN)
    # =========================================================================
    card_android = FancyBboxPatch((3.5, 36), 44.5, 59, boxstyle="round,pad=0.5,rounding_size=2.0",
                                  facecolor='#f0fdf4', edgecolor='#22c55e', lw=1.8)
    ax.add_patch(card_android)
    ax.text(25.75, 92.5, "ANDROID APPLICATION", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#15803d')

    # --- 1A. SMARTPHONE MOCKUP ---
    phone_x, phone_y, phone_w, phone_h = 5.5, 49.5, 18.0, 40.5
    # Bezel
    phone_outer = FancyBboxPatch((phone_x, phone_y), phone_w, phone_h,
                                 boxstyle="round,pad=0.4,rounding_size=2.2",
                                 facecolor='#0f172a', edgecolor='#334155', lw=2.2)
    ax.add_patch(phone_outer)
    # Screen
    screen = FancyBboxPatch((phone_x + 1.0, phone_y + 1.2), phone_w - 2.0, phone_h - 2.4,
                            boxstyle="round,pad=0.3,rounding_size=1.6",
                            facecolor='#ffffff', edgecolor='#0f172a', lw=1.0)
    ax.add_patch(screen)
    # Camera punch hole
    ax.add_patch(Circle((phone_x + phone_w/2, phone_y + phone_h - 2.5), 0.55, facecolor='#0f172a'))
    # Status bar
    ax.text(phone_x + 2.2, phone_y + phone_h - 2.5, "9:41", fontsize=7.5, fontweight='bold', color='#0f172a')
    ax.plot([phone_x + phone_w - 4.5, phone_x + phone_w - 2.5], [phone_y + phone_h - 2.5, phone_y + phone_h - 2.5],
            color='#0f172a', lw=1.8)

    # Phone screen content
    draw_shield(ax, phone_x + phone_w/2, phone_y + phone_h - 7.5, r=1.6, color='#1e3a8a', check=False)
    draw_lock(ax, phone_x + phone_w/2, phone_y + phone_h - 7.5, r=0.9, color='#ffffff')
    ax.text(phone_x + phone_w/2, phone_y + phone_h - 11.2, "Secure App", ha='center', va='center',
            fontsize=9.5, fontweight='bold', color='#0f172a')

    # 5 Phone Menu buttons
    menu_items = [
        ("Login", "user"),
        ("Dashboard", "lock"),
        ("Profile", "user"),
        ("Settings", "gear"),
        ("Logout", "logout")
    ]
    btn_y = phone_y + phone_h - 15.0
    for label, icon_type in menu_items:
        btn = FancyBboxPatch((phone_x + 2.2, btn_y - 1.2), phone_w - 4.4, 2.7,
                             boxstyle="round,pad=0.15,rounding_size=0.5",
                             facecolor='#f8fafc', edgecolor='#cbd5e1', lw=0.9)
        ax.add_patch(btn)
        # Icon
        if icon_type == "user":
            draw_single_user_icon(ax, phone_x + 4.0, btn_y + 0.1, r=0.6, color='#334155')
        elif icon_type == "lock":
            draw_lock(ax, phone_x + 4.0, btn_y + 0.1, r=0.6, color='#334155')
        elif icon_type == "gear":
            draw_gauge_icon(ax, phone_x + 4.0, btn_y + 0.1, r=0.6, color='#334155')
        elif icon_type == "logout":
            ax.plot([phone_x + 3.5, phone_x + 4.5], [btn_y + 0.1, btn_y + 0.1], color='#334155', lw=1.5)
            ax.plot([phone_x + 4.2, phone_x + 4.5, phone_x + 4.2], [btn_y + 0.4, btn_y + 0.1, btn_y - 0.2], color='#334155', lw=1.5)
        ax.text(phone_x + 6.2, btn_y + 0.1, label, ha='left', va='center', fontsize=8.2, fontweight='bold', color='#1e293b')
        btn_y -= 4.2

    # --- 1B. RUNTIME PROTECTION MODULE ---
    box_rpm = FancyBboxPatch((25.5, 49.5), 21.0, 40.5, boxstyle="round,pad=0.3,rounding_size=1.2",
                             facecolor='#f0fdf4', edgecolor='#16a34a', lw=1.4, ls='--')
    ax.add_patch(box_rpm)
    ax.text(36.0, 87.5, "RUNTIME PROTECTION\nMODULE", ha='center', va='center',
            fontsize=8.5, fontweight='bold', color='#15803d')

    rpm_cards = [
        ("Root Detection", "hash"),
        ("Emulator Detection", "phone"),
        ("Frida Detection", "frida"),
        ("Debugger Detection", "bug"),
        ("Integrity Check", "shield"),
        ("SSL Pinning", "lock"),
        ("Code Tamper Detection", "code")
    ]
    card_y = 82.5
    for text, itype in rpm_cards:
        c_patch = FancyBboxPatch((26.8, card_y - 1.4), 18.4, 3.2,
                                 boxstyle="round,pad=0.15,rounding_size=0.6",
                                 facecolor='#ffffff', edgecolor='#bbf7d0', lw=1.0)
        ax.add_patch(c_patch)
        draw_icon_box(ax, 28.5, card_y + 0.2, size=1.8, bg='#dcfce7', border='#86efac')
        if itype == "hash":
            draw_hash(ax, 28.5, card_y + 0.2, r=0.7, color='#15803d')
        elif itype == "phone":
            draw_phone_icon(ax, 28.5, card_y + 0.2, r=0.7, color='#15803d')
        elif itype == "frida":
            draw_alien_mask(ax, 28.5, card_y + 0.2, r=0.7, color='#15803d')
        elif itype == "bug":
            draw_bug_icon(ax, 28.5, card_y + 0.2, r=0.7, color='#15803d')
        elif itype == "shield":
            draw_shield(ax, 28.5, card_y + 0.2, r=0.7, color='#15803d')
        elif itype == "lock":
            draw_lock(ax, 28.5, card_y + 0.2, r=0.7, color='#15803d')
        elif itype == "code":
            draw_code_icon(ax, 28.5, card_y + 0.2, r=0.7, color='#15803d')
        ax.text(30.6, card_y + 0.2, text, ha='left', va='center', fontsize=7.8, fontweight='bold', color='#1e293b')
        card_y -= 4.7

    # --- 1C. SECURE STORAGE ---
    box_ss = FancyBboxPatch((5.5, 37.5), 41.0, 9.8, boxstyle="round,pad=0.3,rounding_size=1.2",
                            facecolor='#f0fdf4', edgecolor='#16a34a', lw=1.4, ls='--')
    ax.add_patch(box_ss)
    ax.text(26.0, 45.2, "SECURE STORAGE", ha='center', va='center',
            fontsize=8.5, fontweight='bold', color='#15803d')

    # SharedPreferences Card
    sp_patch = FancyBboxPatch((6.8, 41.2), 38.4, 2.7, boxstyle="round,pad=0.15,rounding_size=0.5",
                              facecolor='#ffffff', edgecolor='#bbf7d0', lw=1.0)
    ax.add_patch(sp_patch)
    draw_lock(ax, 8.8, 42.55, r=0.65, color='#15803d')
    ax.text(11.0, 42.55, "Encrypted SharedPreferences", ha='left', va='center', fontsize=8.0, fontweight='bold', color='#1e293b')

    # Android Keystore Card
    ks_patch = FancyBboxPatch((6.8, 38.2), 38.4, 2.7, boxstyle="round,pad=0.15,rounding_size=0.5",
                              facecolor='#ffffff', edgecolor='#bbf7d0', lw=1.0)
    ax.add_patch(ks_patch)
    draw_shield(ax, 8.8, 39.55, r=0.65, color='#15803d')
    ax.text(11.0, 39.55, "Android Keystore", ha='left', va='center', fontsize=8.0, fontweight='bold', color='#1e293b')


    # =========================================================================
    # NETWORK LINK (HTTPS TLS 1.3 / JWT)
    # =========================================================================
    net_arr = patches.FancyArrowPatch((48.0, 65.5), (57.5, 65.5), arrowstyle='<->',
                                      mutation_scale=16, lw=2.2, color='#0f172a')
    ax.add_patch(net_arr)
    # Lock pill
    lock_pill = FancyBboxPatch((50.8, 68.2), 4.0, 4.0, boxstyle="round,pad=0.1,rounding_size=0.6",
                               facecolor='#1e293b', edgecolor='#0f172a', lw=1.0)
    ax.add_patch(lock_pill)
    draw_lock(ax, 52.8, 70.2, r=1.0, color='#ffffff')
    ax.text(52.8, 64.0, "HTTPS\nTLS 1.3", ha='center', va='top', fontsize=7.8, fontweight='bold', color='#0f172a')
    ax.text(52.8, 58.5, "JWT\nAccess Token", ha='center', va='top', fontsize=7.5, fontweight='bold', color='#0f172a')


    # =========================================================================
    # 2. API GATEWAY CONTAINER (BLUE)
    # =========================================================================
    card_gw = FancyBboxPatch((57.5, 36), 26.5, 59, boxstyle="round,pad=0.5,rounding_size=2.0",
                             facecolor='#eff6ff', edgecolor='#3b82f6', lw=1.8)
    ax.add_patch(card_gw)
    ax.text(70.75, 92.5, "API GATEWAY", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#1d4ed8')
    ax.text(70.75, 90.0, "(Spring Cloud Gateway)", ha='center', va='center',
            fontsize=9.0, fontstyle='italic', color='#2563eb')

    gw_items = [
        ("Request Routing", "routing"),
        ("Authentication &\nAuthorization", "auth"),
        ("Rate Limiting", "rate"),
        ("Request Validation", "val"),
        ("Security Headers", "headers"),
        ("Logging & Monitoring", "log")
    ]
    gw_y = 83.5
    for text, itype in gw_items:
        h_box = 4.8 if "\n" in text else 4.2
        patch = FancyBboxPatch((59.2, gw_y - h_box/2), 23.1, h_box,
                               boxstyle="round,pad=0.15,rounding_size=0.8",
                               facecolor='#ffffff', edgecolor='#bfdbfe', lw=1.0)
        ax.add_patch(patch)
        draw_icon_box(ax, 61.8, gw_y, size=2.6, bg='#dbeafe', border='#93c5fd')
        if itype == "routing":
            draw_routing_icon(ax, 61.8, gw_y, r=0.9, color='#1d4ed8')
        elif itype == "auth":
            draw_shield(ax, 61.8, gw_y, r=0.9, color='#1d4ed8')
        elif itype == "rate":
            draw_gauge_icon(ax, 61.8, gw_y, r=0.9, color='#1d4ed8')
        elif itype == "val":
            draw_clipboard_icon(ax, 61.8, gw_y, r=0.9, color='#1d4ed8')
        elif itype == "headers":
            draw_shield(ax, 61.8, gw_y, r=0.9, color='#1d4ed8')
        elif itype == "log":
            draw_barchart_icon(ax, 61.8, gw_y, r=0.9, color='#1d4ed8')
        ax.text(64.8, gw_y, text, ha='left', va='center', fontsize=8.0, fontweight='bold', color='#1e293b')
        gw_y -= 7.4


    # =========================================================================
    # ARROW: API GATEWAY -> BACKEND SERVICES
    # =========================================================================
    arr_gw_be = patches.FancyArrowPatch((84.0, 65.5), (90.0, 65.5), arrowstyle='->',
                                        mutation_scale=16, lw=2.2, color='#0f172a')
    ax.add_patch(arr_gw_be)


    # =========================================================================
    # 3. BACKEND SERVICES CONTAINER (PURPLE)
    # =========================================================================
    card_be = FancyBboxPatch((90.0, 36), 33.5, 59, boxstyle="round,pad=0.5,rounding_size=2.0",
                            facecolor='#faf5ff', edgecolor='#a855f7', lw=1.8)
    ax.add_patch(card_be)
    ax.text(106.75, 92.5, "BACKEND SERVICES", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#7e22ce')
    ax.text(106.75, 90.0, "(Spring Boot Microservices)", ha='center', va='center',
            fontsize=9.0, fontstyle='italic', color='#9333ea')

    be_items = [
        ("Auth Service", "(Login, Register, Token)", "users"),
        ("User Service", "(Profile, Preferences)", "user"),
        ("Business Service", "(App Functionalities)", "case"),
        ("Threat Detection Service", "(Runtime & API Events)", "warn"),
        ("Audit & Logging Service", "(Logs, Alerts)", "doc")
    ]
    be_y = 82.5
    for title, sub, itype in be_items:
        patch = FancyBboxPatch((92.0, be_y - 2.8), 29.5, 5.8,
                               boxstyle="round,pad=0.15,rounding_size=0.8",
                               facecolor='#ffffff', edgecolor='#e9d5ff', lw=1.0)
        ax.add_patch(patch)
        draw_icon_box(ax, 95.0, be_y + 0.1, size=3.0, bg='#f3e8ff', border='#d8b4fe')
        if itype == "users":
            draw_users_icon(ax, 95.0, be_y + 0.1, r=1.0, color='#7e22ce')
        elif itype == "user":
            draw_single_user_icon(ax, 95.0, be_y + 0.1, r=1.0, color='#7e22ce')
        elif itype == "case":
            draw_briefcase_icon(ax, 95.0, be_y + 0.1, r=1.0, color='#7e22ce')
        elif itype == "warn":
            draw_warning_icon(ax, 95.0, be_y + 0.1, r=1.0, color='#dc2626')
        elif itype == "doc":
            draw_doc_icon(ax, 95.0, be_y + 0.1, r=1.0, color='#7e22ce')

        ax.text(98.5, be_y + 1.1, title, ha='left', va='center', fontsize=8.8, fontweight='bold', color='#1e293b')
        ax.text(98.5, be_y - 1.1, sub, ha='left', va='center', fontsize=7.6, color='#64748b')
        be_y -= 9.0


    # =========================================================================
    # ARROW: BACKEND SERVICES <-> DATA LAYER
    # =========================================================================
    arr_be_db = patches.FancyArrowPatch((123.5, 65.5), (129.5, 65.5), arrowstyle='<->',
                                        mutation_scale=16, lw=2.2, color='#0f172a')
    ax.add_patch(arr_be_db)


    # =========================================================================
    # 4. DATA LAYER CONTAINER (GOLD / YELLOW)
    # =========================================================================
    card_data = FancyBboxPatch((129.5, 41.5), 26.5, 53.5, boxstyle="round,pad=0.5,rounding_size=2.0",
                               facecolor='#fffbeb', edgecolor='#f59e0b', lw=1.8)
    ax.add_patch(card_data)
    ax.text(142.75, 92.5, "DATA LAYER", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#b45309')

    # --- 4A. DATABASE (PostgreSQL) ---
    db_box = FancyBboxPatch((131.0, 68.0), 23.5, 21.0, boxstyle="round,pad=0.3,rounding_size=1.0",
                            facecolor='#ffffff', edgecolor='#fed7aa', lw=1.2)
    ax.add_patch(db_box)
    ax.text(142.75, 86.8, "DATABASE", ha='center', va='center', fontsize=8.8, fontweight='bold', color='#1e293b')
    ax.text(142.75, 84.8, "(PostgreSQL)", ha='center', va='center', fontsize=7.8, color='#64748b')
    draw_database_3d(ax, 136.0, 75.5, w=5.2, h=5.8, color='#0284c7')

    db_bullets = ["• Users", "• Roles", "• Tokens", "• App Data", "• Logs"]
    by = 79.5
    for bul in db_bullets:
        ax.text(140.5, by, bul, ha='left', va='center', fontsize=7.6, fontweight='bold', color='#334155')
        by -= 2.0

    # --- 4B. CACHE / SESSION STORE (Redis) ---
    cache_box = FancyBboxPatch((131.0, 43.5), 23.5, 22.0, boxstyle="round,pad=0.3,rounding_size=1.0",
                               facecolor='#ffffff', edgecolor='#fed7aa', lw=1.2)
    ax.add_patch(cache_box)
    ax.text(142.75, 63.2, "CACHE / SESSION STORE", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1e293b')
    ax.text(142.75, 61.2, "(Redis)", ha='center', va='center', fontsize=7.8, color='#64748b')
    draw_redis_layers(ax, 136.0, 52.0, w=5.2, h=5.5, color='#dc2626')

    cache_bullets = ["• Sessions", "• Tokens", "• Rate Limit Data", "• Blacklists"]
    cy = 56.5
    for bul in cache_bullets:
        ax.text(140.5, cy, bul, ha='left', va='center', fontsize=7.6, fontweight='bold', color='#334155')
        cy -= 2.2


    # =========================================================================
    # CONNECTOR DOWN FROM BACKEND SERVICES TO LOWER LAYERS
    # =========================================================================
    ax.plot([106.75, 106.75], [36.0, 32.5], color='#0f172a', lw=1.8)
    ax.plot([65.0, 142.5], [32.5, 32.5], color='#0f172a', lw=1.8)
    # Down to Security Layer
    ax.plot([65.0, 65.0], [32.5, 30.5], color='#0f172a', lw=1.8)
    arr_down_sec = patches.FancyArrowPatch((65.0, 32.5), (65.0, 30.5), arrowstyle='->',
                                          mutation_scale=12, lw=1.8, color='#0f172a')
    ax.add_patch(arr_down_sec)
    # Down to Dashboard
    arr_down_dash = patches.FancyArrowPatch((142.5, 32.5), (142.5, 31.0), arrowstyle='->',
                                           mutation_scale=12, lw=1.8, color='#0f172a')
    ax.add_patch(arr_down_dash)


    # =========================================================================
    # 5. SECURITY & MONITORING LAYER CONTAINER (RED DASHED)
    # =========================================================================
    card_sec = FancyBboxPatch((42.0, 17.5), 76.5, 13.0, boxstyle="round,pad=0.4,rounding_size=1.5",
                              facecolor='#fef2f2', edgecolor='#ef4444', lw=1.5, ls='--')
    ax.add_patch(card_sec)
    ax.text(80.25, 28.8, "SECURITY & MONITORING LAYER", ha='center', va='center',
            fontsize=10.0, fontweight='bold', color='#b91c1c')

    sec_items = [
        ("Centralized\nLogging\n(ELK Stack)", "elk"),
        ("Security\nAnalytics\n(Anomaly Detection)", "trend"),
        ("Alert Manager\n(Email / SMS /\nWebhook)", "bell"),
        ("SIEM\nIntegration\n(Optional)", "siem")
    ]
    sx = 44.5
    for title, itype in sec_items:
        patch = FancyBboxPatch((sx, 18.5), 17.2, 8.5, boxstyle="round,pad=0.15,rounding_size=0.6",
                               facecolor='#ffffff', edgecolor='#fecaca', lw=1.0)
        ax.add_patch(patch)
        draw_icon_box(ax, sx + 2.6, 22.75, size=2.8, bg='#f8fafc', border='#e2e8f0')
        if itype == "elk":
            draw_elk_emblem(ax, sx + 2.6, 22.75, r=1.1)
        elif itype == "trend":
            draw_trend_icon(ax, sx + 2.6, 22.75, r=1.0)
        elif itype == "bell":
            draw_bell_icon(ax, sx + 2.6, 22.75, r=1.0)
        elif itype == "siem":
            draw_shield(ax, sx + 2.6, 22.75, r=1.0, color='#2563eb')
        ax.text(sx + 5.2, 22.75, title, ha='left', va='center', fontsize=7.2, fontweight='bold', color='#1e293b')
        sx += 18.8


def draw_grafana_swirl(ax, cx, cy, r=1.5):
    # Grafana orange flower/swirl
    colors = ['#f97316', '#ea580c', '#fb923c', '#fdba74']
    for i, col in enumerate(colors):
        angle = i * (360 / len(colors))
        rad = np.radians(angle)
        px = cx + r*0.35 * np.cos(rad)
        py = cy + r*0.35 * np.sin(rad)
        ax.add_patch(Circle((px, py), r*0.3, facecolor=col, edgecolor='#ffffff', lw=0.5))
    ax.add_patch(Circle((cx, cy), r*0.2, facecolor='#ffffff', edgecolor='#ea580c', lw=0.8))

def generate_architecture_infographic():
    fig, ax = plt.subplots(figsize=(20, 13.5), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 160)
    ax.set_ylim(-1, 107)
    ax.axis('off')

    # =========================================================================
    # MAIN HEADER
    # =========================================================================
    ax.text(80, 103.5, "A Cloud Native Runtime Protection and API Security Framework",
            ha='center', va='center', fontsize=19, fontweight='bold', color='#0f172a')
    ax.text(80, 100.0, "for Client-Server Android Applications",
            ha='center', va='center', fontsize=16, fontweight='bold', color='#1e293b')

    # =========================================================================
    # 1. ANDROID APPLICATION CONTAINER (GREEN)
    # =========================================================================
    card_android = FancyBboxPatch((3.5, 38.0), 44.5, 59.0, boxstyle="round,pad=0.5,rounding_size=2.0",
                                  facecolor='#f0fdf4', edgecolor='#22c55e', lw=1.8)
    ax.add_patch(card_android)
    ax.text(25.75, 94.5, "ANDROID APPLICATION", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#15803d')

    # --- 1A. SMARTPHONE MOCKUP ---
    phone_x, phone_y, phone_w, phone_h = 5.5, 51.5, 18.0, 40.5
    # Bezel
    phone_outer = FancyBboxPatch((phone_x, phone_y), phone_w, phone_h,
                                 boxstyle="round,pad=0.4,rounding_size=2.2",
                                 facecolor='#0f172a', edgecolor='#334155', lw=2.2)
    ax.add_patch(phone_outer)
    # Screen
    screen = FancyBboxPatch((phone_x + 1.0, phone_y + 1.2), phone_w - 2.0, phone_h - 2.4,
                            boxstyle="round,pad=0.3,rounding_size=1.6",
                            facecolor='#ffffff', edgecolor='#0f172a', lw=1.0)
    ax.add_patch(screen)
    # Camera punch hole & Speaker
    ax.add_patch(Circle((phone_x + phone_w/2 - 2.2, phone_y + phone_h - 2.5), 0.55, facecolor='#0f172a'))
    ax.plot([phone_x + phone_w/2 - 0.5, phone_x + phone_w/2 + 2.5], [phone_y + phone_h - 2.5, phone_y + phone_h - 2.5],
            color='#0f172a', lw=1.8, solid_capstyle='round')
    # Status bar (9:41, wifi, battery)
    ax.text(phone_x + 2.2, phone_y + phone_h - 2.5, "9:41", fontsize=7.5, fontweight='bold', color='#0f172a')
    # Battery icon
    ax.add_patch(Rectangle((phone_x + phone_w - 4.2, phone_y + phone_h - 3.1), 2.2, 1.2,
                           facecolor='none', edgecolor='#0f172a', lw=1.0))
    ax.add_patch(Rectangle((phone_x + phone_w - 4.0, phone_y + phone_h - 2.9), 1.5, 0.8,
                           facecolor='#0f172a', edgecolor='none'))
    ax.plot([phone_x + phone_w - 1.9, phone_x + phone_w - 1.9], [phone_y + phone_h - 2.8, phone_y + phone_h - 2.2],
            color='#0f172a', lw=1.2)

    # Phone screen content
    draw_shield(ax, phone_x + phone_w/2, phone_y + phone_h - 7.8, r=1.6, color='#1e3a8a', check=False)
    draw_lock(ax, phone_x + phone_w/2, phone_y + phone_h - 7.8, r=0.9, color='#ffffff')
    ax.text(phone_x + phone_w/2, phone_y + phone_h - 11.4, "Secure App", ha='center', va='center',
            fontsize=9.5, fontweight='bold', color='#0f172a')

    # 5 Phone Menu buttons
    menu_items = [
        ("Login", "user"),
        ("Dashboard", "lock"),
        ("Profile", "user"),
        ("Settings", "gear"),
        ("Logout", "logout")
    ]
    btn_y = phone_y + phone_h - 15.2
    for label, icon_type in menu_items:
        btn = FancyBboxPatch((phone_x + 2.2, btn_y - 1.2), phone_w - 4.4, 2.7,
                             boxstyle="round,pad=0.15,rounding_size=0.5",
                             facecolor='#f8fafc', edgecolor='#cbd5e1', lw=0.9)
        ax.add_patch(btn)
        # Icon
        if icon_type == "user":
            draw_single_user_icon(ax, phone_x + 3.9, btn_y + 0.1, r=0.55, color='#334155')
        elif icon_type == "lock":
            draw_lock(ax, phone_x + 3.9, btn_y + 0.1, r=0.55, color='#334155')
        elif icon_type == "gear":
            draw_gauge_icon(ax, phone_x + 3.9, btn_y + 0.1, r=0.55, color='#334155')
        elif icon_type == "logout":
            ax.plot([phone_x + 3.4, phone_x + 4.4], [btn_y + 0.1, btn_y + 0.1], color='#334155', lw=1.5)
            ax.plot([phone_x + 4.1, phone_x + 4.4, phone_x + 4.1], [btn_y + 0.4, btn_y + 0.1, btn_y - 0.2], color='#334155', lw=1.5)
        ax.text(phone_x + 6.0, btn_y + 0.1, label, ha='left', va='center', fontsize=8.2, fontweight='bold', color='#1e293b')
        btn_y -= 4.2

    # --- 1B. RUNTIME PROTECTION MODULE ---
    box_rpm = FancyBboxPatch((25.5, 51.5), 21.0, 40.5, boxstyle="round,pad=0.3,rounding_size=1.2",
                             facecolor='#f0fdf4', edgecolor='#16a34a', lw=1.4, ls='--')
    ax.add_patch(box_rpm)
    ax.text(36.0, 89.5, "RUNTIME PROTECTION\nMODULE", ha='center', va='center',
            fontsize=8.5, fontweight='bold', color='#15803d')

    rpm_cards = [
        ("Root Detection", "hash"),
        ("Emulator Detection", "phone"),
        ("Frida Detection", "frida"),
        ("Debugger Detection", "bug"),
        ("Integrity Check", "shield"),
        ("SSL Pinning", "lock"),
        ("Code Tamper Detection", "code")
    ]
    card_y = 84.5
    for text, itype in rpm_cards:
        c_patch = FancyBboxPatch((26.8, card_y - 1.4), 18.4, 3.2,
                                 boxstyle="round,pad=0.15,rounding_size=0.6",
                                 facecolor='#ffffff', edgecolor='#bbf7d0', lw=1.0)
        ax.add_patch(c_patch)
        draw_icon_box(ax, 28.5, card_y + 0.2, size=1.8, bg='#dcfce7', border='#86efac')
        if itype == "hash":
            draw_hash(ax, 28.5, card_y + 0.2, r=0.7, color='#15803d')
        elif itype == "phone":
            draw_phone_icon(ax, 28.5, card_y + 0.2, r=0.7, color='#15803d')
        elif itype == "frida":
            draw_alien_mask(ax, 28.5, card_y + 0.2, r=0.7, color='#15803d')
        elif itype == "bug":
            draw_bug_icon(ax, 28.5, card_y + 0.2, r=0.7, color='#15803d')
        elif itype == "shield":
            draw_shield(ax, 28.5, card_y + 0.2, r=0.7, color='#15803d')
        elif itype == "lock":
            draw_lock(ax, 28.5, card_y + 0.2, r=0.7, color='#15803d')
        elif itype == "code":
            draw_code_icon(ax, 28.5, card_y + 0.2, r=0.7, color='#15803d')
        ax.text(30.6, card_y + 0.2, text, ha='left', va='center', fontsize=7.8, fontweight='bold', color='#1e293b')
        card_y -= 4.7

    # --- 1C. SECURE STORAGE ---
    box_ss = FancyBboxPatch((5.5, 39.5), 41.0, 9.8, boxstyle="round,pad=0.3,rounding_size=1.2",
                            facecolor='#f0fdf4', edgecolor='#16a34a', lw=1.4, ls='--')
    ax.add_patch(box_ss)
    ax.text(26.0, 47.2, "SECURE STORAGE", ha='center', va='center',
            fontsize=8.5, fontweight='bold', color='#15803d')

    # SharedPreferences Card
    sp_patch = FancyBboxPatch((6.8, 43.2), 38.4, 2.7, boxstyle="round,pad=0.15,rounding_size=0.5",
                              facecolor='#ffffff', edgecolor='#bbf7d0', lw=1.0)
    ax.add_patch(sp_patch)
    draw_lock(ax, 8.8, 44.55, r=0.65, color='#15803d')
    ax.text(11.0, 44.55, "Encrypted SharedPreferences", ha='left', va='center', fontsize=8.0, fontweight='bold', color='#1e293b')

    # Android Keystore Card
    ks_patch = FancyBboxPatch((6.8, 40.2), 38.4, 2.7, boxstyle="round,pad=0.15,rounding_size=0.5",
                              facecolor='#ffffff', edgecolor='#bbf7d0', lw=1.0)
    ax.add_patch(ks_patch)
    draw_shield(ax, 8.8, 41.55, r=0.65, color='#15803d')
    ax.text(11.0, 41.55, "Android Keystore", ha='left', va='center', fontsize=8.0, fontweight='bold', color='#1e293b')


    # =========================================================================
    # NETWORK LINK (HTTPS TLS 1.3 / JWT)
    # =========================================================================
    net_arr = patches.FancyArrowPatch((48.0, 67.5), (57.5, 67.5), arrowstyle='<->',
                                      mutation_scale=16, lw=2.2, color='#0f172a')
    ax.add_patch(net_arr)
    # Lock pill
    lock_pill = FancyBboxPatch((50.8, 70.2), 4.0, 4.0, boxstyle="round,pad=0.1,rounding_size=0.6",
                               facecolor='#1e293b', edgecolor='#0f172a', lw=1.0)
    ax.add_patch(lock_pill)
    draw_lock(ax, 52.8, 72.2, r=1.0, color='#ffffff')
    ax.text(52.8, 66.0, "HTTPS\nTLS 1.3", ha='center', va='top', fontsize=7.8, fontweight='bold', color='#0f172a')
    ax.text(52.8, 60.5, "JWT\nAccess Token", ha='center', va='top', fontsize=7.5, fontweight='bold', color='#0f172a')


    # =========================================================================
    # 2. API GATEWAY CONTAINER (BLUE)
    # =========================================================================
    card_gw = FancyBboxPatch((57.5, 38.0), 26.5, 59.0, boxstyle="round,pad=0.5,rounding_size=2.0",
                             facecolor='#eff6ff', edgecolor='#3b82f6', lw=1.8)
    ax.add_patch(card_gw)
    ax.text(70.75, 94.5, "API GATEWAY", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#1d4ed8')
    ax.text(70.75, 92.0, "(Spring Cloud Gateway)", ha='center', va='center',
            fontsize=9.0, fontstyle='italic', color='#2563eb')

    gw_items = [
        ("Request Routing", "routing"),
        ("Authentication &\nAuthorization", "auth"),
        ("Rate Limiting", "rate"),
        ("Request Validation", "val"),
        ("Security Headers", "headers"),
        ("Logging & Monitoring", "log")
    ]
    gw_y = 85.5
    for text, itype in gw_items:
        h_box = 4.8 if "\n" in text else 4.2
        patch = FancyBboxPatch((59.2, gw_y - h_box/2), 23.1, h_box,
                               boxstyle="round,pad=0.15,rounding_size=0.8",
                               facecolor='#ffffff', edgecolor='#bfdbfe', lw=1.0)
        ax.add_patch(patch)
        draw_icon_box(ax, 61.8, gw_y, size=2.6, bg='#dbeafe', border='#93c5fd')
        if itype == "routing":
            draw_routing_icon(ax, 61.8, gw_y, r=0.9, color='#1d4ed8')
        elif itype == "auth":
            draw_shield(ax, 61.8, gw_y, r=0.9, color='#1d4ed8')
        elif itype == "rate":
            draw_gauge_icon(ax, 61.8, gw_y, r=0.9, color='#1d4ed8')
        elif itype == "val":
            draw_clipboard_icon(ax, 61.8, gw_y, r=0.9, color='#1d4ed8')
        elif itype == "headers":
            draw_shield(ax, 61.8, gw_y, r=0.9, color='#1d4ed8')
        elif itype == "log":
            draw_barchart_icon(ax, 61.8, gw_y, r=0.9, color='#1d4ed8')
        ax.text(64.8, gw_y, text, ha='left', va='center', fontsize=8.0, fontweight='bold', color='#1e293b')
        gw_y -= 7.4


    # =========================================================================
    # ARROW: API GATEWAY -> BACKEND SERVICES
    # =========================================================================
    arr_gw_be = patches.FancyArrowPatch((84.0, 67.5), (90.0, 67.5), arrowstyle='->',
                                        mutation_scale=16, lw=2.2, color='#0f172a')
    ax.add_patch(arr_gw_be)


    # =========================================================================
    # 3. BACKEND SERVICES CONTAINER (PURPLE)
    # =========================================================================
    card_be = FancyBboxPatch((90.0, 38.0), 33.5, 59.0, boxstyle="round,pad=0.5,rounding_size=2.0",
                            facecolor='#faf5ff', edgecolor='#a855f7', lw=1.8)
    ax.add_patch(card_be)
    ax.text(106.75, 94.5, "BACKEND SERVICES", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#7e22ce')
    ax.text(106.75, 92.0, "(Spring Boot Microservices)", ha='center', va='center',
            fontsize=9.0, fontstyle='italic', color='#9333ea')

    be_items = [
        ("Auth Service", "(Login, Register, Token)", "users"),
        ("User Service", "(Profile, Preferences)", "user"),
        ("Business Service", "(App Functionalities)", "case"),
        ("Threat Detection Service", "(Runtime & API Events)", "warn"),
        ("Audit & Logging Service", "(Logs, Alerts)", "doc")
    ]
    be_y = 84.5
    for title, sub, itype in be_items:
        patch = FancyBboxPatch((92.0, be_y - 2.8), 29.5, 5.8,
                               boxstyle="round,pad=0.15,rounding_size=0.8",
                               facecolor='#ffffff', edgecolor='#e9d5ff', lw=1.0)
        ax.add_patch(patch)
        draw_icon_box(ax, 95.0, be_y + 0.1, size=3.0, bg='#f3e8ff', border='#d8b4fe')
        if itype == "users":
            draw_users_icon(ax, 95.0, be_y + 0.1, r=1.0, color='#7e22ce')
        elif itype == "user":
            draw_single_user_icon(ax, 95.0, be_y + 0.1, r=1.0, color='#7e22ce')
        elif itype == "case":
            draw_briefcase_icon(ax, 95.0, be_y + 0.1, r=1.0, color='#7e22ce')
        elif itype == "warn":
            draw_warning_icon(ax, 95.0, be_y + 0.1, r=1.0, color='#dc2626')
        elif itype == "doc":
            draw_doc_icon(ax, 95.0, be_y + 0.1, r=1.0, color='#7e22ce')

        ax.text(98.5, be_y + 1.1, title, ha='left', va='center', fontsize=8.8, fontweight='bold', color='#1e293b')
        ax.text(98.5, be_y - 1.1, sub, ha='left', va='center', fontsize=7.6, color='#64748b')
        be_y -= 9.0


    # =========================================================================
    # ARROW: BACKEND SERVICES <-> DATA LAYER
    # =========================================================================
    arr_be_db = patches.FancyArrowPatch((123.5, 67.5), (129.5, 67.5), arrowstyle='<->',
                                        mutation_scale=16, lw=2.2, color='#0f172a')
    ax.add_patch(arr_be_db)


    # =========================================================================
    # 4. DATA LAYER CONTAINER (GOLD / YELLOW)
    # =========================================================================
    card_data = FancyBboxPatch((129.5, 43.5), 26.5, 53.5, boxstyle="round,pad=0.5,rounding_size=2.0",
                               facecolor='#fffbeb', edgecolor='#f59e0b', lw=1.8)
    ax.add_patch(card_data)
    ax.text(142.75, 94.5, "DATA LAYER", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#b45309')

    # --- 4A. DATABASE (PostgreSQL) ---
    db_box = FancyBboxPatch((131.0, 70.0), 23.5, 21.0, boxstyle="round,pad=0.3,rounding_size=1.0",
                            facecolor='#ffffff', edgecolor='#fed7aa', lw=1.2)
    ax.add_patch(db_box)
    ax.text(142.75, 88.8, "DATABASE", ha='center', va='center', fontsize=8.8, fontweight='bold', color='#1e293b')
    ax.text(142.75, 86.8, "(PostgreSQL)", ha='center', va='center', fontsize=7.8, color='#64748b')
    draw_database_3d(ax, 136.0, 77.5, w=5.2, h=5.8, color='#0284c7')

    db_bullets = ["• Users", "• Roles", "• Tokens", "• App Data", "• Logs"]
    by = 81.5
    for bul in db_bullets:
        ax.text(140.5, by, bul, ha='left', va='center', fontsize=7.6, fontweight='bold', color='#334155')
        by -= 2.0

    # --- 4B. CACHE / SESSION STORE (Redis) ---
    cache_box = FancyBboxPatch((131.0, 45.5), 23.5, 22.0, boxstyle="round,pad=0.3,rounding_size=1.0",
                               facecolor='#ffffff', edgecolor='#fed7aa', lw=1.2)
    ax.add_patch(cache_box)
    ax.text(142.75, 65.2, "CACHE / SESSION STORE", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1e293b')
    ax.text(142.75, 63.2, "(Redis)", ha='center', va='center', fontsize=7.8, color='#64748b')
    draw_redis_layers(ax, 136.0, 54.0, w=5.2, h=5.5, color='#dc2626')

    cache_bullets = ["• Sessions", "• Tokens", "• Rate Limit Data", "• Blacklists"]
    cy = 58.5
    for bul in cache_bullets:
        ax.text(140.5, cy, bul, ha='left', va='center', fontsize=7.6, fontweight='bold', color='#334155')
        cy -= 2.2


    # =========================================================================
    # CONNECTOR DOWN FROM BACKEND SERVICES TO LOWER LAYERS
    # =========================================================================
    ax.plot([106.75, 106.75], [38.0, 34.5], color='#0f172a', lw=1.8)
    ax.plot([65.0, 142.5], [34.5, 34.5], color='#0f172a', lw=1.8)
    # Down to Security Layer
    arr_down_sec = patches.FancyArrowPatch((65.0, 34.5), (65.0, 32.5), arrowstyle='->',
                                          mutation_scale=12, lw=1.8, color='#0f172a')
    ax.add_patch(arr_down_sec)
    # Down to Dashboard
    arr_down_dash = patches.FancyArrowPatch((142.5, 34.5), (142.5, 32.5), arrowstyle='->',
                                           mutation_scale=12, lw=1.8, color='#0f172a')
    ax.add_patch(arr_down_dash)


    # =========================================================================
    # 5. SECURITY & MONITORING LAYER CONTAINER (RED DASHED)
    # =========================================================================
    card_sec = FancyBboxPatch((42.0, 19.5), 76.5, 13.0, boxstyle="round,pad=0.4,rounding_size=1.5",
                              facecolor='#fef2f2', edgecolor='#ef4444', lw=1.5, ls='--')
    ax.add_patch(card_sec)
    ax.text(80.25, 30.8, "SECURITY & MONITORING LAYER", ha='center', va='center',
            fontsize=10.0, fontweight='bold', color='#b91c1c')

    sec_items = [
        ("Centralized\nLogging\n(ELK Stack)", "elk"),
        ("Security\nAnalytics\n(Anomaly Detection)", "trend"),
        ("Alert Manager\n(Email / SMS /\nWebhook)", "bell"),
        ("SIEM\nIntegration\n(Optional)", "siem")
    ]
    sx = 44.5
    for title, itype in sec_items:
        patch = FancyBboxPatch((sx, 20.5), 17.2, 8.5, boxstyle="round,pad=0.15,rounding_size=0.6",
                               facecolor='#ffffff', edgecolor='#fecaca', lw=1.0)
        ax.add_patch(patch)
        draw_icon_box(ax, sx + 2.6, 24.75, size=2.8, bg='#f8fafc', border='#e2e8f0')
        if itype == "elk":
            draw_elk_emblem(ax, sx + 2.6, 24.75, r=1.1)
        elif itype == "trend":
            draw_trend_icon(ax, sx + 2.6, 24.75, r=1.0)
        elif itype == "bell":
            draw_bell_icon(ax, sx + 2.6, 24.75, r=1.0)
        elif itype == "siem":
            draw_shield(ax, sx + 2.6, 24.75, r=1.0, color='#2563eb')
        ax.text(sx + 5.2, 24.75, title, ha='left', va='center', fontsize=7.2, fontweight='bold', color='#1e293b')
        sx += 18.8


    # =========================================================================
    # 6. WEB DASHBOARD CONTAINER (ADMIN PANEL - MONITOR MOCKUP)
    # =========================================================================
    card_dash = FancyBboxPatch((124.0, 18.0), 32.5, 14.8, boxstyle="round,pad=0.4,rounding_size=1.5",
                               facecolor='#f8fafc', edgecolor='#64748b', lw=1.4, ls='--')
    ax.add_patch(card_dash)
    ax.text(140.25, 31.2, "WEB DASHBOARD", ha='center', va='center',
            fontsize=9.5, fontweight='bold', color='#0f172a')
    ax.text(140.25, 29.5, "(Admin Panel)", ha='center', va='center',
            fontsize=7.5, fontstyle='italic', color='#475569')

    # Realistic Desktop Computer Monitor on Stand
    mx, my, mw, mh = 127.0, 20.0, 26.5, 8.5
    # Bezel
    mon_bezel = FancyBboxPatch((mx, my), mw, mh, boxstyle="round,pad=0.2,rounding_size=0.8",
                               facecolor='#1e293b', edgecolor='#0f172a', lw=1.2)
    ax.add_patch(mon_bezel)
    # Screen inner (White background like real dashboard)
    mon_screen = FancyBboxPatch((mx + 0.8, my + 0.8), mw - 1.6, mh - 1.6,
                                boxstyle="round,pad=0.1,rounding_size=0.4",
                                facecolor='#ffffff', edgecolor='#cbd5e1', lw=0.6)
    ax.add_patch(mon_screen)
    # Left dark sidebar in screen
    ax.add_patch(Rectangle((mx + 0.8, my + 0.8), 2.8, mh - 1.6, facecolor='#1e293b'))
    for dy_nav in [mh - 2.5, mh - 3.8, mh - 5.1]:
        ax.add_patch(Circle((mx + 2.2, my + dy_nav), 0.35, facecolor='#60a5fa'))

    # Stand foot & neck
    ax.plot([mx + mw/2, mx + mw/2], [my, my - 1.2], color='#94a3b8', lw=3.2)
    ax.plot([mx + mw/2 - 2.8, mx + mw/2 + 2.8], [my - 1.2, my - 1.2], color='#94a3b8', lw=2.8)

    # Screen Graphics (SOC Analyst Charts)
    # Donut Chart
    ax.add_patch(patches.Wedge((mx + 6.8, my + mh/2), 1.9, 0, 210, width=0.8, facecolor='#06b6d4'))
    ax.add_patch(patches.Wedge((mx + 6.8, my + mh/2), 1.9, 210, 310, width=0.8, facecolor='#10b981'))
    ax.add_patch(patches.Wedge((mx + 6.8, my + mh/2), 1.9, 310, 360, width=0.8, facecolor='#f59e0b'))
    # Mini Bar Chart
    for bx, bh, bcol in zip([11.8, 14.0, 16.2, 18.4], [2.2, 3.8, 1.6, 4.4], ['#3b82f6', '#2563eb', '#60a5fa', '#1d4ed8']):
        ax.add_patch(Rectangle((mx + bx, my + 1.8), 1.4, bh, facecolor=bcol))
    # Mini Line Chart with nodes
    lx = [mx + 21.0, mx + 22.3, mx + 23.6, mx + 25.0]
    ly = [my + 2.2, my + 4.2, my + 2.8, my + 5.0]
    ax.plot(lx, ly, color='#2563eb', lw=1.6)
    for px, py in zip(lx, ly):
        ax.add_patch(Circle((px, py), 0.25, facecolor='#2563eb'))


    # =========================================================================
    # 7. CLOUD NATIVE INFRASTRUCTURE PIPELINE (BOTTOM FULL WIDTH)
    # =========================================================================
    card_infra = FancyBboxPatch((3.5, 1.2), 153.0, 15.0, boxstyle="round,pad=0.4,rounding_size=1.8",
                                facecolor='#f0f9ff', edgecolor='#0284c7', lw=1.6, ls='--')
    ax.add_patch(card_infra)
    ax.text(80.0, 14.8, "CLOUD NATIVE INFRASTRUCTURE", ha='center', va='center',
            fontsize=10.5, fontweight='bold', color='#0369a1')

    # 5 Pipeline Nodes
    p_nodes = [
        ("Docker Container", "docker"),
        ("Kubernetes (Optional)", "k8s"),
        ("Cloud Platform\n(AWS / GCP / Azure)", "cloud"),
        ("CI/CD Pipeline\n(GitHub Actions / Jenkins)", "cicd"),
        ("Monitoring\n(Prometheus + Grafana)", "mon")
    ]
    node_xs = [16.0, 48.0, 80.0, 114.0, 145.0]

    for i, ((label, ntype), nx) in enumerate(zip(p_nodes, node_xs)):
        if ntype == "docker":
            draw_docker_whale(ax, nx, 9.2, r=1.7, color='#0284c7')
        elif ntype == "k8s":
            draw_k8s_wheel(ax, nx, 9.2, r=1.6, color='#2563eb')
        elif ntype == "cloud":
            draw_cloud_icon(ax, nx, 9.2, r=1.7, color='#0284c7')
        elif ntype == "cicd":
            draw_cicd_pipeline(ax, nx, 9.2, r=1.6, color='#2563eb')
        elif ntype == "mon":
            draw_flame_icon(ax, nx - 1.5, 9.2, r=1.4, color='#ea580c')
            draw_grafana_swirl(ax, nx + 1.5, 9.2, r=1.4)

        ax.text(nx, 5.2, label, ha='center', va='top', fontsize=7.6, fontweight='bold', color='#1e293b')

        # Arrow between nodes
        if i < len(node_xs) - 1:
            next_x = node_xs[i+1]
            arr = patches.FancyArrowPatch((nx + 10.5, 9.2), (next_x - 10.5, 9.2),
                                          arrowstyle='->', mutation_scale=14, lw=1.8, color='#0f172a')
            ax.add_patch(arr)

    # Save output
    out_file1 = os.path.join(OUT_DIR, "Figure_4_1_Six_Tier_System_Architecture.png")
    out_file2 = os.path.join(OUT_DIR, "AppShieldX_Comprehensive_Architecture_Infographic.png")
    plt.tight_layout()
    plt.savefig(out_file1, dpi=300, bbox_inches='tight')
    plt.savefig(out_file2, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated clean: {out_file1}")
    print(f"Generated clean: {out_file2}")

if __name__ == "__main__":
    generate_architecture_infographic()

