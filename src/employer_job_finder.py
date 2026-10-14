
from dataclasses import dataclass

from ddgs import DDGS
from ddgs.exceptions import DDGSException

from job_description_fetcher import JobDescriptionFetcherTool
from job_matcher import JobMatcherTool
import requests
from bs4 import BeautifulSoup
from job_location_extractor import JobLocationExtractorTool
from job_location_matcher import JobLocationMatcherTool
from job_title_extractor import JobTitleExtractorTool
from job_title_matcher import JobTitleMatcherTool
from job_employer_extractor import JobEmployerExtractorTool
from job_employer_matcher import JobEmployerMatcherTool
@dataclass
class EmployerJobMatch:
    url: str
    description: str
    score: float
    source: str


class EmployerJobFinderTool:

    def __init__(self):
        self.fetcher = JobDescriptionFetcherTool()
        self.matcher = JobMatcherTool()
        self.title_extractor = JobTitleExtractorTool()
        self.title_matcher = JobTitleMatcherTool()
        self.employer_extractor = JobEmployerExtractorTool()
        self.employer_matcher = JobEmployerMatcherTool()
        self.location_extractor = JobLocationExtractorTool()
        self.location_matcher = JobLocationMatcherTool()

    def find(
            self,
            company: str,
            title: str,
            snippet: str,
            location: str,
            threshold: float = 0.90,
            max_results: int = 5
    ) -> EmployerJobMatch | None:

        queries = [
            f'"{company}" "{title}"',
            f'{company} {title} careers',
        ]

        checked_urls = set()
        best_match = None

        for query in queries:
            print(f"\nSearching employer pages: {query}")

            try:
                results = DDGS(timeout=15).text(
                    query,
                    max_results=max_results
                )
            except DDGSException as error:
                print(f"Search unavailable: {error}")
                continue

            for result in results or []:
                url = result.get("href") or result.get("url")

                if not url or url in checked_urls:
                    continue

                checked_urls.add(url)

                # Avoid using Adzuna snippets as full descriptions.
                if "adzuna.co.uk" in url.lower():
                    continue

                print(f"Checking: {url}")

                # Verify the actual advertised title before
                # comparing job descriptions.
                try:
                    response = requests.get(
                        url,
                        timeout=20
                    )
                    response.raise_for_status()

                    soup = BeautifulSoup(
                        response.text,
                        "html.parser"
                    )

                    employer_title = self.title_extractor.extract(soup)

                    print(f"Employer title: {employer_title}")

                    if not employer_title:
                        print("Rejected: vacancy title unavailable")
                        continue

                    if not self.title_matcher.is_match(
                            title,
                            employer_title
                    ):
                        print(
                            "Rejected: title mismatch "
                            f"({title!r} vs {employer_title!r})"
                        )
                        continue

                    print("Title verified")

                    # Verify employer identity using structured data
                    # or a previously verified recruitment URL.
                    extracted_employer = self.employer_extractor.extract(soup)

                    print(f"Extracted employer: {extracted_employer}")

                    if not self.employer_matcher.is_match(
                            expected_employer=company,
                            extracted_employer=extracted_employer,
                            url=url,
                    ):
                        print("Rejected: employer identity not verified")
                        continue

                    print("Employer verified")
                    # Verify the vacancy location.
                    employer_locations = self.location_extractor.extract(soup)

                    print(f"Adzuna location: {location}")
                    print(f"Employer locations: {employer_locations}")

                    if not self.location_matcher.is_match(
                            adzuna_location=location,
                            employer_locations=employer_locations,
                    ):
                        print("Rejected: location not verified")
                        continue

                    print("Location verified")

                except requests.RequestException as error:
                    print(f"Unable to verify title: {error}")
                    continue

                print(f"Checking: {url}")

                try:

                    # Reuse the HTML page already downloaded
                    # for title and employer verification.
                    description = self.fetcher.extract_from_soup(soup)

                    if not description:
                        print("Rejected: full description unavailable")
                        continue

                    source = "full"

                    score = self.matcher.calculate_match(
                        snippet,
                        description
                    )

                    print(f"Description match: {score:.2%}")

                    if score >= threshold:
                        match = EmployerJobMatch(
                            url=url,
                            description=description,
                            score=score,
                            source=source
                        )

                        if best_match is None or score > best_match.score:
                            best_match = match

                        if score >= 0.99:
                            return best_match

                except Exception as error:
                    print(f"Unable to fetch: {error}")
                    continue

                score = self.matcher.calculate_match(
                    snippet,
                    description
                )

                print(f"Description match: {score:.2%}")

                if score >= threshold:
                    match = EmployerJobMatch(
                        url=url,
                        description=description,
                        score=score,
                        source=source
                    )

                    if best_match is None or score > best_match.score:
                        best_match = match

                    if score >= 0.99:
                        return best_match

        return best_match
