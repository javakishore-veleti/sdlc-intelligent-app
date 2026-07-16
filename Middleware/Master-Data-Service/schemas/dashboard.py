"""Response schemas for dashboard statistics."""
from datetime import datetime

from pydantic import BaseModel


class TechStackStat(BaseModel):
    name: str
    project_count: int


class DashboardStats(BaseModel):
    project_count: int
    top_tech_stacks: list[TechStackStat]
    generated_at: datetime
    cache_ttl_seconds: int
