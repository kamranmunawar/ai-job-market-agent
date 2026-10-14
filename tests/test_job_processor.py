import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_search import SearchJobsTool
from job_processor import JobProcessor


def main():
    search_tool = SearchJobsTool()
    processor = JobProcessor()

    jobs = search_tool.search(
        query="AI Engineer",
        results_per_page=1
    )

    if not jobs:
        print("No jobs found")
        return

    job = processor.process(jobs[0])

    print("\nPROCESSING RESULT")
    print("=" * 70)
    print(f"Title: {job.title}")
    print(f"Company: {job.company}")
    print(f"Description source: {job.description_source}")
    print(f"Processing status: {job.processing_status}")

    if job.skills:
        print("\nNORMALISED SKILLS")
        print(job.skills.model_dump_json(indent=2))


if __name__ == "__main__":
    main()