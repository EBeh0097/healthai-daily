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


## Phase 3B added

Region-aware narration guidance has been added.

Optional region-specific ElevenLabs voice secrets:

- ELEVENLABS_VOICE_ID_NORTH_AMERICA
- ELEVENLABS_VOICE_ID_LATIN_AMERICA
- ELEVENLABS_VOICE_ID_EUROPE
- ELEVENLABS_VOICE_ID_ASIA
- ELEVENLABS_VOICE_ID_AFRICA

If these are not provided, the app falls back to:

- ELEVENLABS_VOICE_ID
- then ElevenLabs default Rachel voice


## Phase 3C added

### Upgraded newsroom-style script engine

Scripts now enforce:
- ultra-short intros
- immediate hook-first delivery
- professional anchor pacing
- continent-aware tone
- anti-clickbait rules
- high-retention Shorts structure
- Bloomberg/Reuters/CNBC-style delivery guidance

The script engine now prioritizes:
- factual authority
- retention
- professionalism
- monetization-safe delivery


## Phase 4 added

### Male/Female alternate voices

The dashboard now lets you choose:

- female anchor
- male anchor

Optional global voice secrets:

- ELEVENLABS_VOICE_ID_FEMALE
- ELEVENLABS_VOICE_ID_MALE

Optional region + gender voice secrets:

- ELEVENLABS_VOICE_ID_NORTH_AMERICA_FEMALE
- ELEVENLABS_VOICE_ID_NORTH_AMERICA_MALE
- ELEVENLABS_VOICE_ID_LATIN_AMERICA_FEMALE
- ELEVENLABS_VOICE_ID_LATIN_AMERICA_MALE
- ELEVENLABS_VOICE_ID_EUROPE_FEMALE
- ELEVENLABS_VOICE_ID_EUROPE_MALE
- ELEVENLABS_VOICE_ID_ASIA_FEMALE
- ELEVENLABS_VOICE_ID_ASIA_MALE
- ELEVENLABS_VOICE_ID_AFRICA_FEMALE
- ELEVENLABS_VOICE_ID_AFRICA_MALE

### Video foundation

Added:

- `video/branding.py`
- `video/video_assembler.py`
- copyright-safe branded vertical video draft generation
- 1080x1920 MP4 export foundation

This is a simple first MP4 draft engine. Later versions should add AI-generated scenes, animated captions, transitions, and platform publishing.


## Phase 5 added

### AI Visual Scene Engine foundation

This version replaces the flat placeholder video card with a multi-scene, copyright-safe vertical Shorts draft engine.

Added:
- `video/scene_generator.py`
- multi-scene image generation
- cinematic gradient backgrounds
- region-specific visual color themes
- headline scene
- development scene
- impact scene
- source-check scene
- subtle zoom motion
- stronger visual hierarchy

This version still avoids copyrighted footage. Later versions can add OpenAI-generated medical visuals and animated subtitles.


## Phase 6 added

### AI Visual Prompt + Scene Routing Engine

Added:
- `video/cinematic_styles.py`
- `video/visual_prompt_builder.py`
- `video/ai_image_generator.py`
- `video/scene_router.py`

New dashboard option:
- `Use AI-generated healthcare visuals`

If enabled, the app tries to generate story-specific healthcare AI visuals with OpenAI image generation. If that fails, it automatically falls back to the branded synthetic scenes from Phase 5.


## Phase 7 added

Story-aligned interactive visual engine:
- fixed OpenAI image size to `1024x1536`
- AI visuals now map to Hook, Main Development, Impact, and Source Verification
- prompts use healthcare/story keywords such as radiology, cancer, startup, Lagos, hospital, FDA, EHR, telehealth, robotics
- Streamlit now shows a warning if AI images fail and fallback scenes are used
