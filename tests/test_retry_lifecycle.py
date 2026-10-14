
import sys
import tempfile
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from models import Job
from job_repository import JobRepository


MAX_RETRIES = 3


def main():
    with tempfile.TemporaryDirectory() as temp_dir:
        repository = JobRepository()

        # Redirect this repository instance to a temporary DB.
        repository.db_path = Path(temp_dir) / "test_jobs.db"
        repository._create_tables()

        job = Job(
            job_id="retry_test_001",
            title="AI Engineer",
            company="Test Company",
            location="London",
            url="https://example.com/jobs/1",
            description="Python and machine learning",
            processing_status="failed",
            search_categories=["AI Engineer"]
        )

        repository.save(job)

        assert repository.get_retry_count(job.job_id) == 0
        print("PASS: New job starts with retry_count=0")

        for attempt in range(1, MAX_RETRIES + 1):
            # Simulate saving the failed job again.
            repository.save(job)

            # Increment after a failed processing run.
            repository.increment_retry_count(job.job_id)

            actual = repository.get_retry_count(job.job_id)

            assert actual == attempt, (
                f"Expected retry_count={attempt}, got {actual}"
            )

            print(
                f"PASS: Failed attempt {attempt}, "
                f"retry_count={actual}"
            )

        # Verify another save does not reset the counter.
        repository.save(job)

        assert repository.get_retry_count(job.job_id) == 3
        print("PASS: Upsert preserves retry_count")

        # Verify eligibility at the retry limit.
        status = repository.get_status(job.job_id)
        retries = repository.get_retry_count(job.job_id)

        should_process = (
            status not in ("completed", "needs_review")
            and not (
                status == "failed"
                and retries >= MAX_RETRIES
            )
        )

        assert should_process is False
        print("PASS: Job excluded after reaching retry limit")

    print("\nALL RETRY LIFECYCLE TESTS PASSED")


if __name__ == "__main__":
    main()
