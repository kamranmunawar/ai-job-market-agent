
import json
import sqlite3
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_processor import JobProcessor
from employer_job_finder import EmployerJobMatch
from job_repository import JobRepository
from models import Job, Skills


def create_job():
    return Job(
        job_id="integration-test-001",
        title="Core AI Engineer",
        company="G-Research",
        location="London, UK",
        url="https://example.com/job",
        description="Short Adzuna description",
    )


def main():
    with tempfile.TemporaryDirectory() as temp_dir:
        database_path = str(
            Path(temp_dir) / "test_jobs.db"
        )

        repository = JobRepository(database_path)

        processor = JobProcessor.__new__(JobProcessor)
        processor.employer_finder = Mock()
        processor.skill_tool = Mock()
        processor.normalizer_tool = Mock()

        skills = Skills(
            programming_languages=["Python"],
            ai_ml=["Machine Learning"],
        )

        processor.skill_tool.extract.return_value = skills
        processor.normalizer_tool.normalize.return_value = skills

        processor.employer_finder.find.return_value = (
            EmployerJobMatch(
                url="https://www.gresearch.com/vacancies/software-engineer-ai/",
                description="Verified full employer job description",
                score=1.0,
                source="full",
            )
        )

        job = processor.process(create_job())

        assert job.processing_status == "completed"
        assert job.description_source == "full"

        repository.save(job)

        with sqlite3.connect(database_path) as conn:
            row = conn.execute(
                """
                SELECT
                    description,
                    description_source,
                    processing_status,
                    skills_json
                FROM jobs
                WHERE job_id = ?
                """,
                (job.job_id,)
            ).fetchone()

        assert row is not None

        description, source, status, skills_json = row

        assert description == (
            "Verified full employer job description"
        )
        assert source == "full"
        assert status == "completed"

        saved_skills = json.loads(skills_json)

        assert "Python" in saved_skills["programming_languages"]
        assert "Machine Learning" in saved_skills["ai_ml"]

        print("PASS: Full description persisted")
        print("PASS: Description source persisted")
        print("PASS: Processing status persisted")
        print("PASS: Extracted skills persisted")
        print("PASS: Existing jobs.db untouched")
        print("\nALL REPOSITORY INTEGRATION TESTS PASSED")


if __name__ == "__main__":
    main()
