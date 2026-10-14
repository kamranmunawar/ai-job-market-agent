
import argparse
import sqlite3
import json

from employer_job_finder import EmployerJobFinderTool
from job_processor import JobProcessor
from job_repository import JobRepository
from models import Job


def load_review_jobs(repository, limit):
    with sqlite3.connect(repository.db_path) as conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute(
            """
            SELECT
                job_id,
                title,
                company,
                location,
                url,
                description,
                description_source,
                processing_status,
                search_categories_json
            FROM jobs
            WHERE processing_status = 'needs_review'
            ORDER BY created_at ASC, rowid ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return rows


def main():
    parser = argparse.ArgumentParser(
        description="Recover full descriptions for review jobs"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=3,
        help="Maximum review jobs to attempt",
    )

    args = parser.parse_args()

    if args.limit < 1:
        parser.error("--limit must be greater than zero")

    repository = JobRepository()
    processor = JobProcessor()
    finder = EmployerJobFinderTool()

    rows = load_review_jobs(repository, args.limit)

    print("\nREVIEW JOB RECOVERY")
    print("=" * 60)
    print(f"Jobs selected: {len(rows)}")

    recovered = 0
    unchanged = 0

    for index, row in enumerate(rows, start=1):
        print(f"\nProcessing {index}/{len(rows)}")
        print(f"Job ID: {row['job_id']}")
        print(f"Title: {row['title']}")

        original_description = row["description"] or ""

        job = Job(
            job_id=row["job_id"],
            title=row["title"],
            company=row["company"],
            location=row["location"] or "Unknown",
            url=row["url"],
            description=original_description,
            description_source=row["description_source"] or "partial",
            processing_status="needs_review",
        )


        try:
            # 1. Search for a matching full description.
            match = finder.find(
                company=job.company,
                title=job.title,
                snippet=original_description,
                location=job.location,
            )

            # 2. Skip Ollama when no better description exists.
            if match is None:
                unchanged += 1
                print(
                    "SKIPPED: No verified full description. "
                    "Ollama not called."
                )
                continue

            if len(match.description) <= len(original_description):
                unchanged += 1
                print(
                    "SKIPPED: Description not longer. "
                    "Ollama not called."
                )
                continue

            # 3. Run skill extraction only on improved text.
            job.description = match.description
            job.description_source = "full"

            raw_skills = processor.skill_tool.extract(
                job.description
            )

            job.skills = processor.normalizer_tool.normalize(
                raw_skills
            )

            skill_count = sum(
                len(values)
                for values in job.skills.model_dump().values()
            )

            if skill_count == 0:
                unchanged += 1
                print(
                    "SKIPPED: No skills extracted. "
                    "Original record preserved."
                )
                continue

            # 4. Save only after successful extraction.
            job.processing_status = "completed"
            repository.save(job)

            recovered += 1

            print(
                f"SUCCESS: Recovered {len(job.description)} "
                f"characters and {skill_count} skills"
            )

        except Exception as error:
            unchanged += 1
            print(f"ERROR: {error}")


    print("\nRECOVERY SUMMARY")
    print("=" * 60)
    print(f"Attempted: {len(rows)}")
    print(f"Recovered: {recovered}")
    print(f"Unchanged: {unchanged}")


if __name__ == "__main__":
    main()
