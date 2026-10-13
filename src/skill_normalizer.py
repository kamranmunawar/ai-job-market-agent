from models import Skills


class SkillNormalizerTool:

    SKILL_ALIASES = {
        "llm": "Large Language Models",
        "llms": "Large Language Models",
        "large language model": "Large Language Models",
        "large language models": "Large Language Models",

        "genai": "Generative AI",
        "gen ai": "Generative AI",
        "generative ai": "Generative AI",

        "rag": "Retrieval-Augmented Generation",
        "rag pipelines": "Retrieval-Augmented Generation",
        "retrieval augmented generation": "Retrieval-Augmented Generation",
        "retrieval-augmented generation": "Retrieval-Augmented Generation",

        "vector db": "Vector Databases",
        "vector database": "Vector Databases",
        "vector databases": "Vector Databases",
        "vector stores": "Vector Databases",

        "ml": "Machine Learning",
        "machine learning": "Machine Learning",

        "pytorch": "PyTorch",
        "langchain": "LangChain",
        "llamaindex": "LlamaIndex",

        "ci/cd": "CI/CD",
        "cicd": "CI/CD",

        "aws": "AWS",
        "amazon web services": "AWS",

        "gcp": "Google Cloud Platform",
        "google cloud platform": "Google Cloud Platform",
    }

    def normalize_skill(self, skill: str) -> str:
        cleaned = " ".join(skill.strip().split())
        lookup_key = cleaned.casefold()

        return self.SKILL_ALIASES.get(
            lookup_key,
            cleaned
        )

    def normalize(self, skills: Skills) -> Skills:

        normalized_data = {}

        for category, skill_list in skills.model_dump().items():

            normalized_skills = []
            seen = set()

            for skill in skill_list:
                normalized_skill = self.normalize_skill(skill)

                key = normalized_skill.casefold()

                if key not in seen:
                    seen.add(key)
                    normalized_skills.append(normalized_skill)

            normalized_data[category] = normalized_skills

        return Skills.model_validate(normalized_data)