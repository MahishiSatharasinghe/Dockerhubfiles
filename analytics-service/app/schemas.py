from pydantic import BaseModel
from datetime import datetime

class AnalyticsEvent(BaseModel):
    event_type: str
    page_url: str
    user_agent: str
    timestamp: datetime
