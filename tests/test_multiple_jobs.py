import sys
import time
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_search import SearchJobsTool
from job_description_fetcher import JobDescriptionFetcherTool


def main():
    search_tool = SearchJobsTool()
    description_tool = JobDescriptionFetcherTool()

    jobs = search_tool.search(
        query="AI Engineer",
        results_per_page=5
    )

    print("\nTESTING JOB DESCRIPTION EXTRACTION")
    print("=" * 70)

    for index, job in enumerate(jobs, start=1):

        print(f"\nJOB {index}")
        print(f"Title: {job.title}")
        print(f"Company: {job.company}")

        try:
            description, source = description_tool.fetch(
                job.url,
                fallback_description=job.description
            )

            print(f"Source: {source.upper()}")
            print(f"Description length: {len(description)}")

        except Exception as error:
            print("Status: FAILED")
            print(f"Error: {error}")

        print("-" * 70)
        if index < len(jobs):
            time.sleep(2)


if __name__ == "__main__":
    main()
