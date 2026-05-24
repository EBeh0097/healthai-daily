# MedPulse AI Global — Phase 2

Autonomous, source-grounded healthcare AI newsroom MVP.

## Features

- Searches healthcare AI news by continent
- Covers North America, Latin America, Europe, Asia, and Africa
- Generates Morning and Evening reports
- Selects 2 top stories per continent
- Requires source URLs for every story
- Generates fact-check notes and Shorts scripts
- Saves structured reports
- Includes GitHub Actions scheduler

## Required Streamlit/GitHub secrets

- OPENAI_API_KEY
- SERPAPI_API_KEY


## Phase 3A added

- ElevenLabs narration engine
- `video/voice_generator.py`
- `video/outputs/` for generated audio/video
- Dashboard button to generate MP3 narration from approved Shorts scripts

Required new secret:

- `ELEVENLABS_API_KEY`

Optional:

- `ELEVENLABS_VOICE_ID`
