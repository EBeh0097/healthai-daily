from video.cinematic_styles import CINEMATIC_STYLE, get_region_visual_guidance

def build_visual_prompt(title: str, region: str, source: str, scene_type: str = "hook", snippet: str = "") -> str:
    scene_focus = {
        "hook": "dramatic opening visual for a breaking healthcare AI news short",
        "main": "main explanatory visual showing the healthcare AI development",
        "impact": "broader impact on hospitals, patients, and health systems",
        "source": "clean newsroom source verification visual with data screens and citation theme",
    }.get(scene_type, "professional healthcare AI news visual")

    return f"""
Create a vertical 9:16 image for a short-form healthcare AI news video.

Scene focus: {scene_focus}
Story title: {title}
Region: {region}
Regional visual context: {get_region_visual_guidance(region)}
Story context: {snippet}
Source context: {source}

Style: {CINEMATIC_STYLE}

Composition:
- vertical 1080x1920 style composition
- leave safe space in upper left for text overlays
- leave safe space near bottom for source attribution
- no real logos, no copyrighted characters, no fake media branding
- no gore, no patient-identifiable faces
- avoid stereotypes and deficit framing
- show healthcare AI in a factual, premium, globally credible way
"""
