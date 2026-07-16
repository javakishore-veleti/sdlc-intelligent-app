"""Pydantic v2 schemas (Create / Update / Read) for workspace entities."""
from __future__ import annotations

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from models.enums import ReleaseStatus, SprintStatus, WorkItemStatus


class _Read(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime


# ------------------------------------------------------------------------------- Epic
class EpicBase(BaseModel):
    project_id: UUID
    title: str
    description: Optional[str] = None
    status: WorkItemStatus = WorkItemStatus.NEW


class EpicCreate(EpicBase):
    pass


class EpicUpdate(BaseModel):
    project_id: Optional[UUID] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[WorkItemStatus] = None


class EpicRead(EpicBase, _Read):
    pass


# ---------------------------------------------------------------------------- Feature
class FeatureBase(BaseModel):
    project_id: UUID
    epic_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    status: WorkItemStatus = WorkItemStatus.NEW


class FeatureCreate(FeatureBase):
    pass


class FeatureUpdate(BaseModel):
    project_id: Optional[UUID] = None
    epic_id: Optional[UUID] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[WorkItemStatus] = None


class FeatureRead(FeatureBase, _Read):
    pass


# ----------------------------------------------------------------------------- Sprint
class SprintBase(BaseModel):
    project_id: UUID
    name: str
    goal: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: SprintStatus = SprintStatus.PLANNED


class SprintCreate(SprintBase):
    pass


class SprintUpdate(BaseModel):
    project_id: Optional[UUID] = None
    name: Optional[str] = None
    goal: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[SprintStatus] = None


class SprintRead(SprintBase, _Read):
    pass


# ---------------------------------------------------------------------------- Release
class ReleaseBase(BaseModel):
    project_id: UUID
    name: str
    description: Optional[str] = None
    release_date: Optional[date] = None
    status: ReleaseStatus = ReleaseStatus.PLANNED


class ReleaseCreate(ReleaseBase):
    pass


class ReleaseUpdate(BaseModel):
    project_id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    release_date: Optional[date] = None
    status: Optional[ReleaseStatus] = None


class ReleaseRead(ReleaseBase, _Read):
    pass


# ------------------------------------------------------------------------------ Story
class StoryBase(BaseModel):
    project_id: UUID
    feature_id: Optional[UUID] = None
    sprint_id: Optional[UUID] = None
    release_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    story_points: Optional[int] = None
    status: WorkItemStatus = WorkItemStatus.NEW


class StoryCreate(StoryBase):
    pass


class StoryUpdate(BaseModel):
    project_id: Optional[UUID] = None
    feature_id: Optional[UUID] = None
    sprint_id: Optional[UUID] = None
    release_id: Optional[UUID] = None
    title: Optional[str] = None
    description: Optional[str] = None
    story_points: Optional[int] = None
    status: Optional[WorkItemStatus] = None


class StoryRead(StoryBase, _Read):
    pass


# ------------------------------------------------------------------ WorkspaceMembership
class WorkspaceMembershipBase(BaseModel):
    user_email: EmailStr
    project_id: UUID
    role: Optional[str] = None


class WorkspaceMembershipCreate(WorkspaceMembershipBase):
    pass


class WorkspaceMembershipUpdate(BaseModel):
    user_email: Optional[EmailStr] = None
    project_id: Optional[UUID] = None
    role: Optional[str] = None


class WorkspaceMembershipRead(WorkspaceMembershipBase, _Read):
    pass
