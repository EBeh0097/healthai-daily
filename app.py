import streamlit as st
import pandas as pd
from datetime import datetime

from agents.news_search import collect_regional_news
from agents.ranker import rank_stories_by_region
from agents.fact_check import fact_check_story
from agents.script_writer import write_shorts_script
from agents.regional.config import REGIONAL_SEARCH_CONFIG
from video.voice_generator import generate_voice_audio, clean_script_for_voice
from video.regional_voice_profiles import get_voice_profile
from video.video_assembler import assemble_short_video
from video.scene_router import get_last_scene_error

st.set_page_config(
    page_title="MedPulse AI Global",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 MedPulse AI Global — Regional Healthcare AI Newsroom")
st.caption("Source-grounded healthcare AI news from North America, Latin America, Europe, Asia, and Africa.")
st.caption("Phase 8 video engine: AI visuals, captions, motion scenes, and thumbnail generation.")

with st.sidebar:
    st.header("Report Settings")
    report_type = st.radio("Report type", ["Morning Report", "Evening Report"])
    selected_regions = st.multiselect(
        "Regions",
        options=list(REGIONAL_SEARCH_CONFIG.keys()),
        default=list(REGIONAL_SEARCH_CONFIG.keys()),
    )
    top_per_region = st.slider("Stories per region", 1, 5, 2)
    generate_scripts = st.checkbox("Generate fact-check notes and Shorts scripts", value=False)
    voice_gender = st.radio("Anchor voice", ["female", "male"], horizontal=True)
    use_ai_images = st.checkbox("Use AI-generated healthcare visuals", value=False)
    run_button = st.button("Run Regional Newsroom", type="primary")

if "regional_df" not in st.session_state:
    st.session_state["regional_df"] = None

if run_button:
    with st.spinner("Searching regional healthcare AI news..."):
        stories = collect_regional_news(regions=selected_regions, max_per_query=6)

    with st.spinner("Ranking top stories by continent..."):
        ranked = rank_stories_by_region(stories, top_per_region=top_per_region)

    enriched = []
    for story in ranked:
        row = story.copy()
        row["brand"] = "MedPulse AI Global"
        row["report_type"] = report_type
        row["generated_at"] = datetime.now().isoformat(timespec="seconds")

        if generate_scripts and not row.get("error"):
            with st.spinner(f"Fact-checking: {row.get('region')} — {row.get('title')[:60]}..."):
                fc = fact_check_story(row)
            row["confidence"] = fc.get("confidence", "Review Required")
            row["claim_risk"] = fc.get("claim_risk", "Review Required")
            row["fact_check_notes"] = fc.get("fact_check_notes", "")

            with st.spinner(f"Writing Shorts script: {row.get('title')[:60]}..."):
                row["shorts_script"] = write_shorts_script(row, row["fact_check_notes"])
        else:
            row["confidence"] = "Not generated"
            row["claim_risk"] = "Not generated"
            row["fact_check_notes"] = ""
            row["shorts_script"] = ""

        enriched.append(row)

    df = pd.DataFrame(enriched)
    st.session_state["regional_df"] = df

    try:
        existing = pd.read_csv("reports/daily_reports.csv")
        combined = pd.concat([existing, df], ignore_index=True)
    except Exception:
        combined = df

    combined.to_csv("reports/daily_reports.csv", index=False)

df = st.session_state.get("regional_df")

if df is None:
    st.info("Click **Run Regional Newsroom** to generate your first MedPulse AI Global regional report.")
else:
    st.subheader("Regional Report Summary")
    st.dataframe(
        df[["region", "score", "title", "source", "date", "confidence", "claim_risk", "link"]],
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Stories by Region")
    for region in df["region"].dropna().unique():
        st.markdown(f"## {region}")
        region_df = df[df["region"] == region]

        for _, row in region_df.iterrows():
            with st.expander(f"{row.get('title')} — Score {row.get('score')}"):
                st.write(f"**Source:** {row.get('source')}")
                st.write(f"**Published/Date shown:** {row.get('date')}")
                st.write(f"**URL:** {row.get('link')}")
                st.write(f"**Snippet:** {row.get('snippet')}")
                st.write(f"**Confidence:** {row.get('confidence')}")
                st.write(f"**Medical claim risk:** {row.get('claim_risk')}")

                if row.get("fact_check_notes"):
                    st.markdown("### Fact-check notes")
                    st.write(row.get("fact_check_notes"))

                if row.get("shorts_script"):
                    st.markdown("### Shorts Script")
                    st.write(row.get("shorts_script"))

                    st.markdown("### Narration Preview")
                    voice_profile = get_voice_profile(row.get("region"))
                    st.write(f"**Regional voice tone:** {voice_profile.get('tone')}")
                    st.write(f"**Delivery guidance:** {voice_profile.get('delivery')}")
                    narration = clean_script_for_voice(row.get("shorts_script"))
                    st.write(narration)

                    if st.button(f"Generate voice audio for this story", key=f"voice_{row.name}"):
                        with st.spinner("Generating ElevenLabs narration..."):
                            try:
                                audio_path = generate_voice_audio(
                                    row.get("shorts_script"),
                                    region=row.get("region"),
                                    voice_gender=voice_gender,
                                    filename_prefix="medpulse"
                                )
                                st.success(f"Audio generated: {audio_path}")
                                st.audio(audio_path)

                                video_path = assemble_short_video(
                                    audio_path=audio_path,
                                    title=row.get("title"),
                                    region=row.get("region"),
                                    source=row.get("source"),
                                    snippet=row.get("snippet"),
                                    script_text=row.get("shorts_script"),
                                    use_ai_images=use_ai_images,
                                )
                                scene_error = get_last_scene_error()
                                if scene_error:
                                    st.warning(f"AI visuals fell back to branded scenes: {scene_error}")
                                st.success(f"Draft video generated: {video_path}")
                                st.video(video_path)
                            except Exception as e:
                                st.error(str(e))

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download this report as CSV",
        csv,
        file_name=f"medpulse_ai_global_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
    )
