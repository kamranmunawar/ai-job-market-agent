import json
from datetime import datetime
from pathlib import Path

from models import Job


class JobStorage:

    def __init__(self):
        self.data_dir = Path(__file__).resolve().parents[1] / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save(self, jobs: list[Job]) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        output_file = self.data_dir / f"jobs_{timestamp}.json"

        data = [job.model_dump(mode="json") for job in jobs]

        output_file.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        return output_file

    def load(self, file_path: str | Path) -> list[Job]:
        file_path = Path(file_path)

        data = json.loads(
            file_path.read_text(encoding="utf-8")
        )

        return [Job.model_validate(item) for item in data]