
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_employer_extractor import JobEmployerExtractorTool


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
    extractor = JobEmployerExtractorTool()

    for expected_employer, url in JOBS:
        print("\n" + "=" * 60)
        print("Expected employer:", expected_employer)

        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=20
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        extracted_employer = extractor.extract(soup)

        print("Extracted employer:", extracted_employer)

        if extracted_employer is None:
            print("Employer identity unavailable in JSON-LD")
        else:
            print("Employer information found")

    print("\nEMPLOYER EXTRACTION DIAGNOSTIC COMPLETE")


if __name__ == "__main__":
    main()
