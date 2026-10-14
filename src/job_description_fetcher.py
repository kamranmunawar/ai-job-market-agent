import requests
from bs4 import BeautifulSoup
import json
import re

class JobDescriptionFetcherTool:

    @staticmethod
    def extract_json_ld_description(soup: BeautifulSoup) -> str | None:
        """
        Extract a job description from JSON-LD JobPosting data.
        """

        def find_job_posting(data):
            if isinstance(data, list):
                for item in data:
                    result = find_job_posting(item)
                    if result:
                        return result

            elif isinstance(data, dict):
                types = data.get("@type", [])
                if isinstance(types, str):
                    types = [types]

                if "JobPosting" in types:
                    description = data.get("description")

                    if isinstance(description, str) and description.strip():
                        return description

                for value in data.values():
                    if isinstance(value, (dict, list)):
                        result = find_job_posting(value)
                        if result:
                            return result

            return None

        for script in soup.select('script[type="application/ld+json"]'):
            try:
                data = json.loads(script.string or script.get_text())
            except (json.JSONDecodeError, TypeError):
                continue

            description_html = find_job_posting(data)

            if description_html:
                text = BeautifulSoup(
                    description_html,
                    "html.parser"
                ).get_text(separator="\n", strip=True)

                text = re.sub(r"\n{3,}", "\n\n", text)

                if len(text) >= 100:
                    return text

        return None

    def extract_from_soup(self, soup: BeautifulSoup) -> str | None:
        """
        Extract a job description from an already
        downloaded HTML document.
        """

        # First try structured JobPosting data.
        description = self.extract_json_ld_description(soup)

        if description and len(description) >= 100:
            return description

        # Fall back to recognised HTML description sections.
        section = soup.select_one(
            "section.adp-body, .job__description"
        )

        if section is None:
            return None

        for unwanted in section.select(
                "script, style, noscript"
        ):
            unwanted.decompose()

        description = section.get_text(" ", strip=True)

        if len(description) >= 100:
            return description

        return None

    def fetch(
            self,
            url: str,
            fallback_description: str = ""
    ) -> tuple[str, str]:

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(X11; Linux x86_64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/120 Safari/537.36"
            )
        }

        try:
            response = requests.get(
                str(url),
                headers=headers,
                timeout=30
            )
            response.raise_for_status()

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            # Method 1: JSON-LD structured job description
            description = self.extract_json_ld_description(soup)

            if description:
                print("Description extracted from JSON-LD")
                return description, "full"

            # Method 2: Existing Adzuna HTML selector
            #element = soup.select_one("section.adp-body")
            element = soup.select_one(
                "section.adp-body, .job__description"
            )

            if element is not None:
                for tag in element.select(
                        "script, style, noscript"
                ):
                    tag.decompose()

                description = element.get_text(
                    separator="\n",
                    strip=True
                )

                if len(description) >= 100:
                    print("Description extracted from HTML")
                    return description, "full"

            raise ValueError(
                "No suitable job description found"
            )

        except (requests.RequestException, ValueError) as error:
            print(f"Full description unavailable: {error}")

            if fallback_description.strip():
                return fallback_description, "partial"

            raise
