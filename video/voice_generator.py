import re
import requests
from datetime import datetime
from pathlib import Path
from utils.secrets import get_secret

DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # ElevenLabs Rachel voice

def clean_script_for_voice(script_text: str) -> str:
    """Extracts speakable narration from the generated Shorts script."""
    if not script_text:
        return ""

    match = re.search(
        r"Script:\s*(.*?)(?:Source line:|Title options:|Hashtags:|$)",
        script_text,
        flags=re.S | re.I,
    )
    text = match.group(1).strip() if match else script_text
    text = re.sub(r"^(Hook|Script|Source line|Title options|Hashtags):", "", text, flags=re.I | re.M)
    text = re.sub(r"[#*_`]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def generate_voice_audio(script_text: str, output_dir: str = "video/outputs", filename_prefix: str = "medpulse_voice") -> str:
    api_key = get_secret("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY was not found. Add it to Streamlit Secrets and GitHub Secrets.")

    voice_id = get_secret("ELEVENLABS_VOICE_ID", DEFAULT_VOICE_ID)
    narration = clean_script_for_voice(script_text)
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
            "stability": 0.45,
            "similarity_boost": 0.75,
            "style": 0.25,
            "use_speaker_boost": True,
        },
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(output_dir) / f"{filename_prefix}_{stamp}.mp3"
    output_path.write_bytes(response.content)
    return str(output_path)
