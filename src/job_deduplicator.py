from models import Job


class JobDeduplicator:

    def deduplicate(self, jobs: list[Job]) -> list[Job]:
        unique_jobs = []
        seen_ids = set()

        for job in jobs:
            if job.job_id is None:
                # Keep records without an ID rather than
                # incorrectly treating them as duplicates.
                unique_jobs.append(job)
                continue

            if job.job_id in seen_ids:
                continue

            seen_ids.add(job.job_id)
            unique_jobs.append(job)

        return unique_jobs