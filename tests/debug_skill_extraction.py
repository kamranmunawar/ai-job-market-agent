
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_repository import JobRepository
from skill_extractor import SkillExtractorTool


def main():
    repository = JobRepository()
    extractor = SkillExtractorTool()

    job_id = "5761412988"  # Ultralytics

    description = repository.get_description(job_id)

    if not description:
        print("Job description not found.")
        return

    print(f"Job ID: {job_id}")
    print(f"Description length: {len(description)}")

    try:
        skills = extractor.extract(description)

        print("\nEXTRACTED SKILLS")
        print(skills.model_dump_json(indent=2))

    except Exception as error:
        print(f"\nExtraction failed: {error}")


if __name__ == "__main__":
    main()

