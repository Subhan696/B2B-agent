from pydantic import BaseModel
from typing import List, Optional

class CompanyRequest(BaseModel):
    domain: str
    company_name: Optional[str] = None

class ResearchResult(BaseModel):
    news_headlines: List[str]
    ceo_name: Optional[str]
    ceo_recent_activity: List[str]
    pain_points: List[str]

class AgentOutput(BaseModel):
    research: ResearchResult
    email_draft: str
    video_script: str
