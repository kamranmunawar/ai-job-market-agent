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
            timeout=30,
        )

        response.raise_for_status()

        print(f"Final URL: {response.url}")
        print(f"Status: {response.status_code}")

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        text = soup.get_text(
            separator="\n",
            strip=True,
        )

        return text