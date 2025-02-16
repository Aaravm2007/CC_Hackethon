from pydantic import BaseModel
from typing import List

class FounderCreate(BaseModel):
    name: str
    linkedin_id: str
    email: str
    linkedin_url: str
    job_title: str
    skills: List[str]
    experience: List[str]

class MatchResponse(BaseModel):
    matched_founder: str
    compatibility_score: float
