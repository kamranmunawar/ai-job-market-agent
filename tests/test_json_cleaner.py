import sys
import json
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from skill_extractor import clean_json_response


def main():
    cases = [
        (
            "Plain JSON",
            '{"programming_languages": ["Python"]}'
        ),
        (
            "Markdown fenced JSON",
            '```json\n{"programming_languages": ["Python"]}\n```'
        ),
        (
            "JSON with whitespace",
            '  \n{"programming_languages": ["Python"]}\n  '
        ),
    ]

    for name, content in cases:
        cleaned = clean_json_response(content)
        result = json.loads(cleaned)

        assert result["programming_languages"] == ["Python"]
        print(f"PASS: {name}")

    malformed = '```json\n{"skills": ["Python", "RAG]}\n```'

    try:
        json.loads(clean_json_response(malformed))
    except json.JSONDecodeError:
        print("PASS: Malformed JSON correctly rejected")
    else:
        raise AssertionError("Malformed JSON was incorrectly accepted")


if __name__ == "__main__":
    main()