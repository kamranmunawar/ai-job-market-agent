
from job_repository import JobRepository
from multi_job_search import MultiJobSearchTool
from search_config import SEARCH_QUERIES, RESULTS_PER_QUERY


def main():
    repository = JobRepository()
    search_tool = MultiJobSearchTool()

    jobs = search_tool.search(
        queries=SEARCH_QUERIES,
        results_per_query=RESULTS_PER_QUERY
    )

    updated = 0
    not_stored = 0

    for job in jobs:
        if not job.job_id:
            continue

        if repository.exists(job.job_id):
            repository.update_search_categories(
                job.job_id,
                job.search_categories
            )

            print(
                f"Updated: {job.title} "
                f"({job.job_id}) -> {job.search_categories}"
            )
            updated += 1
        else:
            not_stored += 1

    print("\nBACKFILL SUMMARY")
    print("=" * 70)
    print(f"Jobs discovered: {len(jobs)}")
    print(f"Existing database records updated: {updated}")
    print(f"Jobs not yet stored: {not_stored}")


if __name__ == "__main__":
    main()
