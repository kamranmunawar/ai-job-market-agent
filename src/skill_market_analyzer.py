
import json
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from report_skill_normalizer import ReportSkillNormalizer

class SkillMarketAnalyzer:

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)

    def analyze(self):
        overall = Counter()
        by_category = defaultdict(Counter)

        completed_jobs = 0
        category_job_counts = Counter()

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            rows = conn.execute(
                """
                SELECT
                    job_id,
                    skills_json,
                    search_categories_json
                FROM jobs
                WHERE processing_status = 'completed'
                """
            ).fetchall()

        for row in rows:
            if not row["skills_json"]:
                continue

            try:
                skills_data = json.loads(row["skills_json"])
                categories = json.loads(
                    row["search_categories_json"] or "[]"
                )
            except (json.JSONDecodeError, TypeError):
                continue

            if not isinstance(skills_data, dict):
                continue

            if not isinstance(categories, list):
                categories = []

            # Count each skill only once per vacancy.
            job_skills = set()

            for values in skills_data.values():
                if not isinstance(values, list):
                    continue

                for skill in values:
                    if not isinstance(skill, str) or not skill.strip():
                        continue

                    normalized_skill = ReportSkillNormalizer.normalize(skill)

                    if normalized_skill:
                        job_skills.add(normalized_skill)

            completed_jobs += 1
            overall.update(job_skills)

            # One vacancy can belong to several search categories.
            for category in set(categories):
                if not isinstance(category, str):
                    continue

                category = category.strip()
                if not category:
                    continue

                category_job_counts[category] += 1
                by_category[category].update(job_skills)

        return {
            "completed_jobs": completed_jobs,
            "overall": overall,
            "by_category": dict(by_category),
            "category_job_counts": category_job_counts,
        }

    def print_report(self, top_n: int = 15):
        result = self.analyze()

        print("\nAI JOB MARKET ANALYSIS")
        print("=" * 50)

        print(
            f"Completed jobs analysed: "
            f"{result['completed_jobs']}"
        )

        print("\nTOP SKILLS OVERALL")
        print("-" * 50)

        for skill, count in result["overall"].most_common(top_n):
            print(f"{skill:<30} {count:>4} jobs")

        print("\nSKILLS BY JOB CATEGORY")
        print("=" * 50)

        for category in sorted(result["by_category"]):
            job_count = result["category_job_counts"][category]

            print(f"\n{category} ({job_count} jobs)")
            print("-" * 50)

            for skill, count in (
                result["by_category"][category].most_common(top_n)
            ):
                print(f"  {skill:<28} {count:>4} jobs")
