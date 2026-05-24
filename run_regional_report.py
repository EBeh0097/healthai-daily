import os
import pandas as pd
from datetime import datetime, timezone

from agents.news_search import collect_regional_news
from agents.ranker import rank_stories_by_region
from agents.fact_check import fact_check_story
from agents.script_writer import write_shorts_script

def run_report(report_type: str = "Automated Report", generate_scripts: bool = True):
    stories = collect_regional_news(max_per_query=6)
    ranked = rank_stories_by_region(stories, top_per_region=2)

    enriched = []
    for story in ranked:
        row = story.copy()
        row["brand"] = "MedPulse AI Global"
        row["report_type"] = report_type
        row["generated_at_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")

        if generate_scripts and not row.get("error"):
            fc = fact_check_story(row)
            row["confidence"] = fc.get("confidence")
            row["claim_risk"] = fc.get("claim_risk")
            row["fact_check_notes"] = fc.get("fact_check_notes")
            row["shorts_script"] = write_shorts_script(row, row["fact_check_notes"])
        else:
            row["confidence"] = "Not generated"
            row["claim_risk"] = "Not generated"
            row["fact_check_notes"] = ""
            row["shorts_script"] = ""

        enriched.append(row)

    df = pd.DataFrame(enriched)
    os.makedirs("reports", exist_ok=True)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")
    output_path = f"reports/medpulse_{report_type.lower().replace(' ', '_')}_{stamp}.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved report: {output_path}")
    return output_path

if __name__ == "__main__":
    report_type = os.getenv("REPORT_TYPE", "Automated Report")
    run_report(report_type=report_type, generate_scripts=True)
