import re

def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()

def extract_script_sections(script_text: str) -> dict:
    script = str(script_text or "")
    labels = ["Quick intro", "Hook", "Main story", "Why it matters", "Source line", "Viewer question"]
    sections = {}
    for i, label in enumerate(labels):
        rest = labels[i+1:]
        lookahead = "|".join([rf"{l}:" for l in rest]) if rest else "$"
        pattern = rf"{label}:\s*(.*?)(?={lookahead}|$)"
        match = re.search(pattern, script, flags=re.S | re.I)
        sections[label.lower().replace(" ", "_")] = _clean(match.group(1)) if match else ""
    return sections

def plan_story_scenes(title: str, snippet: str = "", script_text: str = "") -> list[dict]:
    sections = extract_script_sections(script_text)
    return [
        {"scene_type": "hook", "caption": sections.get("hook") or title, "main_point": sections.get("hook") or title},
        {"scene_type": "main", "caption": "The development", "main_point": sections.get("main_story") or snippet or title},
        {"scene_type": "impact", "caption": "Why it matters", "main_point": sections.get("why_it_matters") or "Healthcare AI adoption, care delivery, and clinical workflow impact."},
        {"scene_type": "source", "caption": "Source checked", "main_point": sections.get("source_line") or "Source-grounded healthcare AI reporting."},
    ]
