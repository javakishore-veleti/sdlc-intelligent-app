"""ORM models for Workspace-Service (agile delivery artifacts).

Hierarchy:  Project (referenced by id from Master-Data-Service)
              -> Epic -> Feature -> Story
            Sprint and Release are time-boxes a Story can be assigned to.

Every entity carries ``project_id`` (a Master-Data project id; no cross-service FK),
which is what the per-user/admin access scoping filters on. Intra-service references
(epic_id, feature_id, sprint_id, release_id) are real local FKs.
"""
from sqlalchemy import (
    Column,
    Date,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)

from db.base import Base
from models.enums import ReleaseStatus, SprintStatus, WorkItemStatus
from models.mixins import TimestampMixin, UUIDPkMixin


class Epic(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "epics"

    project_id = Column(Uuid, nullable=False, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text)
    status = Column(SAEnum(WorkItemStatus), default=WorkItemStatus.NEW, nullable=False)


class Feature(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "features"

    project_id = Column(Uuid, nullable=False, index=True)
    epic_id = Column(Uuid, ForeignKey("epics.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text)
    status = Column(SAEnum(WorkItemStatus), default=WorkItemStatus.NEW, nullable=False)


class Sprint(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "sprints"

    project_id = Column(Uuid, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    goal = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(SAEnum(SprintStatus), default=SprintStatus.PLANNED, nullable=False)


class Release(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "releases"

    project_id = Column(Uuid, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    release_date = Column(Date)
    status = Column(SAEnum(ReleaseStatus), default=ReleaseStatus.PLANNED, nullable=False)


class Story(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "stories"

    project_id = Column(Uuid, nullable=False, index=True)
    feature_id = Column(Uuid, ForeignKey("features.id", ondelete="SET NULL"), nullable=True, index=True)
    sprint_id = Column(Uuid, ForeignKey("sprints.id", ondelete="SET NULL"), nullable=True, index=True)
    release_id = Column(Uuid, ForeignKey("releases.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text)
    story_points = Column(Integer)
    status = Column(SAEnum(WorkItemStatus), default=WorkItemStatus.NEW, nullable=False)


class WorkspaceMembership(UUIDPkMixin, TimestampMixin, Base):
    """Which projects a user belongs to (drives non-admin access scoping)."""
    __tablename__ = "workspace_memberships"
    __table_args__ = (
        UniqueConstraint("user_email", "project_id", name="uq_membership_user_project"),
    )

    user_email = Column(String(255), nullable=False, index=True)
    project_id = Column(Uuid, nullable=False, index=True)
    role = Column(String(120))
