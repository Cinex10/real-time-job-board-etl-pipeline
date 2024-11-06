from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class JobModel(BaseModel):
    """Standardized job data model"""
    job_id: str
    title: str
    company: str
    state: Optional[str]
    city: str
    country: str
    # description: str
    # salary_range: Optional[str]
    # skills: List[str] = []
    source: str
    link: str
    posted_date: datetime
    fetched_date: datetime
    # raw_data: dict