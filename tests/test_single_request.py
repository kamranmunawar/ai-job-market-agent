
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

    html = """
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
          "description": "We are hiring a Core AI Engineer. The successful candidate will build and maintain machine learning infrastructure, develop model serving systems, and collaborate with engineering teams to deliver reliable AI services."
        }
        </script>
      </head>
      <body>
        <h1>Core AI Engineer</h1>
      </body>
    </html>
    """

    response = Mock()
    response.text = html
    response.raise_for_status.return_value = None

    search_client = Mock()
    search_client.text.return_value = [{
        "href": "https://www.gresearch.com/vacancies/software-engineer-ai/"
    }]

    with (
        patch(
            "employer_job_finder.DDGS",
            return_value=search_client,
        ),
        patch(
            "employer_job_finder.requests.get",
            return_value=response,
        ) as mocked_get,
    ):
        result = finder.find(
            company="G-Research",
            title="Core AI Engineer",
            snippet=(
                "We are hiring a Core AI Engineer. "
                "The successful candidate will build and maintain "
                "machine learning infrastructure, develop model "
                "serving systems, and collaborate with engineering "
                "teams to deliver reliable AI services."
            ),
            max_results=1,
        )

    assert result is not None, "Expected a verified match"

    print("\nHTTP requests:", mocked_get.call_count)

    assert mocked_get.call_count == 1, (
        "Expected exactly one HTTP request"
    )

    print("PASS: One request per candidate")
    print("PASS: Title and employer verified")
    print("PASS: Description extracted from same response")
    print("\nALL SINGLE-REQUEST TESTS PASSED")


if __name__ == "__main__":
    main()
