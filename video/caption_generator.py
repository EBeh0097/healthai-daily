from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

from video.text_utils import wrap_words

W, H = 1080, 1920

def _font(size=58, bold=False):
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

def create_caption_overlay(caption: str, output_dir: str = "video/captions", position: str = "bottom") -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")

    font = _font(58, True)
    small = _font(34, False)
    lines = wrap_words(caption, max_chars=28, max_lines=4)

    box_h = 120 + len(lines) * 70
    y = 1280 if position == "bottom" else 240
    x1, y1, x2, y2 = 70, y, 1010, min(y + box_h, 1810)

    draw.rounded_rectangle([x1, y1, x2, y2], radius=38, fill=(0, 0, 0, 165), outline=(255, 255, 255, 70), width=2)
    draw.text((105, y1 + 30), "MEDPULSE BRIEF", fill=(180, 230, 255, 255), font=small)

    cur_y = y1 + 82
    for line in lines:
        draw.text((105, cur_y), line, fill=(255, 255, 255, 255), font=font)
        cur_y += 68

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    out = Path(output_dir) / f"caption_{stamp}.png"
    img.save(out)
    return str(out)
