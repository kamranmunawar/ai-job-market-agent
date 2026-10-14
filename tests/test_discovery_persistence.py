
import sys
import tempfile
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from models import Job
from job_repository import JobRepository


def main():
    with tempfile.TemporaryDirectory() as temp_dir:
        repository = JobRepository()
        repository.db_path = Path(temp_dir) / "discovery_test.db"
        repository._create_tables()

        job = Job(
            job_id="discovery_test_001",
            title="AI Engineer",
            company="Example Company",
            location="London",
            url="https://example.com/job/1",
            description="Python and machine learning",
            search_categories=["AI Engineer"],
        )

        inserted = repository.save_discovered(job)

        assert inserted is True
        assert repository.get_status(job.job_id) == "pending"

        print("PASS: New job saved as pending")

        # Simulate successful processing.
        job.processing_status = "completed"
        repository.save(job)

        # Rediscover the same job in another category.
        job.search_categories = ["Machine Learning Engineer"]
        inserted_again = repository.save_discovered(job)

        assert inserted_again is False
        assert repository.get_status(job.job_id) == "completed"

        print("PASS: Rediscovery preserves completed status")

        with __import__("sqlite3").connect(repository.db_path) as conn:
            row = conn.execute(
                """
                SELECT search_categories_json
                FROM jobs
                WHERE job_id = ?
                """,
                (job.job_id,)
            ).fetchone()

        import json
        categories = json.loads(row[0])

        assert set(categories) == {
            "AI Engineer",
            "Machine Learning Engineer",
        }

        print("PASS: Search categories merged")
        print("PASS: Existing job not duplicated")

    print("\nALL DISCOVERY PERSISTENCE TESTS PASSED")


if __name__ == "__main__":
    main()
