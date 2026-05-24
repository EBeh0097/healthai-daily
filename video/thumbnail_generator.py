from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from video.branding import BRAND_NAME, get_region_color
from video.text_utils import wrap_words, shorten_title

W, H = 1080, 1920

def _font(size=72, bold=False):
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

def generate_thumbnail(title: str, region: str, source: str, background_path: str | None = None, output_dir: str = "video/thumbnails") -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    if background_path and Path(background_path).exists():
        img = Image.open(background_path).convert("RGB").resize((W, H)).filter(ImageFilter.GaussianBlur(radius=2))
    else:
        color = get_region_color(region)
        img = Image.new("RGB", (W, H), color)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 85))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img, "RGBA")

    brand_font = _font(40, True)
    title_font = _font(88, True)
    meta_font = _font(38, False)
    tag_font = _font(48, True)

    draw.rounded_rectangle([55, 55, 1025, 155], radius=28, fill=(0,0,0,160), outline=(255,255,255,85), width=2)
    draw.text((85, 85), f"{BRAND_NAME} • {region}", fill="white", font=brand_font)

    draw.rounded_rectangle([70, 300, 1010, 1090], radius=44, fill=(0,0,0,175))
    y = 350
    for line in wrap_words(shorten_title(title, 11), max_chars=19, max_lines=6):
        draw.text((105, y), line.upper(), fill="white", font=title_font)
        y += 100

    draw.rounded_rectangle([70, 1210, 750, 1310], radius=28, fill=(255,255,255,230))
    draw.text((105, 1232), "HEALTH AI NEWS", fill=(0,0,0), font=tag_font)

    draw.text((80, 1725), f"Source: {source}"[:65], fill=(235,235,235), font=meta_font)
    draw.text((80, 1785), "Factual • Global • AI-powered", fill=(235,235,235), font=meta_font)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_region = region.lower().replace(" ", "_")
    out = Path(output_dir) / f"thumbnail_{safe_region}_{stamp}.png"
    img.convert("RGB").save(out)
    return str(out)
