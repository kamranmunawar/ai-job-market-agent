
import json
import re

from bs4 import BeautifulSoup


class JobTitleExtractorTool:

    @staticmethod
    def extract(soup: BeautifulSoup) -> str | None:
        """
        Extract the advertised vacancy title.

        Priority:
        1. JSON-LD JobPosting title
        2. HTML h1 heading
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
                    title = data.get("title")

                    if isinstance(title, str) and title.strip():
                        return title.strip()

                for value in data.values():
                    if isinstance(value, (dict, list)):
                        result = find_job_posting(value)
                        if result:
                            return result

            return None

        for script in soup.select(
            'script[type="application/ld+json"]'
        ):
            try:
                data = json.loads(
                    script.string or script.get_text()
                )
            except (json.JSONDecodeError, TypeError):
                continue

            title = find_job_posting(data)

            if title:
                return re.sub(r"\s+", " ", title).strip()

        heading = soup.select_one("h1")

        if heading:
            title = heading.get_text(" ", strip=True)

            if title:
                return re.sub(r"\s+", " ", title).strip()

        return None
