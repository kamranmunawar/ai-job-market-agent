
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from report_skill_normalizer import ReportSkillNormalizer


def normalize_job_skills(skills_data):
    job_skills = set()

    for category_skills in skills_data.values():
        if not isinstance(category_skills, list):
            continue

        for raw_skill in category_skills:
            if not isinstance(raw_skill, str):
                continue

            normalized = ReportSkillNormalizer.normalize(
                raw_skill
            )

            if normalized:
                job_skills.add(normalized)

    return job_skills


def main():
    skills_data = {
        "ai_ml": [
            "LLMs",
            "Large Language Models",
            "RAG",
        ],
        "agentic_ai": [
            "agents",
            "Agentic AI",
        ],
        "programming_languages": [
            "Python",
        ],
    }

    actual = normalize_job_skills(skills_data)

    expected = {
        "Large Language Models",
        "Retrieval-Augmented Generation",
        "Agentic AI",
        "Python",
    }

    assert actual == expected, (
        f"Expected {expected}, got {actual}"
    )

    print("PASS: Synonyms normalised")
    print("PASS: Duplicate skills removed")
    print("PASS: Distinct skills preserved")
    print(f"Unique skills: {len(actual)}")


if __name__ == "__main__":
    main()
