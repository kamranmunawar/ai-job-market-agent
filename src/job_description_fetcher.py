import requests
from bs4 import BeautifulSoup


class JobDescriptionFetcherTool:

    def fetch(self, url: str) -> str:

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
            str(url),
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Locate the actual job description
        description_element = soup.select_one(
            "section.adp-body"
        )

        if description_element is None:
            raise ValueError(
                "Job description section not found"
            )

        # Remove irrelevant elements within the description
        for element in description_element.select(
            "script, style, noscript"
        ):
            element.decompose()

        description = description_element.get_text(
            separator="\n",
            strip=True
        )

        if len(description) < 100:
            raise ValueError(
                "Job description is unexpectedly short"
            )

        return description