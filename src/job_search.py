import os

import requests
from dotenv import load_dotenv

from models import Job


load_dotenv()



class SearchJobsTool:

    BASE_URL = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

    def __init__(self):
        self.app_id = os.getenv("ADZUNA_APP_ID")
        self.app_key = os.getenv("ADZUNA_APP_KEY")

        if not self.app_id or not self.app_key:
            raise ValueError(
                "ADZUNA_APP_ID and ADZUNA_APP_KEY must be set"
            )

    def search(
            self,
            query: str,
            results_per_page: int = 20,
    ) -> list[Job]:
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "what": query,
            "results_per_page": results_per_page,
            "content-type": "application/json",
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()
        #print("\nFIELDS RETURNED BY ADZUNA")
        #print("=" * 70)

        #for key in data["results"][0].keys():
          #  print(key)


        print(f"Total jobs available: {data.get('count', 0)}")

        jobs = []

        for item in data.get("results", []):
            job = Job(
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