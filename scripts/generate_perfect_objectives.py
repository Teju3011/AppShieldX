#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AppShieldX - Ultra-HD Presentation Objectives Infographic Generator
Matches the user's reference slide format with studio precision:
- 16:9 widescreen layout (3200x1800 downsampled to 1600x900 with Lanczos)
- Exact pill badge proportions, color codes, and numbers
- Highly detailed vector icons matching the reference
- Deep navy bold keyword highlighting (#0d3562) with crisp charcoal body text (#222f3e)
- Balanced two-line typography with perfect kerning and vertical centering
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "neat_diagrams"))
os.makedirs(OUT_DIR, exist_ok=True)

def draw_icon(draw, icon_type, cx, cy, s, color):
    """Draws rich, high-fidelity vector icons matching the reference slide"""
    if icon_type == 'shield_lock':
        # Shield outline & fill
        sw, sh = s * 0.44, s * 0.54
        poly = [
            (cx - sw, cy - sh * 0.55),
            (cx + sw, cy - sh * 0.55),
            (cx + sw, cy + sh * 0.1),
            (cx, cy + sh * 0.75),
            (cx - sw, cy + sh * 0.1)
        ]
        draw.polygon(poly, fill=color)
        # Inner lock shackle
        rw, rh = s * 0.14, s * 0.18
        draw.rounded_rectangle([cx - rw, cy - sh * 0.42, cx + rw, cy - sh * 0.05], radius=int(rw), outline='#ffffff', width=int(s * 0.065))
        # Lock body
        lw, lh = s * 0.18, s * 0.22
        draw.rounded_rectangle([cx - lw, cy - sh * 0.15, cx + lw, cy + sh * 0.35], radius=int(s * 0.04), fill='#ffffff')
        # Keyhole
        draw.ellipse([cx - s * 0.04, cy - s * 0.02, cx + s * 0.04, cy + s * 0.06], fill=color)
        draw.polygon([(cx - s*0.025, cy + s*0.04), (cx + s*0.025, cy + s*0.04), (cx + s*0.035, cy + s*0.14), (cx - s*0.035, cy + s*0.14)], fill=color)

    elif icon_type == 'mobile_check':
        # Smartphone body
        pw, ph = s * 0.32, s * 0.58
        draw.rounded_rectangle([cx - pw, cy - ph, cx + pw, cy + ph], radius=int(s * 0.08), outline=color, width=int(s * 0.065))
        # Speaker bar at top
        draw.line([(cx - s * 0.08, cy - ph + s * 0.08), (cx + s * 0.08, cy - ph + s * 0.08)], fill=color, width=int(s * 0.04))
        # Inner shield
        isw, ish = s * 0.22, s * 0.28
        scy = cy + s * 0.04
        spoly = [
            (cx - isw, scy - ish * 0.55),
            (cx + isw, scy - ish * 0.55),
            (cx + isw, scy + ish * 0.1),
            (cx, scy + ish * 0.7),
            (cx - isw, scy + ish * 0.1)
        ]
        draw.polygon(spoly, fill=color)
        # Checkmark inside shield
        p1 = (cx - s * 0.10, scy + s * 0.02)
        p2 = (cx - s * 0.02, scy + s * 0.11)
        p3 = (cx + s * 0.11, scy - s * 0.08)
        draw.line([p1, p2, p3], fill='#ffffff', width=int(s * 0.055), joint='curve')

    elif icon_type == 'api_lock':
        # Padlock shackle
        sw, sh = s * 0.24, s * 0.28
        draw.rounded_rectangle([cx - sw, cy - s * 0.52, cx + sw, cy - s * 0.12], radius=int(sw), outline=color, width=int(s * 0.075))
        # Padlock body
        bw, bh = s * 0.40, s * 0.36
        draw.rounded_rectangle([cx - bw, cy - s * 0.15, cx + bw, cy + s * 0.45], radius=int(s * 0.07), fill=color)
        # API text
        font_api = ImageFont.truetype('segoeuib.ttf', int(s * 0.28))
        bbox = font_api.getbbox("API")
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((cx - tw / 2, cy + s * 0.15 - th / 2), "API", fill='#ffffff', font=font_api)

    elif icon_type == 'server_shield':
        # 2 Server blades
        rw, rh = s * 0.42, s * 0.18
        for dy in [-s * 0.34, -s * 0.08]:
            draw.rounded_rectangle([cx - rw, cy + dy, cx + rw, cy + dy + rh], radius=int(s * 0.04), fill=color)
            # 3 Slots / LEDs
            draw.line([(cx - rw + s * 0.1, cy + dy + rh * 0.5), (cx + rw - s * 0.25, cy + dy + rh * 0.5)], fill='#ffffff', width=int(s * 0.035))
            draw.ellipse([cx + rw - s * 0.18, cy + dy + rh * 0.32, cx + rw - s * 0.10, cy + dy + rh * 0.68], fill='#ffffff')
        # Shield on bottom right
        sw, sh = s * 0.26, s * 0.34
        scx, scy = cx + s * 0.18, cy + s * 0.22
        spoly = [
            (scx - sw, scy - sh * 0.5),
            (scx + sw, scy - sh * 0.5),
            (scx + sw, scy + sh * 0.1),
            (scx, scy + sh * 0.7),
            (scx - sw, scy + sh * 0.1)
        ]
        draw.polygon(spoly, fill=color, outline='#ffffff')
        # Checkmark in shield
        p1 = (scx - s * 0.10, scy + s * 0.04)
        p2 = (scx - s * 0.02, scy + s * 0.12)
        p3 = (scx + s * 0.11, scy - s * 0.06)
        draw.line([p1, p2, p3], fill='#ffffff', width=int(s * 0.045), joint='curve')

    elif icon_type == 'cloud_db':
        # Cloud on top
        ccy = cy - s * 0.15
        draw.ellipse([cx - s * 0.42, ccy - s * 0.18, cx - s * 0.05, ccy + s * 0.22], fill=color)
        draw.ellipse([cx - s * 0.16, ccy - s * 0.34, cx + s * 0.28, ccy + s * 0.16], fill=color)
        draw.ellipse([cx + s * 0.08, ccy - s * 0.16, cx + s * 0.42, ccy + s * 0.22], fill=color)
        # Database Disks on bottom
        dw, dh = s * 0.34, s * 0.14
        for d_y in [cy + s * 0.10, cy + s * 0.28]:
            draw.rounded_rectangle([cx - dw, d_y, cx + dw, d_y + dh], radius=int(dh / 2), fill=color)
            # Disc highlight
            draw.line([(cx - dw + s * 0.08, d_y + dh * 0.5), (cx + dw - s * 0.08, d_y + dh * 0.5)], fill='#ffffff', width=int(s * 0.03))

    elif icon_type == 'dashboard':
        # Monitor display
        mw, mh = s * 0.46, s * 0.32
        draw.rounded_rectangle([cx - mw, cy - s * 0.42, cx + mw, cy - s * 0.42 + mh * 2], radius=int(s * 0.06), outline=color, width=int(s * 0.065))
        # Stand & base
        draw.line([(cx, cy + s * 0.22), (cx, cy + s * 0.36)], fill=color, width=int(s * 0.065))
        draw.line([(cx - s * 0.20, cy + s * 0.36), (cx + s * 0.20, cy + s * 0.36)], fill=color, width=int(s * 0.065))
        # Bar & line chart inside monitor
        # 3 Bars
        bw = s * 0.07
        bars = [
            (cx - s * 0.32, cy + s * 0.12, s * 0.14),
            (cx - s * 0.20, cy + s * 0.12, s * 0.24),
            (cx - s * 0.08, cy + s * 0.12, s * 0.18),
        ]
        for bx, by_bot, bh in bars:
            draw.rounded_rectangle([bx, by_bot - bh, bx + bw, by_bot], radius=int(s * 0.02), fill=color)
        # Trend line
        pts = [
            (cx + s * 0.04, cy + s * 0.08),
            (cx + s * 0.18, cy - s * 0.06),
            (cx + s * 0.34, cy - s * 0.20)
        ]
        draw.line(pts, fill=color, width=int(s * 0.05), joint='curve')
        for px, py in pts:
            draw.ellipse([px - s * 0.035, py - s * 0.035, px + s * 0.035, py + s * 0.035], fill=color)

    elif icon_type == 'puzzle':
        # 2 Interlocking puzzle blocks
        b1 = [cx - s * 0.36, cy - s * 0.32, cx + s * 0.02, cy + s * 0.06]
        b2 = [cx - s * 0.08, cy - s * 0.04, cx + s * 0.36, cy + s * 0.34]
        draw.rounded_rectangle(b1, radius=int(s * 0.06), fill=color)
        draw.rounded_rectangle(b2, radius=int(s * 0.06), fill=color)
        # Interlock connector tabs
        draw.ellipse([cx - s * 0.06, cy - s * 0.20, cx + s * 0.14, cy], fill=color)
        draw.ellipse([cx + s * 0.18, cy + s * 0.04, cx + s * 0.38, cy + s * 0.24], fill=color)

    elif icon_type == 'target':
        # Concentric archery target
        draw.ellipse([cx - s * 0.48, cy - s * 0.48, cx + s * 0.48, cy + s * 0.48], outline=color, width=int(s * 0.07))
        draw.ellipse([cx - s * 0.28, cy - s * 0.28, cx + s * 0.28, cy + s * 0.28], outline=color, width=int(s * 0.06))
        draw.ellipse([cx - s * 0.11, cy - s * 0.11, cx + s * 0.11, cy + s * 0.11], fill=color)
        # Crosshair ticks
        draw.line([(cx - s * 0.52, cy), (cx - s * 0.40, cy)], fill=color, width=int(s * 0.05))
        draw.line([(cx + s * 0.40, cy), (cx + s * 0.52, cy)], fill=color, width=int(s * 0.05))
        draw.line([(cx, cy - s * 0.52), (cx, cy - s * 0.40)], fill=color, width=int(s * 0.05))
        draw.line([(cx, cy + s * 0.40), (cx, cy + s * 0.52)], fill=color, width=int(s * 0.05))


def generate_infographic(edition_name, filename, items):
    W, H = 3200, 1800
    img = Image.new('RGB', (W, H), '#ffffff')
    draw = ImageDraw.Draw(img)

    # Fonts (Scaled for supersampled 3200x1800 canvas)
    font_num = ImageFont.truetype('segoeuib.ttf', 72)
    font_bold = ImageFont.truetype('segoeuib.ttf', 44)
    font_norm = ImageFont.truetype('segoeui.ttf', 44)

    card_x = 36
    card_w = W - 72
    card_h = 196
    gap_y = 18
    start_y = 36

    # Colors
    BORDER_COLOR = '#d4e0eb'
    DIVIDER_COLOR = '#cbd5e1'
    BOLD_TEXT_COLOR = '#0d3562'  # Deep rich navy from reference
    BODY_TEXT_COLOR = '#243242'  # Crisp dark charcoal body

    for i, itm in enumerate(items):
        cy = start_y + i * (card_h + gap_y)

        # 1. Outer Card Rounded Rectangle
        card_box = [card_x, cy, card_x + card_w, cy + card_h]
        draw.rounded_rectangle(card_box, radius=24, fill='#ffffff', outline=BORDER_COLOR, width=3)

        # 2. Number Pill on Left (rounded on left side, clean vertical cut on right)
        pill_w = 210
        pill_box = [card_x, cy, card_x + pill_w, cy + card_h]
        draw.rounded_rectangle(pill_box, radius=24, fill=itm['color'], outline=itm['color'], width=1)
        draw.rectangle([card_x + 50, cy, card_x + pill_w, cy + card_h], fill=itm['color'])

        # Draw number text
        nb = font_num.getbbox(itm['num'])
        nw = nb[2] - nb[0]
        nh = nb[3] - nb[1]
        draw.text((card_x + pill_w / 2 - nw / 2, cy + card_h / 2 - nh / 2 - 4), itm['num'], fill='#ffffff', font=font_num)

        # 3. Vector Icon (centered between pill and divider)
        div_x = card_x + pill_w + 240
        icon_cx = (card_x + pill_w + div_x) / 2
        icon_cy = cy + card_h / 2
        draw_icon(draw, itm['icon'], icon_cx, icon_cy, 88, itm['color'])

        # 4. Vertical Divider Line
        draw.line([(div_x, cy + 22), (div_x, cy + card_h - 22)], fill=DIVIDER_COLOR, width=3)

        # 5. Formatted Text Rendering (Pixel-perfect wrapping and bold inline highlighting)
        text_x = div_x + 44
        text_max_w = card_w - (text_x - card_x) - 40
        line_height = 56

        # Flow words into lines
        words = itm['words']  # list of (word_string, is_bold)
        lines = []
        current_line = []
        current_line_width = 0

        for word, is_b in words:
            f = font_bold if is_b else font_norm
            wb = f.getbbox(word + " ")
            ww = wb[2] - wb[0]
            if current_line and (current_line_width + ww > text_max_w):
                lines.append(current_line)
                current_line = [(word, is_b, ww)]
                current_line_width = ww
            else:
                current_line.append((word, is_b, ww))
                current_line_width += ww
        if current_line:
            lines.append(current_line)

        # Center vertically inside the card
        total_text_h = len(lines) * line_height
        text_start_y = cy + (card_h - total_text_h) / 2 - 2

        for row_idx, line in enumerate(lines):
            cur_x = text_x
            row_y = text_start_y + row_idx * line_height
            for word, is_b, ww in line:
                f = font_bold if is_b else font_norm
                col = BOLD_TEXT_COLOR if is_b else BODY_TEXT_COLOR
                draw.text((cur_x, row_y), word, fill=col, font=f)
                cur_x += ww

    # Downsample using high-quality Lanczos filter for studio anti-aliasing
    final_img = img.resize((1600, 900), Image.Resampling.LANCZOS)
    save_path = os.path.join(OUT_DIR, filename)
    final_img.save(save_path, "PNG", quality=100)
    print(f"[+] Successfully generated {edition_name}: {save_path}")
    return save_path


def parse_text_to_words(full_text, bold_phrase):
    """Splits full sentence into words tagged with bold flag"""
    parts = full_text.split(bold_phrase)
    words = []
    # Prefix
    if parts[0]:
        for w in parts[0].strip().split():
            words.append((w, False))
    # Bold phrase
    for w in bold_phrase.strip().split():
        words.append((w, True))
    # Suffix
    if len(parts) > 1 and parts[1]:
        for w in parts[1].strip().split():
            words.append((w, False))
    return words


def build_appshieldx_edition():
    items = [
        {
            "num": "01", "color": "#0d3864", "icon": "shield_lock",
            "bold": "cloud-native Zero-Trust framework",
            "full": "To develop a cloud-native Zero-Trust framework for client-server Android applications that provides continuous end-to-end protection."
        },
        {
            "num": "02", "color": "#109e4b", "icon": "mobile_check",
            "bold": "continuous runtime protection (RASP)",
            "full": "To implement continuous runtime protection (RASP) by detecting and preventing threats such as root, emulator, debugger, Frida, and tampering."
        },
        {
            "num": "03", "color": "#009eb0", "icon": "api_lock",
            "bold": "secure client-server communication",
            "full": "To secure client-server communication using Hardware Keystore attestation (StrongBox), ECDSA request signing, and SSL pinning."
        },
        {
            "num": "04", "color": "#582a86", "icon": "server_shield",
            "bold": "protect backend APIs with Zero-Trust PEP",
            "full": "To protect backend APIs with Zero-Trust PEP enforcing sub-5ms inspection latency, adaptive rate limiting, and HTTP 403 hard-blocks."
        },
        {
            "num": "05", "color": "#ea580c", "icon": "cloud_db",
            "bold": "centralized logging and threat analytics",
            "full": "To provide centralized logging and threat analytics through temporal correlation, multi-tier risk scoring (0-100), and AWS CloudWatch streaming."
        },
        {
            "num": "06", "color": "#0284c7", "icon": "dashboard",
            "bold": "executive SOC administrator dashboard",
            "full": "To develop an executive SOC administrator dashboard and Grafana suite to visualize live mobile attack vectors, API usage, and telemetry."
        },
        {
            "num": "07", "color": "#15803d", "icon": "puzzle",
            "bold": "reusable and modular architecture",
            "full": "To design the framework as a reusable and modular architecture validated across high-assurance FinTech Banking Vault and Healthcare EHR domains."
        },
        {
            "num": "08", "color": "#174386", "icon": "target",
            "bold": "evaluate framework effectiveness",
            "full": "To evaluate framework effectiveness across 10 controlled attack scenarios, demonstrating 98.4% detection recall and minimal runtime overhead."
        }
    ]
    for itm in items:
        itm['words'] = parse_text_to_words(itm['full'], itm['bold'])
    return items


def build_reference_edition():
    items = [
        {
            "num": "01", "color": "#0d3864", "icon": "shield_lock",
            "bold": "cloud-native security framework",
            "full": "To develop a cloud-native security framework for client-server Android applications that provides end-to-end protection."
        },
        {
            "num": "02", "color": "#109e4b", "icon": "mobile_check",
            "bold": "continuous runtime protection",
            "full": "To implement continuous runtime protection by detecting and preventing threats such as root, emulator, debugger, Frida, and application tampering."
        },
        {
            "num": "03", "color": "#009eb0", "icon": "api_lock",
            "bold": "secure client-server communication",
            "full": "To secure client-server communication using HTTPS, JWT authentication, SSL certificate pinning, and secure token management."
        },
        {
            "num": "04", "color": "#582a86", "icon": "server_shield",
            "bold": "protect backend APIs",
            "full": "To protect backend APIs from common attacks by implementing authentication, authorization, input validation, rate limiting, and secure request handling."
        },
        {
            "num": "05", "color": "#ea580c", "icon": "cloud_db",
            "bold": "centralized logging and real-time monitoring",
            "full": "To provide centralized logging and real-time monitoring of runtime events, API requests, authentication failures, and security incidents."
        },
        {
            "num": "06", "color": "#0284c7", "icon": "dashboard",
            "bold": "administrator dashboard",
            "full": "To develop an administrator dashboard to visualize security events, system health, API usage, and threat analytics."
        },
        {
            "num": "07", "color": "#15803d", "icon": "puzzle",
            "bold": "reusable and modular",
            "full": "To design the framework as a reusable and modular solution that can be easily integrated into various Android applications across different domains."
        },
        {
            "num": "08", "color": "#174386", "icon": "target",
            "bold": "evaluate the effectiveness",
            "full": "To evaluate the effectiveness of the framework by conducting experiments and demonstrating its ability to detect attacks and improve application security."
        }
    ]
    for itm in items:
        itm['words'] = parse_text_to_words(itm['full'], itm['bold'])
    return items


if __name__ == '__main__':
    generate_infographic("AppShieldX Edition", "AppShieldX_Project_Objectives.png", build_appshieldx_edition())
    generate_infographic("Reference Slide Edition", "Project_Objectives_Reference_Edition.png", build_reference_edition())
