import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from skill_analyzer import SkillAnalyzer


def print_analysis(title, results):
    total_jobs = results["total_jobs"]

    print(f"\n{title}")
    print("=" * 70)
    print(f"Jobs analysed: {total_jobs}")

    for skill, count in results["skill_counts"].most_common(15):
        percentage = count / total_jobs * 100 if total_jobs else 0

        print(
            f"{skill:<35} "
            f"{count:>3} jobs "
            f"({percentage:.1f}%)"
        )


def main():
    analyzer = SkillAnalyzer()

    all_results = analyzer.analyze(full_only=False)
    full_results = analyzer.analyze(full_only=True)

    print_analysis(
        "ALL LIVE JOBS",
        all_results
    )

    print_analysis(
        "FULL DESCRIPTIONS ONLY",
        full_results
    )


if __name__ == "__main__":
    main()