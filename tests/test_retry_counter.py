
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_repository import JobRepository


def main():
    repository = JobRepository()

    job_id = "5761412988"

    before = repository.get_retry_count(job_id)

    repository.increment_retry_count(job_id)

    after = repository.get_retry_count(job_id)

    assert after == before + 1, (
        f"Expected {before + 1}, got {after}"
    )

    print("PASS: Retry counter increments correctly")
    print(f"Before: {before}")
    print(f"After: {after}")


if __name__ == "__main__":
    main()
