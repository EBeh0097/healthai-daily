from pathlib import Path
from datetime import datetime

from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from video.scene_generator import generate_story_scenes

def _make_scene_clip(image_path, duration, idx):
    clip = ImageClip(image_path).with_duration(duration)
    # subtle alternating zoom via resize over time, compatible with MoviePy 2.x
    if idx % 2 == 0:
        clip = clip.resized(lambda t: 1.0 + 0.018 * t)
    else:
        clip = clip.resized(lambda t: 1.035 - 0.012 * min(t, duration))
    return clip

def assemble_short_video(
    audio_path: str,
    title: str,
    region: str,
    source: str,
    output_dir: str = "video/outputs"
) -> str:
    """
    Builds a multi-scene 1080x1920 vertical MP4 with branded visuals + narration.
    This is still copyright-safe and does not use external footage.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    audio = AudioFileClip(audio_path)
    scenes = generate_story_scenes(title=title, region=region, source=source, output_dir=output_dir)

    total = max(audio.duration, 4)
    base_duration = total / len(scenes)

    clips = []
    for idx, scene in enumerate(scenes):
        dur = base_duration
        if idx == len(scenes) - 1:
            dur = total - (base_duration * (len(scenes) - 1))
        clips.append(_make_scene_clip(scene, dur, idx))

    video = concatenate_videoclips(clips, method="compose").with_audio(audio)
    video = CompositeVideoClip([video], size=(1080, 1920))

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_region = str(region or "global").lower().replace(" ", "_")
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
    for c in clips:
        c.close()

    return str(out)
