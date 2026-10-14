
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from category_skill_analyzer import CategorySkillAnalyzer
from search_config import SEARCH_QUERIES


def main():
    analyzer = CategorySkillAnalyzer()

    results = analyzer.analyze(full_only=False)

    print("\nSKILL DEMAND BY JOB CATEGORY")
    print("=" * 70)

    for category in SEARCH_QUERIES:
        data = results.get(category)

        print(f"\n{category}")
        print("-" * 70)

        if not data:
            print("No completed jobs with stored category metadata")
            continue

        total = data["total_jobs"]
        print(f"Jobs analysed: {total}")

        for skill, count in data["skill_counts"].most_common(10):
            percentage = count / total * 100 if total else 0

            print(
                f"{skill:<35} "
                f"{count:>3} jobs "
                f"({percentage:.1f}%)"
            )


if __name__ == "__main__":
    main()
