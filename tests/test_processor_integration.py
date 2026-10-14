
import sys
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_processor import JobProcessor
from employer_job_finder import EmployerJobMatch
from models import Job, Skills


def create_job():
    return Job(
        job_id="test-001",
        title="Core AI Engineer",
        company="G-Research",
        location="London, UK",
        url="https://example.com/job",
        description="Short Adzuna description",
    )


def main():
    # Bypass __init__ so no external tools are initialised.
    processor = JobProcessor.__new__(JobProcessor)

    processor.employer_finder = Mock()
    processor.skill_tool = Mock()
    processor.normalizer_tool = Mock()

    skills = Skills(programming_languages=["Python"])

    processor.skill_tool.extract.return_value = skills
    processor.normalizer_tool.normalize.return_value = skills

    # Test 1: Verified full description.
    processor.employer_finder.find.return_value = EmployerJobMatch(
        url="https://www.gresearch.com/vacancies/software-engineer-ai/",
        description="Full verified employer description",
        score=1.0,
        source="full",
    )

    job = processor.process(create_job())

    assert job.description == "Full verified employer description"
    assert job.description_source == "full"
    assert job.processing_status == "completed"

    processor.skill_tool.extract.assert_called_with(
        "Full verified employer description"
    )

    print("PASS: Full description selected and processed")

    # Test 2: No verified employer match.
    processor.employer_finder.find.return_value = None

    job = processor.process(create_job())

    assert job.description == "Short Adzuna description"
    assert job.description_source == "partial"
    assert job.processing_status == "completed"

    processor.skill_tool.extract.assert_called_with(
        "Short Adzuna description"
    )

    print("PASS: Adzuna fallback selected and processed")

    # Test 3: Employer search failure.
    processor.employer_finder.find.side_effect = RuntimeError(
        "Search unavailable"
    )

    job = processor.process(create_job())

    assert job.description_source == "partial"
    assert job.processing_status == "completed"

    print("PASS: Search failure handled safely")

    print("\nALL PROCESSOR INTEGRATION TESTS PASSED")


if __name__ == "__main__":
    main()
