
import sqlite3
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from employer_job_finder import EmployerJobFinderTool


JOBS = [
    ("5904316532", "G-Research", "Core AI Engineer"),
    ("5920622036", "DataCamp", "Principal AI Engineer"),
]


def main():
    finder = EmployerJobFinderTool()

    with sqlite3.connect("data/jobs.db") as conn:
        for job_id, company, title in JOBS:
            row = conn.execute(
                "SELECT description, location FROM jobs WHERE job_id = ?",
                (job_id,)
            ).fetchone()

            assert row is not None

            snippet, location = row
            print(f"Adzuna location: {location}")

            print("\n" + "=" * 70)
            print(f"Finding: {company} — {title}")

            match = finder.find(
                company=company,
                title=title,
                snippet=snippet,
                location=location,
            )

            if match is None:
                print("No verified employer match found")
                continue

            print("\nMATCH FOUND")
            print("URL:", match.url)
            print("Description length:", len(match.description))
            print(f"Match score: {match.score:.2%}")
            print("Source:", match.source)


if __name__ == "__main__":
    main()
