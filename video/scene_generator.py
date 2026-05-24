from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random

from video.branding import BRAND_NAME, get_region_color, get_region_theme_name

W, H = 1080, 1920

def _font(size=60, bold=False):
    candidates = [
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for c in candidates:
        try:
            return ImageFont.truetype(c, size)
        except Exception:
            pass
    return None

def _wrap(text, font, max_width):
    words = str(text or "").split()
    lines, line = [], ""
    dummy = Image.new("RGB", (10, 10))
    draw = ImageDraw.Draw(dummy)

    for word in words:
        test = (line + " " + word).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def _gradient_background(region):
    base = get_region_color(region)
    img = Image.new("RGB", (W, H), base)
    px = img.load()

    for y in range(H):
        for x in range(W):
            ratio = y / H
            vignette = 1 - (abs(x - W/2) / W) * 0.65
            r = int(base[0] * (0.42 + 0.45 * (1-ratio)) * vignette)
            g = int(base[1] * (0.42 + 0.45 * (1-ratio)) * vignette)
            b = int(base[2] * (0.48 + 0.55 * (1-ratio)) * vignette)
            px[x, y] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

    return img.filter(ImageFilter.GaussianBlur(radius=0.4))

def _draw_network(draw, region):
    accent = get_region_color(region)
    random.seed(str(region))
    points = [(random.randint(60, W-60), random.randint(150, H-150)) for _ in range(24)]

    for i, p1 in enumerate(points):
        for p2 in points[i+1:i+4]:
            draw.line([p1, p2], fill=(255,255,255,35), width=2)

    for x, y in points:
        draw.ellipse([x-5, y-5, x+5, y+5], fill=(255,255,255))

    # heartbeat line
    y = 1515
    pts = [(80, y), (210, y), (250, y-50), (295, y+60), (350, y-110), (410, y), (1000, y)]
    draw.line(pts, fill=(255,255,255), width=6)

def _draw_header(draw, region):
    small = _font(34, False)
    bold = _font(42, True)
    draw.text((70, 65), BRAND_NAME, fill="white", font=bold)
    draw.text((70, 120), f"{region} • Healthcare AI News", fill=(230,230,230), font=small)

def _draw_footer(draw, source):
    small = _font(31, False)
    source_text = f"Source: {source}"[:58]
    draw.rounded_rectangle([55, 1685, 1025, 1815], radius=28, fill=(0,0,0,95), outline=(255,255,255,80), width=2)
    draw.text((85, 1715), source_text, fill="white", font=small)
    draw.text((85, 1762), "Source-grounded. AI-powered. Health focused.", fill=(230,230,230), font=small)

def _draw_text_block(draw, title, subtitle=None, y=420, title_size=76, max_width=920):
    title_font = _font(title_size, True)
    sub_font = _font(42, False)
    lines = _wrap(title, title_font, max_width)[:7]

    cur_y = y
    for line in lines:
        draw.text((70, cur_y), line, fill="white", font=title_font)
        cur_y += title_size + 12

    if subtitle:
        cur_y += 35
        sub_lines = _wrap(subtitle, sub_font, max_width)[:4]
        for line in sub_lines:
            draw.text((72, cur_y), line, fill=(235,235,235), font=sub_font)
            cur_y += 55

def create_scene_image(
    scene_type: str,
    title: str,
    region: str,
    source: str,
    output_dir: str = "video/outputs",
    subtitle: str = ""
) -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    img = _gradient_background(region).convert("RGBA")
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay, "RGBA")

    # geometric accents
    accent = get_region_color(region)
    draw.ellipse([650, -120, 1250, 480], fill=(255,255,255,26), outline=(255,255,255,70), width=4)
    draw.ellipse([-220, 1180, 480, 1960], fill=(0,0,0,55), outline=(255,255,255,55), width=4)

    _draw_network(draw, region)
    _draw_header(draw, region)

    if scene_type == "hook":
        draw.text((70, 270), "BREAKING HEALTH AI", fill=(255,255,255), font=_font(38, True))
        _draw_text_block(draw, title, subtitle or "The global AI health race is accelerating.", y=375, title_size=78)
    elif scene_type == "main":
        draw.text((70, 270), "THE DEVELOPMENT", fill=(255,255,255), font=_font(38, True))
        _draw_text_block(draw, title, subtitle or "A new healthcare AI story is gaining attention.", y=380, title_size=68)
    elif scene_type == "impact":
        draw.text((70, 270), "WHY IT MATTERS", fill=(255,255,255), font=_font(38, True))
        _draw_text_block(draw, subtitle or title, "Hospitals, patients, and health systems are watching closely.", y=390, title_size=66)
    elif scene_type == "source":
        draw.text((70, 270), "SOURCE CHECK", fill=(255,255,255), font=_font(38, True))
        _draw_text_block(draw, f"Reported by {source}", "Every MedPulse AI Global video is built from cited sources.", y=410, title_size=70)
    else:
        _draw_text_block(draw, title, subtitle, y=380, title_size=70)

    _draw_footer(draw, source)

    final = Image.alpha_composite(img, overlay).convert("RGB")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    safe_region = str(region or "global").lower().replace(" ", "_")
    out = Path(output_dir) / f"scene_{safe_region}_{scene_type}_{stamp}.png"
    final.save(out)
    return str(out)

def generate_story_scenes(title: str, region: str, source: str, output_dir: str = "video/outputs") -> list[str]:
    theme = get_region_theme_name(region)
    return [
        create_scene_image("hook", title, region, source, output_dir, subtitle=f"{theme} regional briefing"),
        create_scene_image("main", title, region, source, output_dir, subtitle="Here is the key development."),
        create_scene_image("impact", title, region, source, output_dir, subtitle="This could shape how healthcare AI is adopted."),
        create_scene_image("source", title, region, source, output_dir, subtitle="Source-grounded reporting."),
    ]
