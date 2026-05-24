from pathlib import Path
from datetime import datetime

from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
from video.scene_router import get_story_scenes
from video.caption_generator import create_caption_overlay
from video.thumbnail_generator import generate_thumbnail
from video.text_utils import shorten_title

def _make_scene_clip(image_path, duration, idx):
    clip = ImageClip(image_path).with_duration(duration)
    if idx % 2 == 0:
        clip = clip.resized(lambda t: 1.0 + 0.018 * t)
    else:
        clip = clip.resized(lambda t: 1.035 - 0.012 * min(t, duration))
    return clip

def _caption_for_scene(idx, title, region, source):
    if idx == 0:
        return shorten_title(title, 8)
    if idx == 1:
        return "The key development"
    if idx == 2:
        return "Why it matters"
    return f"Source: {source}"

def assemble_short_video(
    audio_path: str,
    title: str,
    region: str,
    source: str,
    snippet: str = "",
    script_text: str = "",
    use_ai_images: bool = False,
    output_dir: str = "video/outputs"
) -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    audio = AudioFileClip(audio_path)
    scenes = get_story_scenes(
        title=title,
        region=region,
        source=source,
        snippet=snippet,
        script_text=script_text,
        output_dir=output_dir,
        use_ai_images=use_ai_images,
    )

    total = max(audio.duration, 4)
    base_duration = total / len(scenes)

    clips = []
    for idx, scene in enumerate(scenes):
        dur = base_duration if idx < len(scenes) - 1 else total - (base_duration * (len(scenes) - 1))
        scene_clip = _make_scene_clip(scene, dur, idx)
        caption_path = create_caption_overlay(_caption_for_scene(idx, title, region, source))
        caption_clip = ImageClip(caption_path).with_duration(dur)
        composed = CompositeVideoClip([scene_clip, caption_clip], size=(1080, 1920))
        clips.append(composed)

    video = concatenate_videoclips(clips, method="compose").with_audio(audio)
    video = CompositeVideoClip([video], size=(1080, 1920))

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_region = str(region or "global").lower().replace(" ", "_")
    out = Path(output_dir) / f"medpulse_short_{safe_region}_{stamp}.mp4"

    thumb = generate_thumbnail(title=title, region=region, source=source, background_path=scenes[0])
    print(f"Thumbnail generated: {thumb}")

    video.write_videofile(
        str(out),
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="medium"
    )

    audio.close()
    video.close()
    for c in clips:
        c.close()

    return str(out)
