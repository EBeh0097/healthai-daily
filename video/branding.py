BRAND_NAME = "MedPulse AI Global"

REGION_COLORS = {
    "North America": {"name": "Blue Steel", "rgb": (32, 92, 180)},
    "Latin America": {"name": "Emerald Teal", "rgb": (0, 150, 120)},
    "Europe": {"name": "Gold Navy", "rgb": (210, 165, 60)},
    "Asia": {"name": "Neon Purple", "rgb": (130, 75, 220)},
    "Africa": {"name": "Sunset Orange", "rgb": (230, 120, 45)},
}

def get_region_color(region: str):
    return REGION_COLORS.get(region, {"name": "Global Blue", "rgb": (38, 120, 190)})["rgb"]

def get_region_theme_name(region: str):
    return REGION_COLORS.get(region, {"name": "Global Blue"})["name"]
