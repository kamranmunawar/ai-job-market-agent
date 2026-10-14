from collections import Counter

from job_repository import JobRepository


class SkillAnalyzer:

    def __init__(self):
        self.repository = JobRepository()

    def analyze(self, full_only: bool = False):
        jobs = self.repository.get_completed_skills()

        # Exclude synthetic test records
        jobs = [
            job for job in jobs
            if not job["job_id"].startswith("test_")
        ]

        # Optionally exclude partial descriptions
        if full_only:
            jobs = [
                job for job in jobs
                if job["description_source"] == "full"
            ]

        skill_counts = Counter()

        for job in jobs:
            unique_skills = set()

            for category_skills in job["skills"].values():
                unique_skills.update(category_skills)

            skill_counts.update(unique_skills)

        return {
            "total_jobs": len(jobs),
            "skill_counts": skill_counts,
        }