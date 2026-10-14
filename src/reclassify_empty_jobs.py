
import json
import sqlite3

from job_repository import JobRepository


def main():
    repository = JobRepository()

    updated = []

    with sqlite3.connect(repository.db_path) as conn:
        rows = conn.execute("""
            SELECT job_id, skills_json
            FROM jobs
            WHERE processing_status = 'completed'
              AND skills_json IS NOT NULL
        """).fetchall()

        for job_id, skills_json in rows:
            if job_id.startswith("test_"):
                continue

            skills = json.loads(skills_json)

            skill_count = sum(
                len(values)
                for values in skills.values()
            )

            if skill_count == 0:
                conn.execute(
                    """
                    UPDATE jobs
                    SET processing_status = 'needs_review'
                    WHERE job_id = ?
                    """,
                    (job_id,)
                )

                updated.append(job_id)

    print("\nRECLASSIFICATION SUMMARY")
    print("=" * 70)
    print(f"Jobs marked needs_review: {len(updated)}")

    for job_id in updated:
        print(f" - {job_id}")


if __name__ == "__main__":
    main()
