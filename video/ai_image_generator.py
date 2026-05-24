import base64
from pathlib import Path
from datetime import datetime
from openai import OpenAI
from utils.secrets import get_secret
from video.visual_prompt_builder import build_visual_prompt
from video.scene_planner import plan_story_scenes

def generate_ai_scene_image(title: str, region: str, source: str, scene_type: str = "hook",
                            snippet: str = "", main_point: str = "", output_dir: str = "video/ai_scenes") -> str:
    api_key = get_secret("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY was not found.")
    client = OpenAI(api_key=api_key)
    prompt = build_visual_prompt(title, region, source, scene_type, snippet, main_point)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    result = client.images.generate(model="gpt-image-1", prompt=prompt, size="1024x1536", n=1)
    image_bytes = base64.b64decode(result.data[0].b64_json)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    safe_region = str(region or "global").lower().replace(" ", "_")
    out = Path(output_dir) / f"ai_scene_{safe_region}_{scene_type}_{stamp}.png"
    out.write_bytes(image_bytes)
    return str(out)

def generate_ai_story_scenes(title: str, region: str, source: str, snippet: str = "",
                             script_text: str = "", output_dir: str = "video/ai_scenes") -> list[str]:
    paths = []
    for scene in plan_story_scenes(title, snippet, script_text):
        paths.append(generate_ai_scene_image(title, region, source, scene["scene_type"], snippet, scene["main_point"], output_dir))
    return paths
