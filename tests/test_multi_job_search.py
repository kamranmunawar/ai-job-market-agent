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

    print("\nUNIQUE JOBS")
    print("=" * 70)

    for index, job in enumerate(jobs, start=1):
        print(
            f"{index}. [{job.job_id}] "
            f"{job.title} - {job.company}"
        )


if __name__ == "__main__":
    main()