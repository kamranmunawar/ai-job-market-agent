
import argparse
import sqlite3
from pathlib import Path

from job_processor import JobProcessor
from job_repository import JobRepository
from models import Job


def main():
    parser = argparse.ArgumentParser(
        description="Reprocess a job marked needs_review"
    )
    parser.add_argument("--job-id", required=True)
    args = parser.parse_args()

    repository = JobRepository()

    with sqlite3.connect(repository.db_path) as conn:
        conn.row_factory = sqlite3.Row

        row = conn.execute(
            """
            SELECT
                job_id,
                title,
                company,
                location,
                url,
                description,
                description_source,
                processing_status
            FROM jobs
            WHERE job_id = ?
            """,
            (args.job_id,),
        ).fetchone()

    if row is None:
        print("Job not found.")
        return

    if row["processing_status"] != "needs_review":
        print(
            "Job is not marked needs_review. "
            "Skipping."
        )
        return

    original_description = row["description"] or ""

    job = Job(
        job_id=row["job_id"],
        title=row["title"],
        company=row["company"],
        location=row["location"] or "Unknown",
        url=row["url"],
        description=original_description,
        description_source=row["description_source"] or "partial",
        processing_status=row["processing_status"],
    )

    print("\nREPROCESSING REVIEW JOB")
    print("=" * 60)
    print(f"Job ID: {job.job_id}")
    print(f"Title: {job.title}")
    print(f"Original length: {len(original_description)}")

    processor = JobProcessor()
    processed_job = processor.process(job)

    # Do not overwrite an existing review job with
    # another unsuccessful extraction.
    if processed_job.processing_status != "completed":
        print(
            "\nNo successful extraction. "
            "Original database record preserved."
        )
        return

    if processed_job.description_source != "full":
        print(
            "\nNo verified full description found. "
            "Original database record preserved."
        )
        return

    repository.save(processed_job)

    print("\nRECOVERY SUCCESS")
    print("=" * 60)
    print(f"Job ID: {processed_job.job_id}")
    print(f"Status: {processed_job.processing_status}")
    print(f"Source: {processed_job.description_source}")
    print(
        f"Description length: "
        f"{len(processed_job.description)}"
    )
    print("Updated record saved to SQLite.")


if __name__ == "__main__":
    main()

