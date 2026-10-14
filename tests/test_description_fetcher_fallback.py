
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import requests

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_description_fetcher import JobDescriptionFetcherTool


def test_html_fallback():
    fetcher = JobDescriptionFetcherTool()

    html = """
    <html>
        <body>
            <section class="adp-body">
                <h2>Requirements</h2>
                <p>We need an experienced AI Engineer with
                Python, PyTorch, Azure, Docker and Kubernetes
                experience to build and deploy machine learning
                systems in production.</p>
            </section>
        </body>
    </html>
    """

    response = Mock()
    response.text = html
    response.raise_for_status.return_value = None

    with patch(
        "job_description_fetcher.requests.get",
        return_value=response
    ):
        description, source = fetcher.fetch(
            "https://example.com/job"
        )

    assert source == "full"
    assert "Python" in description
    assert "Kubernetes" in description

    print("PASS: HTML fallback extraction")


def test_http_403_with_fallback():
    fetcher = JobDescriptionFetcherTool()

    response = Mock()
    response.status_code = 403

    error = requests.HTTPError(
        "403 Client Error: Forbidden",
        response=response
    )

    with patch(
        "job_description_fetcher.requests.get",
        return_value=response
    ):
        response.raise_for_status.side_effect = error

        description, source = fetcher.fetch(
            "https://example.com/blocked-job",
            fallback_description="Python and Azure required"
        )

    assert description == "Python and Azure required"
    assert source == "partial"

    print("PASS: HTTP 403 uses partial fallback")


def test_http_403_without_fallback():
    fetcher = JobDescriptionFetcherTool()

    response = Mock()
    response.status_code = 403

    error = requests.HTTPError(
        "403 Client Error: Forbidden",
        response=response
    )

    with patch(
        "job_description_fetcher.requests.get",
        return_value=response
    ):
        response.raise_for_status.side_effect = error

        try:
            fetcher.fetch(
                "https://example.com/blocked-job"
            )
        except requests.HTTPError:
            print("PASS: HTTP 403 raises without fallback")
        else:
            raise AssertionError(
                "Expected HTTPError without fallback"
            )


if __name__ == "__main__":
    test_html_fallback()
    test_http_403_with_fallback()
    test_http_403_without_fallback()

    print("\nALL FALLBACK TESTS PASSED")
