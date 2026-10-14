
import json

from bs4 import BeautifulSoup


class JobLocationExtractorTool:

    @staticmethod
    def extract(soup: BeautifulSoup) -> list[str]:

        def find_locations(data):
            if isinstance(data, list):
                for item in data:
                    result = find_locations(item)
                    if result:
                        return result

            elif isinstance(data, dict):
                types = data.get("@type", [])

                if isinstance(types, str):
                    types = [types]

                if "JobPosting" in types:
                    locations = data.get("jobLocation", [])

                    if isinstance(locations, dict):
                        locations = [locations]

                    results = []

                    for location in locations:
                        if not isinstance(location, dict):
                            continue

                        address = location.get("address", {})

                        if not isinstance(address, dict):
                            continue

                        parts = [
                            address.get("addressLocality"),
                            address.get("addressRegion"),
                            address.get("addressCountry"),
                        ]

                        text = ", ".join(
                            str(part).strip()
                            for part in parts
                            if part
                        )

                        if text:
                            results.append(text)

                    return results

                for value in data.values():
                    if isinstance(value, (dict, list)):
                        result = find_locations(value)
                        if result:
                            return result

            return []

        for script in soup.select(
            'script[type="application/ld+json"]'
        ):
            try:
                data = json.loads(
                    script.string or script.get_text()
                )
            except (json.JSONDecodeError, TypeError):
                continue

            locations = find_locations(data)

            if locations:
                return locations

        return []
