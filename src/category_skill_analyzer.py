
from collections import Counter, defaultdict

from job_repository import JobRepository


class CategorySkillAnalyzer:

    def __init__(self):
        self.repository = JobRepository()

    def analyze(self, full_only: bool = False):
        jobs = self.repository.get_completed_skills()

        category_jobs = defaultdict(set)
        category_skills = defaultdict(Counter)

        for job in jobs:
            # Exclude synthetic test records
            if job["job_id"].startswith("test_"):
                continue

            # Optionally exclude partial descriptions
            if full_only and job["description_source"] != "full":
                continue

            # Count each skill once per job
            unique_skills = set()

            for skills in job["skills"].values():
                unique_skills.update(skills)

            for category in job["search_categories"]:
                category_jobs[category].add(job["job_id"])
                category_skills[category].update(unique_skills)

        return {
            category: {
                "total_jobs": len(job_ids),
                "skill_counts": category_skills[category]
            }
            for category, job_ids in category_jobs.items()
        }
