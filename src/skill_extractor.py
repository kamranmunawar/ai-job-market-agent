import json

import requests

from models import Skills
import re

import re


def clean_json_response(content: str) -> str:
    content = content.strip()

    # Remove Markdown code fences surrounding JSON
    match = re.fullmatch(
        r"```(?:json)?\s*\n?(.*?)\s*```",
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    if match:
        content = match.group(1).strip()

    return content


class SkillExtractorTool:

    OLLAMA_URL = "http://localhost:11434/api/chat"

    def __init__(self, model: str = "Qwen3.5:latest"):
        self.model = model

    import re



    def extract(self, job_description: str) -> Skills:
        prompt = f"""
    You are analysing an AI job advertisement.

    Extract ONLY skills explicitly mentioned in the text.

    Return a JSON object with these eight categories:
    - programming_languages
    - ai_ml
    - agentic_ai
    - frameworks
    - cloud
    - devops
    - databases
    - other

    Each category must contain a list of strings.
    Use empty lists when no skills are found.
    Do not return a top-level JSON array.
    Do not invent skills.

    Job description:
    {job_description}
    """

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "format": Skills.model_json_schema(),
            "think": False,
            "stream": False,
        }

        max_attempts = 3

        for attempt in range(1, max_attempts + 1):
            print(f"Skill extraction attempt {attempt}/{max_attempts}")

            try:
                response = requests.post(
                    self.OLLAMA_URL,
                    json=payload,
                    timeout=300
                )
                response.raise_for_status()

                result = response.json()
                content = result["message"]["content"]
                print(f"Ollama done reason: {result.get('done_reason')}")
                print(f"Response length: {len(content)} characters")
                print(f"Response preview: {repr(content[:500])}")
                print(f"Ollama done reason: {result.get('done_reason')}")
                print(f"Response length: {len(content)} characters")

                if not content.strip():
                    print("WARNING: Ollama returned empty content")
                    print(f"Prompt tokens: {result.get('prompt_eval_count')}")
                    print(f"Generated tokens: {result.get('eval_count')}")
                    print(
                        "Thinking length:",
                        len(result.get("message", {}).get("thinking", ""))
                    )
                if not content.strip():
                    raise ValueError(
                        "Ollama returned empty content instead of JSON"
                    )

                #data = json.loads(content)
                cleaned_content = clean_json_response(content)

                if not cleaned_content:
                    raise ValueError("Ollama returned empty content")

                data = json.loads(cleaned_content)

                if not isinstance(data, dict):
                    raise ValueError(
                        f"Expected JSON object, got {type(data).__name__}"
                    )

                skills = Skills.model_validate(data)

                if not isinstance(data, dict):
                    raise ValueError(
                        f"Expected JSON object, got {type(data).__name__}"
                    )

                skills = Skills.model_validate(data)

                return skills

            except (
                    requests.RequestException,
                    ValueError,
                    KeyError,
                    TypeError
            ) as error:
                print(f"Attempt {attempt} failed: {error}")

                if attempt == max_attempts:
                    raise RuntimeError(
                        f"Skill extraction failed after {max_attempts} attempts"
                    ) from error

                # Tell the model what went wrong.
                payload["messages"] = [
                    {"role": "user", "content": prompt},
                    {
                        "role": "assistant",
                        "content": content
                    } if "content" in locals() else {
                        "role": "assistant",
                        "content": ""
                    },
                    {
                        "role": "user",
                        "content": (
                            "Your previous response was invalid. "
                            "Return a JSON OBJECT matching the supplied "
                            "schema, not a JSON array. "
                            "All eight categories must be present."
                        )
                    }
                ]


