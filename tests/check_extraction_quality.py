
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_repository import JobRepository


def main():
    repository = JobRepository()
    jobs = repository.get_completed_skills()

    print("\nEXTRACTION QUALITY REPORT")
    print("=" * 70)

    total = 0
    empty = 0
    partial = 0

    for job in jobs:
        if job["job_id"].startswith("test_"):
            continue

        total += 1

        skills = job["skills"]

        skill_count = sum(
            len(values)
            for values in skills.values()
        )

        if job["description_source"] == "partial":
            partial += 1

        if skill_count == 0:
            empty += 1

        print(
            f"Job: {job['job_id']} | "
            f"Skills: {skill_count} | "
            f"Source: {job['description_source']} | "
            f"Categories: {job['search_categories']}"
        )

    print("\nQUALITY SUMMARY")
    print("=" * 70)
    print(f"Completed live jobs: {total}")
    print(f"Jobs with zero skills: {empty}")
    print(f"Jobs using partial descriptions: {partial}")

    if total:
        print(
            f"Non-empty extraction rate: "
            f"{(total - empty) / total * 100:.1f}%"
        )


if __name__ == "__main__":
    main()

