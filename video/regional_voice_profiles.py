"""
Region-aware voice guidance for MedPulse AI Global.

These profiles do not mimic or stereotype accents.
They guide tone, pacing, and delivery style for respectful regional reporting.

Optional voice secrets:
- ELEVENLABS_VOICE_ID_MALE
- ELEVENLABS_VOICE_ID_FEMALE
- ELEVENLABS_VOICE_ID_NORTH_AMERICA_MALE
- ELEVENLABS_VOICE_ID_NORTH_AMERICA_FEMALE
- ELEVENLABS_VOICE_ID_LATIN_AMERICA_MALE
- ELEVENLABS_VOICE_ID_LATIN_AMERICA_FEMALE
- ELEVENLABS_VOICE_ID_EUROPE_MALE
- ELEVENLABS_VOICE_ID_EUROPE_FEMALE
- ELEVENLABS_VOICE_ID_ASIA_MALE
- ELEVENLABS_VOICE_ID_ASIA_FEMALE
- ELEVENLABS_VOICE_ID_AFRICA_MALE
- ELEVENLABS_VOICE_ID_AFRICA_FEMALE
"""

REGIONAL_VOICE_PROFILES = {
    "North America": {
        "voice_secret": "ELEVENLABS_VOICE_ID_NORTH_AMERICA",
        "male_voice_secret": "ELEVENLABS_VOICE_ID_NORTH_AMERICA_MALE",
        "female_voice_secret": "ELEVENLABS_VOICE_ID_NORTH_AMERICA_FEMALE",
        "tone": "clear, confident, newsroom-style, concise",
        "pace": "medium-fast",
        "delivery": "professional and direct, with strong emphasis on facts and impact",
    },
    "Latin America": {
        "voice_secret": "ELEVENLABS_VOICE_ID_LATIN_AMERICA",
        "male_voice_secret": "ELEVENLABS_VOICE_ID_LATIN_AMERICA_MALE",
        "female_voice_secret": "ELEVENLABS_VOICE_ID_LATIN_AMERICA_FEMALE",
        "tone": "warm, energetic, respectful, globally professional",
        "pace": "medium",
        "delivery": "engaging but factual, with care not to exaggerate regional context",
    },
    "Europe": {
        "voice_secret": "ELEVENLABS_VOICE_ID_EUROPE",
        "male_voice_secret": "ELEVENLABS_VOICE_ID_EUROPE_MALE",
        "female_voice_secret": "ELEVENLABS_VOICE_ID_EUROPE_FEMALE",
        "tone": "polished, measured, analytical, policy-aware",
        "pace": "medium",
        "delivery": "calm and authoritative, especially for regulation, hospital systems, and AI safety",
    },
    "Asia": {
        "voice_secret": "ELEVENLABS_VOICE_ID_ASIA",
        "male_voice_secret": "ELEVENLABS_VOICE_ID_ASIA_MALE",
        "female_voice_secret": "ELEVENLABS_VOICE_ID_ASIA_FEMALE",
        "tone": "precise, innovation-focused, respectful, globally accessible",
        "pace": "medium-fast",
        "delivery": "clear and technology-forward, with careful pronunciation of country and institution names",
    },
    "Africa": {
        "voice_secret": "ELEVENLABS_VOICE_ID_AFRICA",
        "male_voice_secret": "ELEVENLABS_VOICE_ID_AFRICA_MALE",
        "female_voice_secret": "ELEVENLABS_VOICE_ID_AFRICA_FEMALE",
        "tone": "warm, dignified, optimistic, innovation-centered",
        "pace": "medium",
        "delivery": "respectful and empowering, emphasizing health access, digital health, and local innovation without deficit framing",
    },
}

DEFAULT_PROFILE = {
    "voice_secret": "ELEVENLABS_VOICE_ID",
    "male_voice_secret": "ELEVENLABS_VOICE_ID_MALE",
    "female_voice_secret": "ELEVENLABS_VOICE_ID_FEMALE",
    "tone": "professional, factual, culturally respectful",
    "pace": "medium",
    "delivery": "credible global healthcare AI news delivery",
}

def get_voice_profile(region: str) -> dict:
    return REGIONAL_VOICE_PROFILES.get(region, DEFAULT_PROFILE)
