
import json
import sqlite3
from datetime import datetime
from pathlib import Path

from models import Skills
from job_repository import JobRepository
from skill_normalizer import SkillNormalizerTool


def main():
    repository = JobRepository()
    normalizer = SkillNormalizerTool()

    db_path = Path(repository.db_path)

    backup_path = db_path.with_name(
        f"jobs_backup_{datetime.now():%Y%m%d_%H%M%S}.db"
    )

    # Create a consistent SQLite backup.
    with sqlite3.connect(db_path) as source:
        with sqlite3.connect(backup_path) as backup:
            source.backup(backup)

    print(f"Database backup created: {backup_path}")

    updated = 0
    unchanged = 0

    with sqlite3.connect(db_path) as conn:
        rows = conn.execute("""
            SELECT job_id, skills_json
            FROM jobs
            WHERE skills_json IS NOT NULL
        """).fetchall()

        for job_id, skills_json in rows:
            raw_skills = Skills.model_validate_json(skills_json)

            normalized_skills = normalizer.normalize(raw_skills)

            old_data = json.loads(skills_json)
            new_data = normalized_skills.model_dump()

            if old_data == new_data:
                unchanged += 1
                continue

            conn.execute("""
                UPDATE jobs
                SET skills_json = ?
                WHERE job_id = ?
            """, (
                normalized_skills.model_dump_json(),
                job_id
            ))

            updated += 1
            print(f"Updated: {job_id}")

    print("\nNORMALISATION SUMMARY")
    print("=" * 60)
    print(f"Records updated: {updated}")
    print(f"Records unchanged: {unchanged}")
    print(f"Backup: {backup_path}")


if __name__ == "__main__":
    main()
