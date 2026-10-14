
import sqlite3
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_description_fetcher import JobDescriptionFetcherTool
from job_matcher import JobMatcherTool


JOBS = [
    {
        "job_id": "5904316532",
        "company": "G-Research",
        "url": "https://www.gresearch.com/vacancies/software-engineer-ai/",
    },
    {
        "job_id": "5920622036",
        "company": "DataCamp",
        "url": "https://job-boards.greenhouse.io/datacamp/jobs/8074115",
    },
]


def main():
    fetcher = JobDescriptionFetcherTool()
    matcher = JobMatcherTool()

    descriptions = {}
    snippets = {}

    with sqlite3.connect("data/jobs.db") as conn:
        for job in JOBS:
            job_id = job["job_id"]

            row = conn.execute(
                "SELECT description FROM jobs WHERE job_id = ?",
                (job_id,)
            ).fetchone()

            assert row is not None, f"Job not found: {job_id}"

            snippets[job_id] = row[0]

            full_description, source = fetcher.fetch(
                job["url"],
                fallback_description=""
            )

            assert source == "full"

            descriptions[job_id] = full_description

            score = matcher.calculate_match(
                snippets[job_id],
                full_description
            )

            print(f"\n{job['company']}")
            print(f"Description length: {len(full_description)}")
            print(f"Match score: {score:.2%}")

            assert score >= 0.90, (
                f"Expected strong match for {job['company']}"
            )

    # Negative test: compare descriptions from different employers.
    wrong_score = matcher.calculate_match(
        snippets["5904316532"],
        descriptions["5920622036"]
    )

    print("\nIncorrect employer pairing")
    print(f"Match score: {wrong_score:.2%}")

    assert wrong_score < 0.90, (
        "Incorrect vacancy was accepted"
    )

    print("\nALL REAL JOB MATCHER TESTS PASSED")


if __name__ == "__main__":
    main()
