"""Enumerations for workspace (agile delivery) entities."""
from enum import Enum


class WorkItemStatus(str, Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    IN_REVIEW = "IN_REVIEW"
    DONE = "DONE"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"


class SprintStatus(str, Enum):
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"


class ReleaseStatus(str, Enum):
    PLANNED = "PLANNED"
    RELEASED = "RELEASED"
    CANCELLED = "CANCELLED"
