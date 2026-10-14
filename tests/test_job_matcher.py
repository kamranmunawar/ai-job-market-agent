
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_matcher import JobMatcherTool


def main():
    matcher = JobMatcherTool()

    snippet = (
        "We are seeking a Senior AI Engineer to build "
        "production machine learning systems using Python, "
        "PyTorch and Azure. The successful candidate will "
        "develop reliable AI applications and collaborate "
        "with engineering teams."
    )

    matching_description = (
        "About the company. "
        + snippet
        + " Additional responsibilities include monitoring "
          "models and deploying applications using Docker."
    )

    unrelated_description = (
        "We are seeking a Senior Marketing Manager to lead "
        "campaigns, manage advertising budgets and coordinate "
        "brand strategy across international markets."
    )

    matching_score = matcher.calculate_match(
        snippet,
        matching_description
    )

    unrelated_score = matcher.calculate_match(
        snippet,
        unrelated_description
    )

    print(f"Matching description: {matching_score:.2%}")
    print(f"Unrelated description: {unrelated_score:.2%}")

    assert matcher.is_match(
        snippet,
        matching_description
    )

    assert not matcher.is_match(
        snippet,
        unrelated_description
    )

    print("\nALL JOB MATCHER TESTS PASSED")


if __name__ == "__main__":
    main()
