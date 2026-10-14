import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from models import Job, Skills
from job_repository import JobRepository


def main():
    repository = JobRepository()

    job = Job(
        job_id="test_001",
        title="AI Engineer",
        company="Example Company",
        location="London",
        url="https://example.com/job",
        description="Python and RAG experience required.",
        skills=Skills(
            programming_languages=["Python"],
            ai_ml=["Retrieval-Augmented Generation"]
        ),
        processing_status="completed"
    )

    before = repository.count()

    repository.save(job)

    assert repository.exists("test_001")

    after_first_save = repository.count()

    repository.save(job)

    after_second_save = repository.count()

    assert after_second_save == after_first_save

    print(f"Jobs before test: {before}")
    print(f"Jobs after first save: {after_first_save}")
    print(f"Jobs after second save: {after_second_save}")
    print("Duplicate prevention: PASSED")


if __name__ == "__main__":
    main()