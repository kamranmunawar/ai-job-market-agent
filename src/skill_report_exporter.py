
import csv
from pathlib import Path


class SkillReportExporter:

    def __init__(self, output_dir: str | Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def export(self, analysis: dict):
        overall_path = self.output_dir / "skills_overall.csv"
        category_path = self.output_dir / "skills_by_category.csv"

        total_jobs = analysis["completed_jobs"]

        with overall_path.open(
            "w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)

            writer.writerow([
                "skill",
                "job_count",
                "total_jobs",
                "percentage",
            ])

            for skill, count in analysis["overall"].most_common():
                percentage = (
                    round(count / total_jobs * 100, 2)
                    if total_jobs else 0
                )

                writer.writerow([
                    skill,
                    count,
                    total_jobs,
                    percentage,
                ])

        with category_path.open(
            "w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)

            writer.writerow([
                "category",
                "skill",
                "job_count",
                "category_jobs",
                "percentage",
            ])

            for category in sorted(analysis["by_category"]):
                category_jobs = (
                    analysis["category_job_counts"][category]
                )

                for skill, count in (
                    analysis["by_category"][category].most_common()
                ):
                    percentage = (
                        round(count / category_jobs * 100, 2)
                        if category_jobs else 0
                    )

                    writer.writerow([
                        category,
                        skill,
                        count,
                        category_jobs,
                        percentage,
                    ])

        return overall_path, category_path
