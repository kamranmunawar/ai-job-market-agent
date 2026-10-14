
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_title_matcher import JobTitleMatcherTool


def main():
    matcher = JobTitleMatcherTool()

    test_cases = [
        ("Core AI Engineer", "Core AI Engineer", True),
        ("Principal AI Engineer", "Principal AI Engineer", True),
        ("Applied AI Engineer", "Core AI Engineer", False),
        ("Software Engineer - AI", "Software Engineer AI", True),
        ("Senior AI Engineer", "Graduate AI Engineer", False),
        ("Principal AI Engineer", "Principal AI Engineer - AI Tutor", False),
        ("", "Core AI Engineer", False),
    ]

    for adzuna_title, employer_title, expected in test_cases:
        result = matcher.is_match(
            adzuna_title,
            employer_title
        )

        print(
            f"{adzuna_title!r} vs "
            f"{employer_title!r} -> {result}"
        )

        assert result == expected

    print("\nALL JOB TITLE MATCHER TESTS PASSED")


if __name__ == "__main__":
    main()
