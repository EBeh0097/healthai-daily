from video.scene_generator import generate_story_scenes
from video.ai_image_generator import generate_ai_story_scenes

def get_story_scenes(title: str, region: str, source: str, snippet: str = "",
                     output_dir: str = "video/outputs", use_ai_images: bool = False) -> list[str]:
    if use_ai_images:
        try:
            return generate_ai_story_scenes(title, region, source, snippet, output_dir="video/ai_scenes")
        except Exception as exc:
            print(f"AI image generation failed; using branded fallback scenes. Error: {exc}")

    return generate_story_scenes(title=title, region=region, source=source, output_dir=output_dir)
