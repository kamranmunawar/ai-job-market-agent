
import argparse

from job_processor import JobProcessor
from job_repository import JobRepository
from job_storage import JobStorage
from multi_job_search import MultiJobSearchTool

from search_config import (
    SEARCH_QUERIES,
    RESULTS_PER_QUERY,
    PAGES_PER_QUERY,
    MAX_JOBS_PER_RUN,
)


MAX_RETRIES = 3


def parse_args():
    parser = argparse.ArgumentParser(
        description="AI Job Market Agent"
    )

    parser.add_argument(
        "--process-pending",
        action="store_true",
        help="Process existing pending jobs without searching Adzuna",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=MAX_JOBS_PER_RUN,
        help="Maximum jobs to process (default: configured limit)",
    )

    args = parser.parse_args()

    if args.limit < 1:
        parser.error("--limit must be greater than zero")

    return args


def main():
    args = parse_args()

    repository = JobRepository()

    newly_discovered = 0
    already_known = 0
    missing_ids = 0
    jobs = []

    # 1. Discover jobs only in normal mode.
    if not args.process_pending:
        print("\nJOB DISCOVERY")
        print("=" * 70)

        search_tool = MultiJobSearchTool()

        jobs = search_tool.search(
            queries=SEARCH_QUERIES,
            results_per_query=RESULTS_PER_QUERY,
            pages_per_query=PAGES_PER_QUERY,
        )

        for job in jobs:
            if job.job_id is None:
                missing_ids += 1
                continue

            inserted = repository.save_discovered(job)

            if inserted:
                newly_discovered += 1
            else:
                already_known += 1

        print("\nDISCOVERY SUMMARY")
        print("=" * 70)
        print(f"Unique jobs discovered: {len(jobs)}")
        print(f"New jobs stored: {newly_discovered}")
        print(f"Already known: {already_known}")
        print(f"Missing job IDs: {missing_ids}")

    else:
        print("\nPENDING-ONLY MODE")
        print("=" * 70)
        print("Adzuna discovery skipped.")
        print("Processing existing SQLite queue.")

    # 2. Build the processing queue.
    #
    # Pending-only mode processes pending jobs exclusively.
    # Normal mode retains the existing failed-job retry policy.

    if args.process_pending:
        failed_jobs = []
        pending_jobs = repository.get_pending_jobs(
            limit=args.limit
        )

    else:
        failed_jobs = repository.get_retryable_failed_jobs(
            limit=1,
            max_retries=MAX_RETRIES,
        )

        pending_limit = max(
            0,
            args.limit - len(failed_jobs)
        )

        pending_jobs = repository.get_pending_jobs(
            limit=pending_limit
        )

    processing_queue = pending_jobs + failed_jobs

    print("\nPROCESSING PLAN")
    print("=" * 70)
    print(f"Pending jobs selected: {len(pending_jobs)}")
    print(f"Failed jobs selected for retry: {len(failed_jobs)}")
    print(f"Total selected: {len(processing_queue)}")
    print(f"Processing limit: {args.limit}")

    if not processing_queue:
        print("\nNo jobs available for processing.")
        return

    # 3. Initialise tools only when there is work.
    processor = JobProcessor()
    storage = JobStorage()

    processed_jobs = []

    # 4. Process and persist each job immediately.
    for index, job in enumerate(processing_queue, start=1):
        print(f"\nProcessing {index}/{len(processing_queue)}")
        print(f"Job ID: {job.job_id}")
        print(f"Title: {job.title}")
        print(f"Company: {job.company}")

        try:
            processed_job = processor.process(job)

        except Exception as error:
            job.processing_status = "failed"
            processed_job = job
            print(f"Unexpected error: {error}")

        repository.save(processed_job)

        if processed_job.processing_status == "failed":
            repository.increment_retry_count(
                processed_job.job_id
            )

        processed_jobs.append(processed_job)

        print(f"Status: {processed_job.processing_status}")
        print(
            f"Description source: "
            f"{processed_job.description_source}"
        )

    # 5. Export batch JSON.
    output_file = storage.save(processed_jobs)
    print(f"\nBatch JSON saved to: {output_file}")

    # 6. Summarise the run.
    completed = sum(
        job.processing_status == "completed"
        for job in processed_jobs
    )

    failed = sum(
        job.processing_status == "failed"
        for job in processed_jobs
    )

    needs_review = sum(
        job.processing_status == "needs_review"
        for job in processed_jobs
    )

    print("\nBATCH SUMMARY")
    print("=" * 70)
    print(f"Unique jobs discovered: {len(jobs)}")
    print(f"New jobs stored: {newly_discovered}")
    print(f"Processed this run: {len(processed_jobs)}")
    print(f"Completed: {completed}")
    print(f"Failed: {failed}")
    print(f"Needs review: {needs_review}")
    print(f"Total jobs in database: {repository.count()}")


if __name__ == "__main__":
    main()
