
import re


class JobLocationMatcherTool:

    COUNTRY_ALIASES = {
        "gb": "united kingdom",
        "uk": "united kingdom",
        "great britain": "united kingdom",
        "united kingdom": "united kingdom",
    }

    @classmethod
    def normalise(cls, location: str) -> list[str]:
        parts = []

        for part in location.split(","):
            part = re.sub(r"[^\w\s]", " ", part.lower())
            part = " ".join(part.split())

            if part:
                parts.append(
                    cls.COUNTRY_ALIASES.get(part, part)
                )

        return parts

    def is_match(
        self,
        adzuna_location: str,
        employer_locations: list[str],
    ) -> bool:

        if not adzuna_location or not employer_locations:
            return False

        expected = set(self.normalise(adzuna_location))

        for location in employer_locations:
            actual = set(self.normalise(location))

            shared = expected & actual

            # A country-only match is insufficient.
            shared.discard("united kingdom")

            if not shared:
                continue

            # Reject conflicting explicitly stated countries.
            known_countries = {"united kingdom", "united states"}

            expected_countries = expected & known_countries
            actual_countries = actual & known_countries

            if (
                expected_countries
                and actual_countries
                and expected_countries != actual_countries
            ):
                continue

            return True

        return False
