import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from models import Skills
from skill_normalizer import SkillNormalizerTool


def main():

    sample_skills = Skills(
        programming_languages=["Python", "python"],
        ai_ml=[
            "LLM",
            "LLMs",
            "Large Language Models",
            "GenAI",
            "Generative AI",
            "RAG",
            "RAG pipelines",
        ],
        frameworks=[
            "PyTorch",
            "pytorch",
            "LangChain",
        ],
        cloud=[
            "AWS",
            "Amazon Web Services",
            "GCP",
        ],
    )

    normalizer = SkillNormalizerTool()

    result = normalizer.normalize(sample_skills)

    print("\nORIGINAL SKILLS")
    print("=" * 70)
    print(sample_skills.model_dump_json(indent=2))

    print("\nNORMALISED SKILLS")
    print("=" * 70)
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()