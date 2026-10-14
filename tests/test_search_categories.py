import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from multi_job_search import MultiJobSearchTool
from search_config import SEARCH_QUERIES


def main():
    search_tool = MultiJobSearchTool()

    jobs = search_tool.search(
        queries=SEARCH_QUERIES,
        results_per_query=3
    )

    print("\nJOB SEARCH CATEGORIES")
    print("=" * 70)

    for job in jobs:
        print(f"\n{job.title}")
        print(f"ID: {job.job_id}")
        print(f"Matched searches: {job.search_categories}")

    assert all(job.search_categories for job in jobs)
    assert len({job.job_id for job in jobs}) == len(jobs)

    print("\nPASS: All returned jobs have search categories and unique IDs")


if __name__ == "__main__":
    main()