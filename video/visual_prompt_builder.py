from video.cinematic_styles import CINEMATIC_STYLE, get_region_visual_guidance

def extract_visual_keywords(title: str, snippet: str = "") -> str:
    text = f"{title} {snippet}".lower()
    keyword_map = {
        "radiology": "AI radiology workstation, medical imaging scans, diagnostic dashboard",
        "breast cancer": "breast cancer screening workflow, medical imaging AI, oncology analytics",
        "cancer": "oncology AI dashboard, clinical decision support, cancer screening visuals",
        "startup": "healthtech startup workspace, founder team, AI product dashboard",
        "lagos": "modern Lagos healthtech innovation hub, Nigerian digital health startup environment",
        "hospital": "smart hospital command center, clinicians using AI dashboards",
        "robot": "healthcare robotics lab, robotic assistant in clinical environment",
        "surgery": "surgical planning AI interface, operating room technology, no gore",
        "fda": "regulatory review, medical device AI approval, compliance dashboard",
        "approved": "regulated medical AI product, clinical safety verification dashboard",
        "ehr": "electronic health record AI assistant, clinical workflow optimization",
        "genomic": "genomics AI visualization, DNA data interface, precision medicine",
        "drug": "AI drug discovery lab, molecular modeling, biotech research",
        "telehealth": "telehealth AI consultation interface, remote care technology",
        "doctor": "clinician reviewing AI insights, professional healthcare setting",
        "screening": "preventive screening AI dashboard, patient population analytics",
        "machine learning": "machine learning model dashboard, healthcare data science visual",
    }
    matches = [v for k, v in keyword_map.items() if k in text]
    return "; ".join(matches[:4]) if matches else "healthcare AI dashboard, clinical analytics, global medical technology"

def build_visual_prompt(title: str, region: str, source: str, scene_type: str = "hook", snippet: str = "", main_point: str = "") -> str:
    visual_keywords = extract_visual_keywords(title, snippet)
    scene_focus = {
        "hook": f"opening visual that instantly communicates the headline: {title}",
        "main": f"visual explanation of the core development: {main_point or title}",
        "impact": "visual showing how this could affect hospitals, clinicians, patients, health systems, or access to care",
        "source": "clean newsroom verification visual showing credible source-checking, citations, data review, and editorial fact-checking",
    }.get(scene_type, "professional healthcare AI news visual")

    return f"""
Create a premium vertical 9:16 image for a short-form healthcare AI news video.

Scene type: {scene_type}
Scene focus: {scene_focus}
Story title: {title}
Main point: {main_point or title}
Region: {region}
Regional visual context: {get_region_visual_guidance(region)}
Specific visual elements to include if appropriate: {visual_keywords}
Story context: {snippet}
Source context: {source}

Style: {CINEMATIC_STYLE}

Composition requirements:
- vertical 9:16 composition for YouTube Shorts/Reels/TikTok
- cinematic, realistic, premium newsroom look
- clear focal subject, not cluttered
- add subtle healthcare AI interface overlays and data visualization elements
- leave safe space in upper left for text overlays
- leave safe space near bottom for source attribution
- no real company logos, copyrighted brand marks, or fake media branding
- no gore, no patient-identifiable faces, no frightening medical imagery
- avoid stereotypes, poverty framing, or deficit framing
- represent the region respectfully and professionally
- visually attractive, factual, and not sensational
"""
