
import re


class ReportSkillNormalizer:
    """Canonical skill names for market analysis."""

    ALIASES = {
        "llm": "Large Language Models",
        "llms": "Large Language Models",
        "large language model": "Large Language Models",
        "large language models": "Large Language Models",
        "llms (large language models)": "Large Language Models",

        "gen ai": "Generative AI",
        "genai": "Generative AI",
        "generative ai": "Generative AI",

        "rag": "Retrieval-Augmented Generation",
        "retrieval augmented generation":
            "Retrieval-Augmented Generation",
        "retrieval-augmented generation":
            "Retrieval-Augmented Generation",
        "rag architectures":
            "Retrieval-Augmented Generation",

        "agentic ai": "Agentic AI",
        "ai agents": "Agentic AI",
        "autonomous ai agents": "Agentic AI",
        "agents": "Agentic AI",

        "agentic workflows": "Agentic Workflows",
        "autonomous agent workflows": "Agentic Workflows",
        "multi-agent workflows": "Multi-Agent Systems",
        "multi-agent architectures": "Multi-Agent Systems",

        "pytorch": "PyTorch",
        "tensorflow": "TensorFlow",
        "scikit learn": "scikit-learn",
        "sklearn": "scikit-learn",
        "scikit-learn": "scikit-learn",

        "aws": "AWS",
        "amazon web services": "AWS",
        "gcp": "Google Cloud Platform",
        "google cloud": "Google Cloud Platform",
        "google cloud platform": "Google Cloud Platform",
        "microsoft azure": "Azure",
        "azure": "Azure",

        "ci cd": "CI/CD",
        "ci/cd": "CI/CD",
        "continuous integration/continuous delivery": "CI/CD",

        "machine learning": "Machine Learning",
        "ml": "Machine Learning",
        "python": "Python",
        "sql": "SQL",
    }

    @classmethod
    def normalize(cls, skill: str) -> str:
        cleaned = " ".join(skill.strip().split())

        key = cleaned.casefold()
        key = re.sub(r"\s+", " ", key)

        return cls.ALIASES.get(key, cleaned)
