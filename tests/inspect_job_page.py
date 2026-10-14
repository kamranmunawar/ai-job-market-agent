import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_search import SearchJobsTool


def main():
    search_tool = SearchJobsTool()

    jobs = search_tool.search(
        query="AI Engineer",
        results_per_page=1
    )

    if not jobs:
        print("No jobs found")
        return

    job = jobs[0]

    print(f"\nJOB: {job.title}")
    print(f"COMPANY: {job.company}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(X11; Linux x86_64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/120 Safari/537.36"
        )
    }

    response = requests.get(
        str(job.url),
        headers=headers,
        timeout=30
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    print("\nFINDING JOB DESCRIPTION")
    print("=" * 70)

    # Search for distinctive text from the Adzuna API description
    description_preview = job.description[:80]

    print(f"Searching for: {description_preview}")

    for element in soup.find_all(string=True):
        if description_preview[:40].lower() in element.lower():

            parent = element.parent

            print("\nMATCH FOUND")
            print(f"TAG: {parent.name}")
            print(f"CLASS: {parent.get('class')}")
            print(f"ID: {parent.get('id')}")

            print("\nPARENT ELEMENTS")
            print("=" * 70)

            for level in range(5):
                if parent is None:
                    break

                text = parent.get_text(" ", strip=True)

                print(f"\nLEVEL {level}")
                print(f"TAG: {parent.name}")
                print(f"CLASS: {parent.get('class')}")
                print(f"ID: {parent.get('id')}")
                print(f"TEXT LENGTH: {len(text)}")
                print(f"PREVIEW: {text[:300]}")

                parent = parent.parent

            break


if __name__ == "__main__":
    main()