from video.scene_generator import generate_story_scenes
from video.ai_image_generator import generate_ai_story_scenes

LAST_SCENE_ERROR = ""

def get_last_scene_error() -> str:
    return LAST_SCENE_ERROR

def get_story_scenes(title: str, region: str, source: str, snippet: str = "",
                     script_text: str = "", output_dir: str = "video/outputs",
                     use_ai_images: bool = False) -> list[str]:
    global LAST_SCENE_ERROR
    LAST_SCENE_ERROR = ""
    if use_ai_images:
        try:
            return generate_ai_story_scenes(title, region, source, snippet, script_text, output_dir="video/ai_scenes")
        except Exception as exc:
            LAST_SCENE_ERROR = str(exc)
            print(f"AI image generation failed; using branded fallback scenes. Error: {exc}")
    return generate_story_scenes(title=title, region=region, source=source, output_dir=output_dir)
