
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
        programming_languages=[
            "Python",
            "python",
            "",
            "  C#  "
        ],
        frameworks=[
            "PyTorch",
            "pytorch",
            " "
        ]
    )

    result = normalizer.normalize(raw_skills)

    assert result.programming_languages == [
        "Python",
        "C#"
    ], result.programming_languages

    assert result.frameworks == [
        "PyTorch"
    ], result.frameworks

    print("PASS: Full normalizer removes empty skills")
    print("PASS: Full normalizer removes duplicates")
    print("PASS: Full normalizer trims whitespace")
    print("Normalized programming languages:",
          result.programming_languages)
    print("Normalized frameworks:",
          result.frameworks)


if __name__ == "__main__":
    main()
