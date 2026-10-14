
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_title_extractor import JobTitleExtractorTool


JOBS = [
    {
        "company": "G-Research",
        "url": (
            "https://www.gresearch.com/"
            "vacancies/software-engineer-ai/"
        ),
    },
    {
        "company": "DataCamp",
        "url": (
            "https://job-boards.greenhouse.io/"
            "datacamp/jobs/8074115"
        ),
    },
]


def main():
    extractor = JobTitleExtractorTool()

    for job in JOBS:
        print("\n" + "=" * 60)
        print("Employer:", job["company"])

        try:
            response = requests.get(
                job["url"],
                timeout=20
            )
            response.raise_for_status()

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            title = extractor.extract(soup)

            print("Extracted title:", title)

            assert title is not None
            assert len(title) > 3

        except requests.RequestException as error:
            print("HTTP request failed:", error)
            raise

    print("\nALL TITLE EXTRACTION TESTS PASSED")


if __name__ == "__main__":
    main()
