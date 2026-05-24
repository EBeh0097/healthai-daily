from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip
from video.branding import BRAND_NAME, get_region_color, get_region_theme_name

def create_placeholder_background(
    title: str,
    region: str,
    source: str,
    output_dir: str = "video/outputs"
) -> str:
    """
    Creates a copyright-safe branded vertical background image.
    This is a placeholder foundation for later AI-generated scenes.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    width, height = 1080, 1920
    color = get_region_color(region)

    img = Image.new("RGB", (width, height), color)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 74)
        body_font = ImageFont.truetype("DejaVuSans.ttf", 42)
        small_font = ImageFont.truetype("DejaVuSans.ttf", 34)
    except Exception:
        title_font = body_font = small_font = None

    def wrap_text(text, max_chars=24):
        words = str(text).split()
        lines, line = [], ""
        for word in words:
            if len(line + " " + word) <= max_chars:
                line = (line + " " + word).strip()
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        return "\n".join(lines[:7])

    draw.text((70, 90), BRAND_NAME, fill="white", font=small_font)
    draw.text((70, 170), region, fill="white", font=body_font)
    draw.text((70, 320), wrap_text(title, 22), fill="white", font=title_font)
    draw.text((70, 1560), f"Theme: {get_region_theme_name(region)}", fill="white", font=small_font)
    draw.text((70, 1630), f"Source: {source}", fill="white", font=small_font)
    draw.text((70, 1740), "Source-grounded healthcare AI news", fill="white", font=small_font)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(output_dir) / f"background_{region.lower().replace(' ', '_')}_{stamp}.png"
    img.save(out)
    return str(out)

def assemble_short_video(
    audio_path: str,
    title: str,
    region: str,
    source: str,
    output_dir: str = "video/outputs"
) -> str:
    """
    Builds a basic 1080x1920 vertical MP4 using branded background + narration.
    Later versions will add animated captions, AI scenes, and transitions.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    bg_path = create_placeholder_background(title, region, source, output_dir)

    audio = AudioFileClip(audio_path)
    image_clip = ImageClip(bg_path).with_duration(audio.duration).with_audio(audio)

    video = CompositeVideoClip([image_clip], size=(1080, 1920))

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_region = region.lower().replace(" ", "_")
    out = Path(output_dir) / f"medpulse_short_{safe_region}_{stamp}.mp4"

    video.write_videofile(
        str(out),
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="medium"
    )

    audio.close()
    video.close()
    image_clip.close()
    return str(out)
