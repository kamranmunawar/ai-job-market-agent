
import json

from bs4 import BeautifulSoup


class JobEmployerExtractorTool:

    @staticmethod
    def extract(soup: BeautifulSoup) -> str | None:

        def find_employer(data):
            if isinstance(data, list):
                for item in data:
                    result = find_employer(item)
                    if result:
                        return result

            elif isinstance(data, dict):
                types = data.get("@type", [])

                if isinstance(types, str):
                    types = [types]

                if "JobPosting" in types:
                    organisation = data.get("hiringOrganization")

                    if isinstance(organisation, dict):
                        name = organisation.get("name")

                        if isinstance(name, str) and name.strip():
                            return name.strip()

                for value in data.values():
                    if isinstance(value, (dict, list)):
                        result = find_employer(value)
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

            employer = find_employer(data)

            if employer:
                return employer

        return None
