
import sqlite3
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_description_fetcher import JobDescriptionFetcherTool
from job_matcher import JobMatcherTool


def main():
    fetcher = JobDescriptionFetcherTool()
    matcher = JobMatcherTool()

    core_url = (
        "https://www.gresearch.com/"
        "vacancies/software-engineer-ai/"
    )

    description, source = fetcher.fetch(
        url=core_url,
        fallback_description=""
    )

    assert source == "full"

    job_ids = {
        "Core AI Engineer": "5904316532",
        "Applied AI Engineer": "5904316492",
    }

    with sqlite3.connect("data/jobs.db") as conn:
        for title, job_id in job_ids.items():
            row = conn.execute(
                """
                SELECT description
                FROM jobs
                WHERE job_id = ?
                """,
                (job_id,)
            ).fetchone()

            assert row is not None

            score = matcher.calculate_match(
                row[0],
                description
            )

            print("\n" + "=" * 60)
            print("Adzuna vacancy:", title)
            print("Employer page: Core AI Engineer")
            print(f"Description match: {score:.2%}")

            if title == "Applied AI Engineer" and score >= 0.90:
                print("WARNING: Potential false positive!")

    print("\nDIAGNOSTIC COMPLETE")


if __name__ == "__main__":
    main()
