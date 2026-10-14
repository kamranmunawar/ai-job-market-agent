
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_search import SearchJobsTool


def main():
    search_tool = SearchJobsTool()

    query = "AI Engineer"

    print("Retrieving page 1...")
    page_1 = search_tool.search(
        query=query,
        results_per_page=5,
        page=1
    )

    print("\nRetrieving page 2...")
    page_2 = search_tool.search(
        query=query,
        results_per_page=5,
        page=2
    )

    ids_1 = {
        job.job_id
        for job in page_1
        if job.job_id
    }

    ids_2 = {
        job.job_id
        for job in page_2
        if job.job_id
    }

    print("\nPAGINATION TEST")
    print("=" * 60)

    print(f"Page 1 jobs: {len(page_1)}")
    print(f"Page 2 jobs: {len(page_2)}")

    print(f"Page 1 IDs: {ids_1}")
    print(f"Page 2 IDs: {ids_2}")

    overlap = ids_1.intersection(ids_2)

    print(f"Overlapping job IDs: {len(overlap)}")

    assert page_1, "Page 1 returned no jobs"
    assert page_2, "Page 2 returned no jobs"

    assert not overlap, (
        f"Unexpected duplicate job IDs across pages: {overlap}"
    )

    print("\nPASS: Pagination retrieves distinct job results")


if __name__ == "__main__":
    main()
