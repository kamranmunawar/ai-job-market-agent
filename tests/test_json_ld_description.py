
import sys
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_description_fetcher import JobDescriptionFetcherTool


def main():
    html = """
    <html>
    <head>
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "JobPosting",
        "title": "AI Engineer",
        "description": "<p>We require Python, PyTorch, machine learning and experience deploying production AI systems.</p><p>Experience with Azure, Docker and CI/CD pipelines is desirable.</p>"
    }
    </script>
    </head>
    <body></body>
    </html>
    """

    soup = BeautifulSoup(html, "html.parser")

    description = (
        JobDescriptionFetcherTool.extract_json_ld_description(soup)
    )

    assert description is not None
    assert "Python" in description
    assert "PyTorch" in description
    assert "Azure" in description
    assert "<p>" not in description

    print("PASS: JobPosting JSON-LD description extracted")
    print("PASS: HTML tags removed")
    print("\nExtracted description:")
    print(description)


if __name__ == "__main__":
    main()

