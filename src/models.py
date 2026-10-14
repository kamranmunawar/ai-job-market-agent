from typing import Optional
from pydantic import BaseModel, HttpUrl

from pydantic import BaseModel
from pydantic import BaseModel, HttpUrl, Field

class Skills(BaseModel):
    programming_languages: list[str] = []
    ai_ml: list[str] = []
    agentic_ai: list[str] = []
    frameworks: list[str] = []
    cloud: list[str] = []
    devops: list[str] = []
    databases: list[str] = []
    other: list[str] = []
class Job(BaseModel):
    title: str
    company: str
    location: str

    url: HttpUrl

    description: str

    salary: Optional[str] = None
    experience: Optional[str] = None

    skills: Skills | None = None
    description_source: str = "api"
    processing_status: str = "pending"
    job_id: str | None = None
    search_categories: list[str] = Field(default_factory=list)
