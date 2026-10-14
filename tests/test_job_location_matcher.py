
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_location_matcher import JobLocationMatcherTool


def main():
    matcher = JobLocationMatcherTool()

    cases = [
        ("London, UK", ["London, London, GB"], True),
        ("London", ["London, GB"], True),
        ("Manchester, UK", ["London, GB"], False),
        ("London, UK", ["London, United States"], False),
        ("London, UK", [], False),
        ("", ["London, GB"], False),
        ("Bristol, UK", ["London, GB", "Bristol, GB"], True),
        ("United Kingdom", ["London, GB"], False),
    ]

    for adzuna, employer, expected in cases:
        result = matcher.is_match(adzuna, employer)

        print(
            f"{adzuna!r} vs {employer!r} "
            f"-> {result}"
        )

        assert result == expected

    print("\nALL LOCATION MATCHER TESTS PASSED")


if __name__ == "__main__":
    main()
