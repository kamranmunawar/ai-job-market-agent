import json
import sqlite3
from pathlib import Path

from models import Job


class JobRepository:

    def __init__(self, db_path: str | Path | None = None):
        if db_path is None:
            data_dir = Path(__file__).resolve().parents[1] / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = data_dir / "jobs.db"
        else:
            self.db_path = Path(db_path)
            self.db_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

        self._create_tables()

    def get_retryable_failed_jobs(self, limit: int = 5, max_retries: int = 3) -> list[Job]:
        """
        Retrieve failed jobs that have not reached the retry limit.
        """
        if limit < 1:
            return []

        with sqlite3.connect(self.db_path) as conn:
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
                WHERE processing_status = 'failed'
                  AND retry_count < ?
                ORDER BY created_at ASC, rowid ASC
                LIMIT ?
                """,
                (max_retries, limit)
            ).fetchall()

        return [
            Job(
                job_id=row["job_id"],
                title=row["title"],
                company=row["company"],
                location=row["location"] or "Unknown",
                url=row["url"],
                description=row["description"] or "",
                description_source=row["description_source"] or "api",
                processing_status=row["processing_status"],
                search_categories=json.loads(
                    row["search_categories_json"] or "[]"
                ),
            )
            for row in rows
        ]

    def get_pending_jobs(self, limit: int = 5) -> list[Job]:
        """
        Retrieve pending jobs from SQLite in discovery order.
        """
        if limit < 1:
            return []

        with sqlite3.connect(self.db_path) as conn:
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
                WHERE processing_status = 'pending'
                ORDER BY created_at ASC, rowid ASC
                LIMIT ?
                """,
                (limit,)
            ).fetchall()

        jobs = []

        for row in rows:
            job = Job(
                job_id=row["job_id"],
                title=row["title"],
                company=row["company"],
                location=row["location"] or "Unknown",
                url=row["url"],
                description=row["description"] or "",
                description_source=row["description_source"] or "api",
                processing_status=row["processing_status"],
                search_categories=json.loads(
                    row["search_categories_json"] or "[]"
                ),
            )

            jobs.append(job)

        return jobs

    def save_discovered(self, job: Job) -> bool:
        """
        Insert a newly discovered job without overwriting
        an existing job's processing results.

        Returns True if inserted, False if already present.
        """
        if job.job_id is None:
            raise ValueError("Cannot save job without job_id")

        categories_json = json.dumps(job.search_categories)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT OR IGNORE INTO jobs (
                    job_id,
                    title,
                    company,
                    location,
                    url,
                    description,
                    description_source,
                    processing_status,
                    search_categories_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job.job_id,
                    job.title,
                    job.company,
                    job.location,
                    str(job.url),
                    job.description,
                    job.description_source,
                    "pending",
                    categories_json,
                )
            )

            inserted = cursor.rowcount == 1

            if not inserted:
                row = conn.execute(
                    """
                    SELECT search_categories_json
                    FROM jobs
                    WHERE job_id = ?
                    """,
                    (job.job_id,)
                ).fetchone()

                existing = json.loads(row[0] or "[]") if row else []

                merged = list(
                    dict.fromkeys(existing + job.search_categories)
                )

                conn.execute(
                    """
                    UPDATE jobs
                    SET search_categories_json = ?
                    WHERE job_id = ?
                    """,
                    (json.dumps(merged), job.job_id)
                )

        return inserted

    def get_retry_count(self, job_id: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("""
                SELECT retry_count
                FROM jobs
                WHERE job_id = ?
            """, (job_id,)).fetchone()

        return row[0] if row else 0

    def increment_retry_count(self, job_id: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE jobs
                SET retry_count = retry_count + 1
                WHERE job_id = ?
            """, (job_id,))

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
                    search_categories_json TEXT DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Check columns in the existing table
            columns = {
                row[1]
                for row in conn.execute("PRAGMA table_info(jobs)")
            }

            # Add the column if this is an older database
            if "search_categories_json" not in columns:
                conn.execute("""
                    ALTER TABLE jobs
                    ADD COLUMN search_categories_json TEXT DEFAULT '[]'
                """)
                print("Database migrated: added search_categories_json")
            if "retry_count" not in columns:
                conn.execute("""
                    ALTER TABLE jobs
                    ADD COLUMN retry_count INTEGER NOT NULL DEFAULT 0
                """)
                print("Database migrated: added retry_count")

            conn.commit()

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
            row = conn.execute(
                """
                SELECT search_categories_json
                FROM jobs
                WHERE job_id = ?
                """,
                (job.job_id,)
            ).fetchone()

            existing_categories = json.loads(row[0] or "[]") if row else []

            merged_categories = list(
                dict.fromkeys(existing_categories + job.search_categories)
            )

            categories_json = json.dumps(merged_categories)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO jobs (
                    job_id,
                    title,
                    company,
                    location,
                    url,
                    description,
                    skills_json,
                    description_source,
                    processing_status,
                    search_categories_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(job_id) DO UPDATE SET
                    title = excluded.title,
                    company = excluded.company,
                    location = excluded.location,
                    url = excluded.url,
                    description = excluded.description,
                    skills_json = excluded.skills_json,
                    description_source = excluded.description_source,
                    processing_status = excluded.processing_status,
                    search_categories_json = excluded.search_categories_json
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
                categories_json
            ))

    def update_search_categories(
            self,
            job_id: str,
            categories: list[str]
    ):
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                """
                SELECT search_categories_json
                FROM jobs
                WHERE job_id = ?
                """,
                (job_id,)
            ).fetchone()

            if row is None:
                return

            existing = json.loads(row[0] or "[]")

            merged = list(dict.fromkeys(existing + categories))

            conn.execute(
                """
                UPDATE jobs
                SET search_categories_json = ?
                WHERE job_id = ?
                """,
                (json.dumps(merged), job_id)
            )


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

    def get_completed_skills(self) -> list[dict]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("""
                SELECT
                    job_id,
                    skills_json,
                    description_source,
                    search_categories_json
                FROM jobs
                WHERE processing_status = 'completed'
                  AND skills_json IS NOT NULL
            """).fetchall()

        results = []

        for job_id, skills_json, source, categories_json in rows:
            results.append({
                "job_id": job_id,
                "skills": json.loads(skills_json),
                "description_source": source,
                "search_categories": json.loads(categories_json or "[]")
            })

        return results

    def get_description(self, job_id: str) -> str | None:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT description FROM jobs WHERE job_id = ?",
                (job_id,)
            ).fetchone()

        return row[0] if row else None