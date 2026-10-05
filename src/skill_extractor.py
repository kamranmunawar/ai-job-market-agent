import json

import requests

from models import Skills


class SkillExtractorTool:

    OLLAMA_URL = "http://localhost:11434/api/chat"

    def __init__(self, model: str = "Qwen3.5:latest"):
        self.model = model

    def extract(self, job_description: str) -> Skills:

        prompt = f"""
You are analysing an AI job advertisement.

Extract ONLY skills and technologies explicitly required
or mentioned in the job description.

Categorise them into:

- programming_languages
- ai_ml
- agentic_ai
- frameworks
- cloud
- devops
- databases
- other

Do not invent skills.

Job description:

{job_description}

Return valid JSON only.
"""

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "format": Skills.model_json_schema(),
            "think": False,
            "stream": False,
        }

        response = requests.post(
            self.OLLAMA_URL,
            json=payload,
            timeout=600,
        )

        response.raise_for_status()

        result = response.json()



        content = result["message"]["content"]

        content = result["message"]["content"]



        data = json.loads(content)

        return Skills.model_validate(data)