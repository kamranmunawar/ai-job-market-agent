
from ddgs import DDGS
from ddgs.exceptions import DDGSException


def search_employer_job(company: str, title: str):
    queries = [
        f'"{company}" "{title}"',
        f'{company} {title} jobs',
        f'{company} {title} careers',
    ]

    print(f"\n{'=' * 70}")
    print(f"Searching for: {company} — {title}")
    print("=" * 70)

    for query in queries:
        print(f"\nQuery: {query}")

        try:
            results = DDGS(timeout=15).text(
                query,
                max_results=5
            )

            valid_results = []

            for result in results or []:
                if not isinstance(result, dict):
                    continue

                url = result.get("href") or result.get("url")

                if not url:
                    continue

                valid_results.append(result)

            if not valid_results:
                print("No usable results")
                continue

            for index, result in enumerate(
                valid_results,
                start=1
            ):
                print(f"\nResult {index}")
                print("Title:", result.get("title"))
                print(
                    "URL:",
                    result.get("href") or result.get("url")
                )
                print("Description:", result.get("body"))

            # Stop after finding usable search results.
            return valid_results

        except DDGSException as error:
            print(f"Search unavailable: {error}")

        except Exception as error:
            print(f"Unexpected error: {error}")

    print("\nNo usable results found for this vacancy.")
    return []


if __name__ == "__main__":
    search_employer_job(
        company="G-Research",
        title="Core AI Engineer"
    )

    search_employer_job(
        company="DataCamp",
        title="Principal AI Engineer"
    )
