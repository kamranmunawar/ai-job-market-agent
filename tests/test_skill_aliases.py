
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from models import Skills
from skill_normalizer import SkillNormalizerTool


def main():
    normalizer = SkillNormalizerTool()

    raw_skills = Skills(
        ai_ml=[
            "LLM",
            "LLMs",
            "large language models",
            "ML",
            "machine_learning",
            "GenAI",
            "RAG"
        ],
        devops=[
            "MLOps",
            "ML Ops",
            "ml_ops"
        ]
    )

    result = normalizer.normalize(raw_skills)

    expected_ai_ml = [
        "Large Language Models",
        "Machine Learning",
        "Generative AI",
        "Retrieval-Augmented Generation"
    ]

    expected_devops = ["MLOps"]

    assert result.ai_ml == expected_ai_ml, (
        f"Expected {expected_ai_ml}, got {result.ai_ml}"
    )

    assert result.devops == expected_devops, (
        f"Expected {expected_devops}, got {result.devops}"
    )

    print("PASS: LLM aliases normalised")
    print("PASS: Machine Learning aliases normalised")
    print("PASS: Generative AI and RAG normalised")
    print("PASS: MLOps aliases normalised")

    print("\nNormalised AI/ML skills:", result.ai_ml)
    print("Normalised DevOps skills:", result.devops)


if __name__ == "__main__":
    main()
