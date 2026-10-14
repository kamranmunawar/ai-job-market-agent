
import html
import re


class JobTitleMatcherTool:

    @staticmethod
    def normalise(title: str) -> str:
        # 1. Decode HTML entities, including double encoding.
        for _ in range(3):
            decoded = html.unescape(title)

            if decoded == title:
                break

            title = decoded

        # 2. Normalise Unicode dashes after decoding.
        title = title.replace("–", "-").replace("—", "-")

        # 3. Convert to lowercase.
        title = title.lower()

        # 4. Replace punctuation with spaces.
        title = re.sub(r"[^\w\s]", " ", title)

        # 5. Remove repeated whitespace.
        return " ".join(title.split())

    def is_match(
        self,
        adzuna_title: str,
        employer_title: str
    ) -> bool:
        if not adzuna_title or not employer_title:
            return False

        return (
            self.normalise(adzuna_title)
            == self.normalise(employer_title)
        )
