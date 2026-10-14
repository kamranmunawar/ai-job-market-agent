from job_search import SearchJobsTool
from job_deduplicator import JobDeduplicator


class MultiJobSearchTool:

    def __init__(self):
        self.search_tool = SearchJobsTool()
        self.deduplicator = JobDeduplicator()

    def search(
            self,
            queries: list[str],
            results_per_query: int = 5,
            pages_per_query: int = 1,
    ):
        if pages_per_query < 1:
            raise ValueError("pages_per_query must be >= 1")

        jobs_by_id = {}

        for query in queries:
            print(f"\nSearching for: {query}")

            for page in range(1, pages_per_query + 1):
                print(f"  Fetching page {page}/{pages_per_query}")

                try:
                    jobs = self.search_tool.search(
                        query=query,
                        results_per_page=results_per_query,
                        page=page,
                    )

                except Exception as error:
                    print(
                        f"  Search failed for '{query}', "
                        f"page {page}: {error}"
                    )
                    break

                print(f"  Retrieved: {len(jobs)} jobs")

                if not jobs:
                    break

                for job in jobs:
                    job_id = job.job_id

                    if job_id is None:
                        continue

                    if job_id not in jobs_by_id:
                        job.search_categories = [query]
                        jobs_by_id[job_id] = job

                    elif query not in jobs_by_id[job_id].search_categories:
                        jobs_by_id[job_id].search_categories.append(query)

                if len(jobs) < results_per_query:
                    break

        unique_jobs = list(jobs_by_id.values())

        print("\nSEARCH SUMMARY")
        print("=" * 70)
        print(f"Unique jobs: {len(unique_jobs)}")

        return unique_jobs
