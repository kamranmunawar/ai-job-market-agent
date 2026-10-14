
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_description_fetcher import JobDescriptionFetcherTool


def main():
    fetcher = JobDescriptionFetcherTool()

    jobs = [
        {
            "company": "G-Research",
            "title": "Core AI Engineer",
            "url": (
                "https://www.gresearch.com/"
                "vacancies/software-engineer-ai/"
            ),
        },
        {
            "company": "DataCamp",
            "title": "Principal AI Engineer",
            "url": (
                "https://job-boards.greenhouse.io/"
                "datacamp/jobs/8074115"
            ),
        },
    ]

    for job in jobs:
        print("\n" + "=" * 70)
        print(f"{job['company']} — {job['title']}")
        print("URL:", job["url"])

        try:
            description, source = fetcher.fetch(
                url=job["url"],
                fallback_description=""
            )

            print("Source:", source)
            print("Description length:", len(description))
            print("\nDescription preview:")
            print(description[:1000])

        except Exception as error:
            print("Extraction failed:", error)


if __name__ == "__main__":
    main()
