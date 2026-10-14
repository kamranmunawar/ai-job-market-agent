
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from report_skill_normalizer import ReportSkillNormalizer


def main():
    cases = {
        "LLMs": "Large Language Models",
        "LLMs (Large Language Models)": "Large Language Models",
        "RAG": "Retrieval-Augmented Generation",
        "RAG architectures": "Retrieval-Augmented Generation",
        "agents": "Agentic AI",
        "autonomous agent workflows": "Agentic Workflows",
        "Google Cloud": "Google Cloud Platform",
        "Microsoft Azure": "Azure",
        "sklearn": "scikit-learn",
    }

    for raw, expected in cases.items():
        actual = ReportSkillNormalizer.normalize(raw)

        assert actual == expected, (
            f"{raw!r}: expected {expected!r}, got {actual!r}"
        )

        print(f"PASS: {raw} -> {actual}")

    print("\nAll report normalisation tests passed.")


if __name__ == "__main__":
    main()
