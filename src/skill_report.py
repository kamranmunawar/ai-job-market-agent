
from pathlib import Path

from skill_market_analyzer import SkillMarketAnalyzer
from skill_report_exporter import SkillReportExporter


def main():
    project_root = Path(__file__).resolve().parents[1]

    database_path = project_root / "data" / "jobs.db"
    output_dir = project_root / "reports"

    if not database_path.exists():
        print(f"Database not found: {database_path}")
        return

    analyzer = SkillMarketAnalyzer(database_path)

    # Display the existing report.
    analyzer.print_report(top_n=15)

    # Export the same analysis to CSV.
    analysis = analyzer.analyze()

    exporter = SkillReportExporter(output_dir)
    overall_path, category_path = exporter.export(analysis)

    print("\nCSV REPORTS GENERATED")
    print("=" * 50)
    print(f"Overall skills: {overall_path}")
    print(f"Category skills: {category_path}")


if __name__ == "__main__":
    main()
