import streamlit as st
import pandas as pd
from datetime import datetime

from agents.news_search import collect_news, DEFAULT_QUERIES
from agents.ranker import rank_stories
from agents.fact_check import fact_check_story
from agents.script_writer import write_shorts_script

st.set_page_config(
    page_title="HealthAI Daily",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 HealthAI Daily — Source-Grounded News Agent")
st.caption("Healthcare AI news discovery, ranking, citation tracking, fact-checking, and Shorts script generation.")

with st.sidebar:
    st.header("Search Settings")
    run_mode = st.radio("Report type", ["Morning Report", "Evening Report"])
    top_n = st.slider("Number of ranked stories", 3, 15, 7)
    custom_queries = st.text_area(
        "Search queries, one per line",
        value="\n".join(DEFAULT_QUERIES),
        height=220,
    )
    generate_scripts = st.checkbox("Generate fact-check notes and Shorts scripts", value=False)
    run_button = st.button("Run News Agent", type="primary")

if "report_df" not in st.session_state:
    st.session_state["report_df"] = None

if run_button:
    queries = [q.strip() for q in custom_queries.splitlines() if q.strip()]

    with st.spinner("Searching healthcare AI news..."):
        stories = collect_news(queries=queries, max_per_query=8)

    with st.spinner("Ranking stories..."):
        ranked = rank_stories(stories, top_n=top_n)

    enriched = []
    for story in ranked:
        row = story.copy()
        row["report_type"] = run_mode
        row["generated_at"] = datetime.now().isoformat(timespec="seconds")

        if generate_scripts and not row.get("error"):
            with st.spinner(f"Fact-checking: {row.get('title')[:60]}..."):
                fc = fact_check_story(row)
            row["confidence"] = fc.get("confidence", "Review Required")
            row["fact_check_notes"] = fc.get("fact_check_notes", "")

            with st.spinner(f"Writing Shorts script: {row.get('title')[:60]}..."):
                row["shorts_script"] = write_shorts_script(row, row["fact_check_notes"])
        else:
            row["confidence"] = "Not generated"
            row["fact_check_notes"] = ""
            row["shorts_script"] = ""

        enriched.append(row)

    df = pd.DataFrame(enriched)
    st.session_state["report_df"] = df

    output_path = "reports/daily_reports.csv"
    try:
        previous = pd.read_csv(output_path)
        combined = pd.concat([previous, df], ignore_index=True)
    except Exception:
        combined = df

    combined.to_csv(output_path, index=False)

df = st.session_state.get("report_df")

if df is None:
    st.info("Click **Run News Agent** to generate your first HealthAI Daily report.")
else:
    st.subheader("Ranked Stories")
    st.dataframe(
        df[["score", "title", "source", "date", "link", "confidence"]],
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Story Cards")
    for _, row in df.iterrows():
        with st.expander(f"{row.get('title')} — Score {row.get('score')}"):
            st.write(f"**Source:** {row.get('source')}")
            st.write(f"**Published/Date shown:** {row.get('date')}")
            st.write(f"**URL:** {row.get('link')}")
            st.write(f"**Snippet:** {row.get('snippet')}")
            st.write(f"**Confidence:** {row.get('confidence')}")

            if row.get("fact_check_notes"):
                st.markdown("### Fact-check notes")
                st.write(row.get("fact_check_notes"))

            if row.get("shorts_script"):
                st.markdown("### YouTube Shorts Script")
                st.write(row.get("shorts_script"))

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download this report as CSV",
        csv,
        file_name=f"healthai_daily_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
    )
