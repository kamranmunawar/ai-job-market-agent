
import sys
import json
import sqlite3
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_repository import JobRepository


def main():
    repository = JobRepository()

    # Existing Ocho vacancy
    job_id = "5896924922"

    categories = [
        "Machine Learning Engineer",
        "LLM Engineer"
    ]

    # Save the categories
    repository.update_search_categories(
        job_id,
        categories
    )

    # Read the categories back from SQLite
    with sqlite3.connect(repository.db_path) as conn:
        row = conn.execute(
            """
            SELECT search_categories_json
            FROM jobs
            WHERE job_id = ?
            """,
            (job_id,)
        ).fetchone()

    assert row is not None, "Job not found in database"

    saved_categories = json.loads(row[0])

    assert "Machine Learning Engineer" in saved_categories
    assert "LLM Engineer" in saved_categories

    print("PASS: Search categories persisted in SQLite")
    print(f"Job ID: {job_id}")
    print(f"Categories: {saved_categories}")


if __name__ == "__main__":
    main()

