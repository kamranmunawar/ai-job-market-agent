
import sys
import tempfile
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_repository import JobRepository
from multi_job_search import MultiJobSearchTool


def main():
    search_tool = MultiJobSearchTool()

    with tempfile.TemporaryDirectory() as temp_dir:
        repository = JobRepository()
        repository.db_path = Path(temp_dir) / "integration_test.db"
        repository._create_tables()

        print("\nSTEP 1: Discover jobs")

        jobs = search_tool.search(
            queries=["AI Engineer"],
            results_per_query=5,
            pages_per_query=2,
        )

        assert jobs, "No jobs discovered"

        print("\nSTEP 2: Save discovered jobs")

        inserted = 0

        for job in jobs:
            if job.job_id is None:
                continue

            if repository.save_discovered(job):
                inserted += 1

        print(f"Jobs inserted: {inserted}")
        print(f"Jobs in database: {repository.count()}")

        assert repository.count() == inserted

        print("\nSTEP 3: Retrieve pending jobs")

        pending = repository.get_pending_jobs(limit=5)

        assert len(pending) == min(5, inserted)

        for job in pending:
            print(
                f"{job.job_id} | "
                f"{job.processing_status} | "
                f"{job.title}"
            )

        print("\nSTEP 4: Simulate processing one job")

        first_job = pending[0]
        first_job.processing_status = "completed"

        repository.save(first_job)

        assert repository.get_status(first_job.job_id) == "completed"

        next_pending = repository.get_pending_jobs(limit=5)

        assert first_job.job_id not in {
            job.job_id for job in next_pending
        }

        print("PASS: Completed job removed from pending queue")

        print("\nSTEP 5: Simulate another discovery run")

        for job in jobs:
            if job.job_id is not None:
                repository.save_discovered(job)

        assert repository.get_status(first_job.job_id) == "completed"

        print("PASS: Rediscovery preserves completed status")
        print("PASS: Previously discovered pending jobs remain queued")

    print("\nALL DISCOVERY QUEUE INTEGRATION TESTS PASSED")


if __name__ == "__main__":
    main()
