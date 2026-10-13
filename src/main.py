
from job_search import SearchJobsTool
from job_processor import JobProcessor
from job_deduplicator import JobDeduplicator
from job_repository import JobRepository
from job_storage import JobStorage


def main():
    search_tool = SearchJobsTool()
    processor = JobProcessor()
    deduplicator = JobDeduplicator()
    repository = JobRepository()
    storage = JobStorage()

    # 1. Search for vacancies
    jobs = search_tool.search(
        query="AI Engineer",
        results_per_page=5
    )

    if not jobs:
        print("No jobs found.")
        return

    # 2. Remove duplicates within the search results
    jobs = deduplicator.deduplicate(jobs)

    print(f"\nUnique jobs retrieved: {len(jobs)}")

    processed_jobs = []
    skipped = 0

    # 3. Process only new or previously failed jobs
    for index, job in enumerate(jobs, start=1):
        print(f"\nJob {index}/{len(jobs)}")
        print(f"Title: {job.title}")
        print(f"Company: {job.company}")

        if job.job_id is None:
            print("Skipped: Missing Adzuna job ID")
            skipped += 1
            continue

        status = repository.get_status(job.job_id)

        if status == "completed":
            print("Skipped: Already processed successfully")
            skipped += 1
            continue

        if status == "failed":
            print("Retrying previously failed job")

        try:
            processed_job = processor.process(job)
        except Exception as error:
            job.processing_status = "failed"
            processed_job = job
            print(f"Unexpected processing error: {error}")

        # Save immediately after processing each job
        repository.save(processed_job)
        processed_jobs.append(processed_job)

        print(f"Status: {processed_job.processing_status}")
        print(f"Description source: {processed_job.description_source}")

    # 4. Export newly processed jobs to JSON
    if processed_jobs:
        output_file = storage.save(processed_jobs)
        print(f"\nBatch JSON saved to: {output_file}")

    # 5. Summary
    completed = sum(
        job.processing_status == "completed"
        for job in processed_jobs
    )
    failed = len(processed_jobs) - completed

    print("\nBATCH SUMMARY")
    print("=" * 70)
    print(f"Jobs retrieved: {len(jobs)}")
    print(f"New jobs processed: {len(processed_jobs)}")
    print(f"Completed: {completed}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")
    print(f"Total jobs in database: {repository.count()}")


if __name__ == "__main__":
    main()
