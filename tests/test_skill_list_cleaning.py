
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from skill_normalizer import SkillNormalizerTool


def main():
    input_skills = [
        "Python",
        "",
        "python",
        "  PyTorch  ",
        " ",
        "AWS",
        "aws"
    ]

    expected = [
        "Python",
        "PyTorch",
        "AWS"
    ]

    actual = SkillNormalizerTool.clean_skill_list(
        input_skills
    )

    assert actual == expected, (
        f"Expected {expected}, got {actual}"
    )

    print("PASS: Empty skills removed")
    print("PASS: Whitespace trimmed")
    print("PASS: Duplicate skills removed")
    print(f"Cleaned skills: {actual}")


if __name__ == "__main__":
    main()
