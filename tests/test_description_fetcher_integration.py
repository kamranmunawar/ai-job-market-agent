
import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_description_fetcher import JobDescriptionFetcherTool


def main():
    fetcher = JobDescriptionFetcherTool()

    html = """
    <html>
    <head>
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "JobPosting",
        "title": "Machine Learning Engineer",
        "description": "<p>We require Python, PyTorch, scikit-learn and machine learning experience.</p><p>Knowledge of Azure, Docker, Kubernetes and CI/CD is desirable for production deployment.</p>"
    }
    </script>
    </head>
    <body></body>
    </html>
    """

    response = Mock()
    response.text = html
    response.raise_for_status.return_value = None

    with patch(
        "job_description_fetcher.requests.get",
        return_value=response
    ) as mocked_get:

        description, source = fetcher.fetch(
            url="https://example.com/jobs/123",
            fallback_description="Short Adzuna snippet"
        )

        mocked_get.assert_called_once()

    assert source == "full"
    assert "Python" in description
    assert "PyTorch" in description
    assert "Kubernetes" in description
    assert "<p>" not in description

    print("PASS: Fetcher extracted JSON-LD description")
    print("PASS: Description marked as full")
    print("PASS: HTML removed")
    print("PASS: HTTP request mocked successfully")

    print("\nExtracted description:")
    print(description)


if __name__ == "__main__":
    main()
