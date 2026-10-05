from job_search import SearchJobsTool
from job_description_fetcher import JobDescriptionFetcherTool
from skill_extractor import SkillExtractorTool


def main():

    search_tool = SearchJobsTool()
    description_tool = JobDescriptionFetcherTool()
    skill_tool = SkillExtractorTool()

    # 1. Discover one job
    jobs = search_tool.search(
        query="AI Engineer",
        results_per_page=1,
    )

    job = jobs[0]

    print("\nJOB")
    print("=" * 70)
    print(f"Title:    {job.title}")
    print(f"Company:  {job.company}")
    print(f"Location: {job.location}")

    # 2. Fetch full job page
    print("\nFetching full job description...")

    full_description = description_tool.fetch(
        job.url
    )

    print(
        f"Full description length: "
        f"{len(full_description)} characters"
    )

    # 3. Extract skills using the LLM
    print("\nExtracting skills with Qwen3.5...")

    skills = skill_tool.extract(
        full_description
    )

    job.skills = skills

    # 4. Display structured result
    print("\nSKILLS")
    print("=" * 70)

    print(
        job.skills.model_dump_json(
            indent=2
        )
    )


if __name__ == "__main__":
    main()