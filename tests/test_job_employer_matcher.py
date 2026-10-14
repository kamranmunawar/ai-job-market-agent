
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_employer_matcher import JobEmployerMatcherTool


def main():
    matcher = JobEmployerMatcherTool()

    tests = [
        (
            "G-Research",
            "G-Research",
            "https://www.gresearch.com/vacancies/software-engineer-ai/",
            True,
        ),
        (
            "G-Research",
            "Another Company",
            "https://www.gresearch.com/vacancies/software-engineer-ai/",
            False,
        ),
        (
            "DataCamp",
            None,
            "https://job-boards.greenhouse.io/datacamp/jobs/8074115",
            True,
        ),
        (
            "DataCamp",
            None,
            "https://job-boards.greenhouse.io/othercompany/jobs/123",
            False,
        ),
        (
            "DataCamp",
            None,
            "https://example.com/datacamp/jobs/8074115",
            False,
        ),
        (
            "Unknown Company",
            None,
            "https://unknowncompany.com/jobs/123",
            False,
        ),
    ]

    for employer, extracted, url, expected in tests:
        result = matcher.is_match(
            expected_employer=employer,
            extracted_employer=extracted,
            url=url,
        )

        print(
            f"{employer} | "
            f"Extracted: {extracted} | "
            f"Result: {result}"
        )

        assert result == expected

    print("\nALL EMPLOYER MATCHER TESTS PASSED")


if __name__ == "__main__":
    main()

