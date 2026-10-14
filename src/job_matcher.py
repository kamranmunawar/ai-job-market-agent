
import re
from difflib import SequenceMatcher


class JobMatcherTool:

    @staticmethod
    def normalise(text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        return " ".join(text.split())

    def calculate_match(
        self,
        snippet: str,
        full_description: str
    ) -> float:

        snippet = self.normalise(snippet)
        full_description = self.normalise(full_description)

        if not snippet or not full_description:
            return 0.0

        # Compare a meaningful portion of the snippet.
        # Avoid the final truncated word.
        snippet_words = snippet.split()[:60]

        if len(snippet_words) < 10:
            return 0.0

        snippet_text = " ".join(snippet_words)

        # Look for the best matching passage in the
        # full description, preserving word order.
        full_words = full_description.split()
        window_size = len(snippet_words)

        best_score = 0.0

        for start in range(len(full_words)):
            window = full_words[start:start + window_size]

            if len(window) < window_size:
                break

            candidate = " ".join(window)

            score = SequenceMatcher(
                None,
                snippet_text,
                candidate,
                autojunk=False
            ).ratio()

            best_score = max(best_score, score)

            if best_score >= 0.99:
                break

        return best_score

    def is_match(
        self,
        snippet: str,
        full_description: str,
        threshold: float = 0.90
    ) -> bool:

        score = self.calculate_match(
            snippet,
            full_description
        )

        return score >= threshold
