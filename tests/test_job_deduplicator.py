import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from models import Job
from job_deduplicator import JobDeduplicator


def make_job(job_id: str, title: str) -> Job:
    return Job(
        job_id=job_id,
        title=title,
        company="Example Company",
        location="London",
        url="https://example.com/job",
        description="Example job description",
    )


def main():
    jobs = [
        make_job("101", "AI Engineer"),
        make_job("102", "ML Engineer"),
        make_job("101", "AI Engineer"),
        make_job("103", "Data Scientist"),
        make_job("102", "ML Engineer"),
    ]

    deduplicator = JobDeduplicator()
    unique_jobs = deduplicator.deduplicate(jobs)

    assert len(unique_jobs) == 3

    print(f"Original jobs: {len(jobs)}")
    print(f"Unique jobs: {len(unique_jobs)}")
    print(f"Duplicates removed: {len(jobs) - len(unique_jobs)}")

    for job in unique_jobs:
        print(f"{job.job_id}: {job.title}")


if __name__ == "__main__":
    main()