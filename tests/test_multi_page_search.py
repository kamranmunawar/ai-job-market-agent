
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from multi_job_search import MultiJobSearchTool


def main():
    search_tool = MultiJobSearchTool()

    jobs = search_tool.search(
        queries=[
            "AI Engineer",
            "Machine Learning Engineer",
        ],
        results_per_query=5,
        pages_per_query=2,
    )

    print("\nMULTI-PAGE TEST")
    print("=" * 60)

    job_ids = [
        job.job_id
        for job in jobs
        if job.job_id is not None
    ]

    print(f"Unique jobs retrieved: {len(jobs)}")
    print(f"Unique job IDs: {len(set(job_ids))}")

    assert len(job_ids) == len(set(job_ids)), (
        "Duplicate job IDs found"
    )

    assert all(
        job.search_categories for job in jobs
    ), "Some jobs have no search category"

    assert jobs, "No jobs returned"

    print("PASS: No duplicate jobs")
    print("PASS: Every job has a search category")

    print("\nSample jobs:")

    for job in jobs[:5]:
        print(
            f"{job.job_id} | {job.title} | "
            f"{job.search_categories}"
        )


if __name__ == "__main__":
    main()
