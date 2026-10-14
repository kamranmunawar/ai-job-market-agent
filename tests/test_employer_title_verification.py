
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

    # Search returns a Core AI Engineer page.
    search_result = [{
        "title": "Core AI Engineer",
        "href": "https://example.com/core-ai-engineer",
        "body": "AI engineering vacancy",
    }]

    search_client = Mock()
    search_client.text.return_value = search_result

    response = Mock()
    response.text = """
    <html>
      <body>
        <h1>Core AI Engineer</h1>
      </body>
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
            "fetch"
        ) as mocked_fetch,
    ):
        match = finder.find(
            company="G-Research",
            title="Applied AI Engineer",
            snippet="Shared company introduction",
            max_results=1
        )

    assert match is None
    mocked_fetch.assert_not_called()

    print("PASS: Incorrect vacancy title rejected")
    print("PASS: Description fetch skipped")
    print("\nALL TITLE VERIFICATION TESTS PASSED")


if __name__ == "__main__":
    main()
