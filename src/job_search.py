import os

import requests
from dotenv import load_dotenv

from models import Job
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()



class SearchJobsTool:

    BASE_URL = "https://api.adzuna.com/v1/api/jobs/gb/search"

    def __init__(self):
        self.app_id = os.getenv("ADZUNA_APP_ID")
        self.app_key = os.getenv("ADZUNA_APP_KEY")

        if not self.app_id or not self.app_key:
            raise ValueError(
                "ADZUNA_APP_ID and ADZUNA_APP_KEY must be set"
            )
        retry_strategy = Retry(
            total=3,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            respect_retry_after_header=True,
        )

        self.session = requests.Session()

        adapter = HTTPAdapter(max_retries=retry_strategy)

        self.session.mount("https://", adapter)

    def search(
            self,
            query: str,
            results_per_page: int = 20,
            page: int = 1,
    ) -> list[Job]:

        if page < 1:
            raise ValueError("Page number must be >= 1")

        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "what": query,
            "results_per_page": results_per_page,
            "content-type": "application/json",
        }

        url = f"{self.BASE_URL}/{page}"

        response = self.session.get(
            url,
            params=params,
            timeout=30
        )

        if not response.ok:
            raise RuntimeError(
                f"Adzuna API request failed with HTTP {response.status_code}"
            )

        data = response.json()

        print(f"Total jobs available: {data.get('count', 0)}")
        print(f"Page retrieved: {page}")

        jobs = []

        for item in data.get("results", []):
            job = Job(
                job_id=(
                    str(item["id"])
                    if item.get("id") is not None
                    else None
                ),
                title=item.get("title", ""),
                company=item.get(
                    "company", {}
                ).get("display_name", "Unknown"),
                location=item.get(
                    "location", {}
                ).get("display_name", "Unknown"),
                url=item.get("redirect_url"),
                description=item.get("description", ""),
            )

            jobs.append(job)

        return jobs
