
import sqlite3
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from employer_job_finder import EmployerJobFinderTool


JOB_ID = "5904316532"
DB_PATH = Path(__file__).resolve().parents[1] / "data" / "jobs.db"


def main():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        job = conn.execute(
            """
            SELECT
                job_id,
                title,
                company,
                location,
                description,
                description_source,
                processing_status
            FROM jobs
            WHERE job_id = ?
            """,
            (JOB_ID,),
        ).fetchone()

    if job is None:
        print(f"Job not found: {JOB_ID}")
        return

    print("JOB")
    print("=" * 60)
    print(f"Title: {job['title']}")
    print(f"Company: {job['company']}")
    print(f"Location: {job['location']}")
    print(f"Current source: {job['description_source']}")
    print(f"Current length: {len(job['description'] or '')}")
    print(f"Current status: {job['processing_status']}")

    finder = EmployerJobFinderTool()

    match = finder.find(
        company=job["company"],
        title=job["title"],
        snippet=job["description"] or "",
        location=job["location"],
    )

    print("\nRECOVERY RESULT")
    print("=" * 60)

    if match is None:
        print("No verified matching description found.")
        return

    print(f"URL: {match.url}")
    print(f"Match score: {match.score:.2%}")
    print(f"Recovered length: {len(match.description)}")
    print(f"Previous length: {len(job['description'] or '')}")

    print("\nDESCRIPTION PREVIEW")
    print("-" * 60)
    print(match.description[:700])

    print("\nNo database changes made.")


if __name__ == "__main__":
    main()
