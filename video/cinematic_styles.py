CINEMATIC_STYLE = """
premium global technology newsroom aesthetic, cinematic healthcare documentary style,
modern medical AI visuals, high-end broadcast graphics, clean composition,
subtle futuristic interface overlays, realistic lighting, professional color grading,
no logos, no copyrighted brand marks, no sensational imagery, no gore
"""

REGION_VISUAL_GUIDANCE = {
    "North America": "North American healthcare innovation context, advanced hospital systems, clinical AI dashboards, blue and steel visual tone",
    "Latin America": "Latin American digital health innovation context, modern clinics, telehealth, emerald and teal visual tone",
    "Europe": "European regulated healthcare AI context, hospitals, AI safety, navy and gold visual tone",
    "Asia": "Asian health technology innovation context, smart hospitals, robotics, precision technology, purple and neon visual tone",
    "Africa": "African healthtech innovation context, digital health access, modern clinics, respectful empowering representation, sunset orange visual tone",
}

def get_region_visual_guidance(region: str) -> str:
    return REGION_VISUAL_GUIDANCE.get(region, "global healthcare AI newsroom visuals")
