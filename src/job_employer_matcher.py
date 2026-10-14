

import re
from urllib.parse import urlparse


class JobEmployerMatcherTool:

    # Explicitly verified employer recruitment sites.
    # Extend this mapping only after verification.
    TRUSTED_HOSTS = {
        "g research": {
            "www.gresearch.com",
            "gresearch.com",
        },
        "datacamp": {
            "job-boards.greenhouse.io",
        },
    }

    TRUSTED_PATH_PREFIXES = {
        "datacamp": {
            "job-boards.greenhouse.io": "/datacamp/jobs/",
        },
    }

    @staticmethod
    def normalise(name: str) -> str:
        name = name.lower()
        name = re.sub(r"[^\w\s]", " ", name)
        return " ".join(name.split())

    def is_match(
        self,
        expected_employer: str,
        extracted_employer: str | None,
        url: str,
    ) -> bool:

        expected = self.normalise(expected_employer)

        # Prefer employer identity from structured data.
        if extracted_employer:
            actual = self.normalise(extracted_employer)
            return expected == actual

        # Only use explicit, previously verified URL patterns.
        parsed = urlparse(url)

        if parsed.scheme != "https":
            return False

        hostname = (parsed.hostname or "").lower()

        allowed_hosts = self.TRUSTED_HOSTS.get(
            expected, set()
        )

        if hostname not in allowed_hosts:
            return False

        required_prefix = self.TRUSTED_PATH_PREFIXES.get(
            expected, {}
        ).get(hostname)

        if required_prefix:
            return parsed.path.startswith(required_prefix)

        return True
