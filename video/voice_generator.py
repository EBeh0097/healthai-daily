import re
import requests
from datetime import datetime
from pathlib import Path
from utils.secrets import get_secret
from video.regional_voice_profiles import get_voice_profile

# ElevenLabs public/default sample voice IDs
DEFAULT_FEMALE_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel
DEFAULT_MALE_VOICE_ID = "pNInz6obpgDQGcFmaJgB"    # Adam

def clean_script_for_voice(script_text: str) -> str:
    """Extracts speakable narration from the generated Shorts script."""
    if not script_text:
        return ""

    sections = [
        "Quick intro:",
        "Hook:",
        "Main story:",
        "Why it matters:",
        "Source line:",
        "Viewer question:",
    ]

    text = script_text
    # Remove title options and hashtags from narration
    text = re.split(r"Title options:|Hashtags:", text, flags=re.I)[0]

    for label in sections:
        text = re.sub(re.escape(label), "", text, flags=re.I)

    # Backward compatible extraction if old format uses Script:
    match = re.search(r"Script:\s*(.*?)(?:Source line:|Title options:|Hashtags:|$)", text, flags=re.S | re.I)
    if match:
        text = match.group(1).strip()

    text = re.sub(r"[#*_`]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def build_culturally_sensitive_narration(script_text: str, region: str = "") -> str:
    """
    Adds respectful delivery guidance without requesting a fake accent.
    """
    profile = get_voice_profile(region)
    narration = clean_script_for_voice(script_text)

    guidance = (
        f"Read this as a {profile['tone']} healthcare AI news update. "
        f"Delivery should be {profile['delivery']}. "
        f"Use a {profile['pace']} pace. "
        "Use a professional news-anchor style. "
        "Keep the intro very brief and move directly into the news. "
        "Avoid stereotypes, fake accents, sensationalism, or deficit framing. "
        "Pronounce regional names carefully and respectfully. "
        "Now read the news script: "
    )

    return guidance + narration

def get_region_voice_id(region: str = "", voice_gender: str = "female") -> str:
    """
    Looks for a region + gender-specific ElevenLabs voice ID first.
    Fallback order:
    1. Region-specific male/female voice
    2. Global male/female voice
    3. Region default voice
    4. Global default voice
    5. Built-in fallback voice
    """
    profile = get_voice_profile(region)
    gender = (voice_gender or "female").lower().strip()

    if gender == "male":
        return (
            get_secret(profile.get("male_voice_secret", ""))
            or get_secret("ELEVENLABS_VOICE_ID_MALE")
            or get_secret(profile.get("voice_secret", ""))
            or get_secret("ELEVENLABS_VOICE_ID")
            or DEFAULT_MALE_VOICE_ID
        )

    return (
        get_secret(profile.get("female_voice_secret", ""))
        or get_secret("ELEVENLABS_VOICE_ID_FEMALE")
        or get_secret(profile.get("voice_secret", ""))
        or get_secret("ELEVENLABS_VOICE_ID")
        or DEFAULT_FEMALE_VOICE_ID
    )

def generate_voice_audio(
    script_text: str,
    region: str = "",
    voice_gender: str = "female",
    output_dir: str = "video/outputs",
    filename_prefix: str = "medpulse_voice"
) -> str:
    api_key = get_secret("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY was not found. Add it to Streamlit Secrets and GitHub Secrets.")

    voice_id = get_region_voice_id(region, voice_gender=voice_gender)
    narration = build_culturally_sensitive_narration(script_text, region)

    if not narration:
        raise ValueError("No narration text was found in the script.")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": narration,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.50,
            "similarity_boost": 0.75,
            "style": 0.20,
            "use_speaker_boost": True,
        },
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_region = str(region or "global").lower().replace(" ", "_")
    safe_gender = str(voice_gender or "voice").lower()
    output_path = Path(output_dir) / f"{filename_prefix}_{safe_region}_{safe_gender}_{stamp}.mp3"
    output_path.write_bytes(response.content)
    return str(output_path)
