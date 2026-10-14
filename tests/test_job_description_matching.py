
import sqlite3
import sys
import re
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_description_fetcher import JobDescriptionFetcherTool


def normalise(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return " ".join(text.split())


def calculate_match(snippet: str, full_description: str) -> float:
    """
    Compare the first 200 normalised characters of
    the Adzuna snippet with the employer description.
    """

    snippet = normalise(snippet)[:200]
    full_description = normalise(full_description)

    if not snippet:
        return 0.0

    # Exact prefix substring match
    if snippet in full_description:
        return 1.0

    # Compare individual words as a diagnostic fallback
    snippet_words = set(snippet.split())
    full_words = set(full_description.split())

    if not snippet_words:
        return 0.0

    return len(snippet_words & full_words) / len(snippet_words)


jobs = [
    (
        "5904316532",
        "G-Research",
        "https://www.gresearch.com/vacancies/software-engineer-ai/"
    ),
    (
        "5920622036",
        "DataCamp",
        "https://job-boards.greenhouse.io/datacamp/jobs/8074115"
    ),
]

fetcher = JobDescriptionFetcherTool()

with sqlite3.connect("data/jobs.db") as conn:
    for job_id, company, url in jobs:
        row = conn.execute(
            "SELECT description FROM jobs WHERE job_id = ?",
            (job_id,)
        ).fetchone()

        if not row:
            print(f"Job not found: {job_id}")
            continue

        snippet = row[0]

        print("\n" + "=" * 65)
        print("Company:", company)
        print("Job ID:", job_id)

        try:
            full_description, source = fetcher.fetch(
                url=url,
                fallback_description=""
            )

            score = calculate_match(
                snippet,
                full_description
            )

            print("Description source:", source)
            print("Description length:", len(full_description))
            print(f"Match score: {score:.2%}")

            if score >= 0.90:
                print("Result: STRONG TEXT MATCH")
            elif score >= 0.70:
                print("Result: POSSIBLE MATCH — REVIEW")
            else:
                print("Result: LOW MATCH — DO NOT AUTO-ACCEPT")

        except Exception as error:
            print("Verification failed:", error)
