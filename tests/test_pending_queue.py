
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
        repository.db_path = Path(temp_dir) / "queue_test.db"
        repository._create_tables()

        for number in range(1, 8):
            job = Job(
                job_id=f"queue_test_{number:03d}",
                title=f"AI Engineer {number}",
                company="Test Company",
                location="London",
                url=f"https://example.com/jobs/{number}",
                description="Python, machine learning",
                search_categories=["AI Engineer"],
            )

            repository.save_discovered(job)

        pending = repository.get_pending_jobs(limit=5)

        assert len(pending) == 5
        assert [job.job_id for job in pending] == [
            f"queue_test_{number:03d}"
            for number in range(1, 6)
        ]

        print("PASS: Retrieves five oldest pending jobs")

        first_job = pending[0]
        first_job.processing_status = "completed"
        repository.save(first_job)

        next_pending = repository.get_pending_jobs(limit=5)

        assert len(next_pending) == 5
        assert next_pending[0].job_id == "queue_test_002"
        assert next_pending[-1].job_id == "queue_test_006"

        print("PASS: Completed job removed from pending queue")
        print("PASS: Next pending job becomes eligible")

    print("\nALL PENDING QUEUE TESTS PASSED")


if __name__ == "__main__":
    main()
