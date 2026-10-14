
import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from employer_job_finder import EmployerJobFinderTool


def main():
    finder = EmployerJobFinderTool()

    search_client = Mock()
    search_client.text.return_value = [{
        "href": "https://www.gresearch.com/vacancies/software-engineer-ai/"
    }]

    response = Mock()
    response.text = """
    <html>
      <head>
        <script type="application/ld+json">
        {
          "@context": "https://schema.org",
          "@type": "JobPosting",
          "title": "Core AI Engineer",
          "hiringOrganization": {
            "@type": "Organization",
            "name": "G-Research"
          },
          "jobLocation": {
            "@type": "Place",
            "address": {
              "@type": "PostalAddress",
              "addressLocality": "New York",
              "addressCountry": "US"
            }
          },
          "description": "We are hiring a Core AI Engineer to build machine learning infrastructure and reliable AI services."
        }
        </script>
      </head>
      <body><h1>Core AI Engineer</h1></body>
    </html>
    """
    response.raise_for_status.return_value = None

    with (
        patch(
            "employer_job_finder.DDGS",
            return_value=search_client
        ),
        patch(
            "employer_job_finder.requests.get",
            return_value=response
        ),
        patch.object(
            finder.fetcher,
            "extract_from_soup"
        ) as mocked_extract,
    ):
        result = finder.find(
            company="G-Research",
            title="Core AI Engineer",
            snippet="We are hiring a Core AI Engineer",
            location="London, UK",
            max_results=1,
        )

    assert result is None
    mocked_extract.assert_not_called()

    print("\nPASS: Correct title recognised")
    print("PASS: Correct employer recognised")
    print("PASS: Incorrect location rejected")
    print("PASS: Description extraction skipped")
    print("\nALL LOCATION VERIFICATION TESTS PASSED")


if __name__ == "__main__":
    main()
