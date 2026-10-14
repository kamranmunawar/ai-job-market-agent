
from job_description_fetcher import JobDescriptionFetcherTool
from skill_extractor import SkillExtractorTool
from skill_normalizer import SkillNormalizerTool
from models import Job
from employer_job_finder import EmployerJobFinderTool


class JobProcessor:

    def __init__(self):
        self.description_tool = JobDescriptionFetcherTool()
        self.skill_tool = SkillExtractorTool()
        self.normalizer_tool = SkillNormalizerTool()
        self.employer_finder = EmployerJobFinderTool()

    def process(self, job: Job) -> Job:
        try:
            # Preserve the original Adzuna snippet as fallback.
            adzuna_description = job.description

            description = adzuna_description
            source = "partial"

            # Search for a verified full employer description.
            try:
                match = self.employer_finder.find(
                    company=job.company,
                    title=job.title,
                    snippet=adzuna_description,
                    location=job.location,
                )

                if match is not None:
                    description = match.description
                    source = "full"

                    print(
                        "Verified employer description found: "
                        f"{len(description)} characters"
                    )
                else:
                    print(
                        "No verified employer description. "
                        "Using Adzuna snippet."
                    )

            except Exception as error:
                print(
                    f"Employer search failed: {error}. "
                    "Using Adzuna snippet."
                )

            job.description = description
            job.description_source = source

            # Extract skills using the selected description.
            raw_skills = self.skill_tool.extract(job.description)

            # Normalise extracted skills.
            job.skills = self.normalizer_tool.normalize(raw_skills)

            skill_count = sum(
                len(values)
                for values in job.skills.model_dump().values()
            )

            if skill_count == 0:
                job.processing_status = "needs_review"
                print(
                    "WARNING: No skills extracted. "
                    "Job marked for review."
                )
            else:
                job.processing_status = "completed"

            print(f"Extracted skill entries: {skill_count}")

        except Exception as error:
            job.processing_status = "failed"
            print(f"Failed to process {job.title}: {error}")

        return job
