
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_location_extractor import JobLocationExtractorTool


JOBS = [
    (
        "G-Research",
        "https://www.gresearch.com/vacancies/software-engineer-ai/"
    ),
    (
        "DataCamp",
        "https://job-boards.greenhouse.io/datacamp/jobs/8074115"
    ),
]


def main():
    extractor = JobLocationExtractorTool()

    for employer, url in JOBS:
        print("\n" + "=" * 60)
        print("Employer:", employer)

        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=20,
        )
        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        locations = extractor.extract(soup)

        print("Extracted locations:", locations)

        if not locations:
            print("Location unavailable in JSON-LD")

    print("\nLOCATION EXTRACTION DIAGNOSTIC COMPLETE")


if __name__ == "__main__":
    main()
