import sqlite3
from pathlib import Path

from models import Job


class JobRepository:

    def __init__(self):
        data_dir = Path(__file__).resolve().parents[1] / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        self.db_path = data_dir / "jobs.db"
        self._create_tables()

    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    company TEXT NOT NULL,
                    location TEXT,
                    url TEXT,
                    description TEXT,
                    skills_json TEXT,
                    description_source TEXT,
                    processing_status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def exists(self, job_id: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            result = conn.execute(
                "SELECT 1 FROM jobs WHERE job_id = ?",
                (job_id,)
            ).fetchone()

        return result is not None

    def save(self, job: Job):
        if job.job_id is None:
            raise ValueError("Cannot save job without job_id")

        skills_json = (
            job.skills.model_dump_json()
            if job.skills is not None
            else None
        )

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO jobs (
                    job_id, title, company, location, url,
                    description, skills_json,
                    description_source, processing_status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(job_id) DO UPDATE SET
                    title = excluded.title,
                    company = excluded.company,
                    location = excluded.location,
                    url = excluded.url,
                    description = excluded.description,
                    skills_json = excluded.skills_json,
                    description_source = excluded.description_source,
                    processing_status = excluded.processing_status
            """, (
                job.job_id,
                job.title,
                job.company,
                job.location,
                str(job.url),
                job.description,
                skills_json,
                job.description_source,
                job.processing_status,
            ))

    def count(self) -> int:
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute(
                "SELECT COUNT(*) FROM jobs"
            ).fetchone()[0]

    def get_status(self, job_id: str) -> str | None:
        with sqlite3.connect(self.db_path) as conn:
            result = conn.execute(
                "SELECT processing_status FROM jobs WHERE job_id = ?",
                (job_id,)
            ).fetchone()

        return result[0] if result else None