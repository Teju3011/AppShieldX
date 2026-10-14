#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AppShieldX - Complete App Icon & Asset Generation Pipeline
Processes the user's official AppShieldX logo and produces:
1. Android launcher icons across all mipmap densities (mdpi, hdpi, xhdpi, xxhdpi, xxxhdpi)
2. Android round launcher icons and adaptive icon foreground/background
3. Web icons (favicon, PWA icons, apple touch icons)
4. Flutter high-res in-app assets (full logo, shield emblem, transparent variants)
5. Admin dashboard assets
"""

import os
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SOURCE_IMG = os.path.join(BASE_DIR, "source_logo.jpg")

# If source_logo.jpg not in BASE_DIR, check brain artifacts
USER_UPLOADED = r"C:\Users\tej30\.gemini\antigravity-ide\brain\3d5b5d94-28fd-4ce2-b142-2b01cf17e056\.user_uploaded\media_1791959617168.jpg"
if os.path.exists(USER_UPLOADED) and not os.path.exists(SOURCE_IMG):
    import shutil
    shutil.copyfile(USER_UPLOADED, SOURCE_IMG)

def process_and_generate_assets():
    print(f"[*] Loading source logo from: {SOURCE_IMG}")
    orig = Image.open(SOURCE_IMG).convert("RGB")
    W, H = orig.size # 1024x1024

    # 1. Extract Shield-only region and Full region
    # Full content box: x=(74, 952), y=(120, 922)
    # Shield region: y=(120, 794), x=(235, 789)
    # Text region: y=(815, 922), x=(74, 952)
    
    # Create clean transparent RGBA version of the full image
    arr = np.array(orig, dtype=float)
    # Background is white (~254)
    # Exterior background mask: distance from (254, 254, 254)
    bg = np.array([254.0, 254.0, 254.0])
    diff = np.max(bg - arr, axis=2) # 0 for pure white background
    
    # Smooth thresholding for antialiased edges
    alpha = np.clip((diff - 8.0) / 25.0 * 255.0, 0, 255).astype(np.uint8)
    
    # For interior of shield (which has pure white background inside on left):
    # We want the white background OUTSIDE the shield and text to be transparent,
    # but the shield outline and inner parts preserved.
    # Let's inspect: The shield outer boundary is teal (diff > 50).
    # Flood-fill from corners to find only the EXTERIOR background!
    from collections import deque
    is_ext_bg = np.zeros((H, W), dtype=bool)
    visited = np.zeros((H, W), dtype=bool)
    
    # Seed corners
    queue = deque([(0, 0), (W-1, 0), (0, H-1), (W-1, H-1)])
    for x, y in queue:
        visited[y, x] = True
    
    # A pixel is background if it's connected to corner and bright (diff < 35)
    while queue:
        cx, cy = queue.popleft()
        is_ext_bg[cy, cx] = True
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < W and 0 <= ny < H and not visited[ny, nx]:
                visited[ny, nx] = True
                if diff[ny, nx] < 35:
                    queue.append((nx, ny))
                    
    # Generate Alpha: 0 for exterior background, 255 for content
    final_alpha = np.ones((H, W), dtype=np.uint8) * 255
    final_alpha[is_ext_bg] = 0
    
    # Smooth alpha edges with a small blur
    alpha_img = Image.fromarray(final_alpha, mode='L')
    alpha_img = alpha_img.filter(ImageFilter.GaussianBlur(radius=0.7))
    
    # Full Transparent Logo
    full_transparent = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    full_transparent.paste(orig, (0, 0), mask=alpha_img)
    
    # 2. Extract Shield Emblem (Square canvas, beautifully centered with 12% padding)
    shield_crop = orig.crop((230, 115, 794, 794)) # ~564x679
    # Put into 1024x1024 square with white background
    shield_canvas_white = Image.new("RGB", (1024, 1024), "#ffffff")
    target_shield_h = int(1024 * 0.82)
    aspect = shield_crop.width / shield_crop.height
    target_shield_w = int(target_shield_h * aspect)
    shield_resized = shield_crop.resize((target_shield_w, target_shield_h), Image.Resampling.LANCZOS)
    paste_x = (1024 - target_shield_w) // 2
    paste_y = (1024 - target_shield_h) // 2
    shield_canvas_white.paste(shield_resized, (paste_x, paste_y))

    # Transparent Shield Emblem
    shield_trans_crop = full_transparent.crop((230, 115, 794, 794))
    shield_trans_canvas = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    shield_trans_resized = shield_trans_crop.resize((target_shield_w, target_shield_h), Image.Resampling.LANCZOS)
    shield_trans_canvas.paste(shield_trans_resized, (paste_x, paste_y), mask=shield_trans_resized)

    # Round Shield Emblem (For Android round launcher icons)
    shield_round_canvas = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    mask_circle = Image.new("L", (1024, 1024), 0)
    draw_c = ImageDraw.Draw(mask_circle)
    draw_c.ellipse((24, 24, 1000, 1000), fill=255)
    
    # Circle background with white fill and subtle border
    draw_round = ImageDraw.Draw(shield_round_canvas)
    draw_round.ellipse((24, 24, 1000, 1000), fill="#ffffff", outline="#00A2B3", width=12)
    # Place scaled shield inside circle
    round_shield_h = int(1024 * 0.68)
    round_shield_w = int(round_shield_h * aspect)
    r_resized = shield_trans_crop.resize((round_shield_w, round_shield_h), Image.Resampling.LANCZOS)
    shield_round_canvas.paste(r_resized, ((1024 - round_shield_w)//2, (1024 - round_shield_h)//2), mask=r_resized)

    # 3. Save Flutter App Assets in mobile/assets/images/
    assets_dir = os.path.join(BASE_DIR, "mobile", "assets", "images")
    os.makedirs(assets_dir, exist_ok=True)
    
    orig.save(os.path.join(assets_dir, "app_logo.png"), "PNG")
    full_transparent.save(os.path.join(assets_dir, "app_logo_transparent.png"), "PNG")
    shield_canvas_white.save(os.path.join(assets_dir, "app_logo_shield.png"), "PNG")
    shield_trans_canvas.save(os.path.join(assets_dir, "app_logo_shield_transparent.png"), "PNG")
    print(f"[+] Saved Flutter assets to: {assets_dir}")

    # 4. Generate Android Launcher Icons
    # Mipmap densities
    densities = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192,
    }
    res_dir = os.path.join(BASE_DIR, "mobile", "android", "app", "src", "main", "res")
    
    for folder, size in densities.items():
        folder_path = os.path.join(res_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
        
        # Standard icon (with clean white background, squircle/square ready)
        icon_std = shield_canvas_white.resize((size, size), Image.Resampling.LANCZOS)
        icon_std.save(os.path.join(folder_path, "ic_launcher.png"), "PNG")
        
        # Round icon
        icon_rnd = shield_round_canvas.resize((size, size), Image.Resampling.LANCZOS)
        icon_rnd.save(os.path.join(folder_path, "ic_launcher_round.png"), "PNG")
        
        # Adaptive foreground (scaled down to fit 66% safe zone of 432x432)
        fg_size = int(size * 2.25)
        fg_canvas = Image.new("RGBA", (fg_size, fg_size), (0, 0, 0, 0))
        emblem_size = int(fg_size * 0.65)
        emblem_w = int(emblem_size * aspect)
        emblem_resized = shield_trans_crop.resize((emblem_w, emblem_size), Image.Resampling.LANCZOS)
        fg_canvas.paste(emblem_resized, ((fg_size - emblem_w)//2, (fg_size - emblem_size)//2), mask=emblem_resized)
        fg_canvas.save(os.path.join(folder_path, "ic_launcher_foreground.png"), "PNG")
        
        print(f"[+] Generated Android icons in {folder} ({size}x{size})")

    # Android Adaptive Icon XML (res/mipmap-anydpi-v26/)
    anydpi_dir = os.path.join(res_dir, "mipmap-anydpi-v26")
    os.makedirs(anydpi_dir, exist_ok=True)
    
    with open(os.path.join(anydpi_dir, "ic_launcher.xml"), "w") as f:
        f.write('''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>
</adaptive-icon>
''')
    with open(os.path.join(anydpi_dir, "ic_launcher_round.xml"), "w") as f:
        f.write('''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>
</adaptive-icon>
''')
        
    # Values colors.xml
    values_dir = os.path.join(res_dir, "values")
    colors_xml = os.path.join(values_dir, "colors.xml")
    with open(colors_xml, "w") as f:
        f.write('''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="ic_launcher_background">#FFFFFF</color>
</resources>
''')
    print(f"[+] Generated Android adaptive icon configs in mipmap-anydpi-v26 and colors.xml")

    # 5. Generate Web Icons (mobile/web)
    web_dir = os.path.join(BASE_DIR, "mobile", "web")
    web_icons_dir = os.path.join(web_dir, "icons")
    os.makedirs(web_icons_dir, exist_ok=True)
    
    shield_canvas_white.resize((192, 192), Image.Resampling.LANCZOS).save(os.path.join(web_icons_dir, "Icon-192.png"))
    shield_canvas_white.resize((512, 512), Image.Resampling.LANCZOS).save(os.path.join(web_icons_dir, "Icon-512.png"))
    shield_canvas_white.resize((192, 192), Image.Resampling.LANCZOS).save(os.path.join(web_icons_dir, "Icon-maskable-192.png"))
    shield_canvas_white.resize((512, 512), Image.Resampling.LANCZOS).save(os.path.join(web_icons_dir, "Icon-maskable-512.png"))
    
    shield_canvas_white.resize((180, 180), Image.Resampling.LANCZOS).save(os.path.join(web_dir, "apple-touch-icon.png"))
    shield_canvas_white.resize((180, 180), Image.Resampling.LANCZOS).save(os.path.join(web_dir, "apple-touch-icon-precomposed.png"))
    shield_canvas_white.resize((64, 64), Image.Resampling.LANCZOS).save(os.path.join(web_dir, "favicon.png"))
    shield_canvas_white.resize((32, 32), Image.Resampling.LANCZOS).save(os.path.join(web_dir, "favicon.ico"), format="ICO")
    print(f"[+] Generated Web PWA & Favicon assets in mobile/web")

    # 6. Admin Dashboard Web Assets (admin-dashboard/public)
    dash_pub = os.path.join(BASE_DIR, "admin-dashboard", "public")
    if os.path.exists(dash_pub):
        full_transparent.save(os.path.join(dash_pub, "appshieldx_logo.png"), "PNG")
        shield_canvas_white.resize((64, 64), Image.Resampling.LANCZOS).save(os.path.join(dash_pub, "favicon.ico"), format="ICO")
        print(f"[+] Updated Admin Dashboard assets in {dash_pub}")

if __name__ == '__main__':
    process_and_generate_assets()
