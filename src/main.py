from job_search import SearchJobsTool
from job_description_fetcher import JobDescriptionFetcherTool
from skill_extractor import SkillExtractorTool
from pathlib import Path
from datetime import datetime
from skill_normalizer import SkillNormalizerTool

def main():

    search_tool = SearchJobsTool()
    description_tool = JobDescriptionFetcherTool()
    skill_tool = SkillExtractorTool()
    normalizer_tool = SkillNormalizerTool()

    # 1. Discover one job
    jobs = search_tool.search(
        query="AI Engineer",
        results_per_page=1,
    )

    if not jobs:
        print("No jobs found.")
        return

    job = jobs[0]

    print("\nJOB")
    print("=" * 70)
    print(f"Title: {job.title}")
    print(f"Company: {job.company}")
    print(f"Location: {job.location}")

    # 2. Fetch job description
    print("\nFetching full job description...")

    try:
        description, source = description_tool.fetch(
            job.url,
            fallback_description=job.description
        )

        job.description = description
        job.description_source = source

        print(f"Description source: {job.description_source}")
        print(f"Description length: {len(job.description)}")

    except Exception as error:
        job.processing_status = "failed"
        print(f"Description retrieval failed: {error}")

        print("\nPROCESSED JOB")
        print(job.model_dump_json(indent=2))
        return

    # 3. Extract skills using Qwen3.5
    print("\nExtracting skills with Qwen3.5...")

    try:
        raw_skills = skill_tool.extract(job.description)

        print("\nRAW SKILLS")
        print(raw_skills.model_dump_json(indent=2))

        job.skills = normalizer_tool.normalize(raw_skills)
        job.processing_status = "completed"

        print("\nNORMALISED SKILLS")
        print(job.skills.model_dump_json(indent=2))

    except Exception as error:
        job.processing_status = "failed"
        print(f"Skill processing failed: {error}")

    # 4. Display extracted skills
    if job.skills is not None:
        print("\nSKILLS")
        print("=" * 70)
        print(job.skills.model_dump_json(indent=2))

    # 5. Display final structured job
    print("\nPROCESSED JOB")
    print("=" * 70)
    print(job.model_dump_json(indent=2))
    output_dir = Path(__file__).resolve().parents[1] / "data"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"job_{timestamp}.json"

    output_file.write_text(
        job.model_dump_json(indent=2),
        encoding="utf-8"
    )

    print(f"\nJob saved to: {output_file}")


if __name__ == "__main__":
    main()