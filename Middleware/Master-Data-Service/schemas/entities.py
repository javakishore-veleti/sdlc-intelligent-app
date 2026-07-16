"""Pydantic v2 schemas (Create / Update / Read) for every master-data entity.

Convention per entity:
- ``*Base``   shared fields
- ``*Create`` request body for POST
- ``*Update`` request body for PUT (all fields optional -> partial update)
- ``*Read``   response model (adds id + timestamps, reads from ORM attributes)
"""
from __future__ import annotations

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from models.enums import (
    ArtifactType,
    CapabilityType,
    KnowledgeBaseType,
    RecordStatus,
    TechStackCategory,
)


class _Read(BaseModel):
    """Base read model: reads attributes off ORM instances and carries audit fields."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime


# --------------------------------------------------------------------------- Employee
class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    title: Optional[str] = None
    status: RecordStatus = RecordStatus.ACTIVE


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    title: Optional[str] = None
    status: Optional[RecordStatus] = None


class EmployeeRead(EmployeeBase, _Read):
    pass


# ---------------------------------------------------------------------------- Project
class ProjectBase(BaseModel):
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    status: RecordStatus = RecordStatus.ACTIVE


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    status: Optional[RecordStatus] = None


class ProjectRead(ProjectBase, _Read):
    pass


# ------------------------------------------------------------------------ ProjectRole
class ProjectRoleBase(BaseModel):
    project_id: UUID
    name: str
    description: Optional[str] = None


class ProjectRoleCreate(ProjectRoleBase):
    pass


class ProjectRoleUpdate(BaseModel):
    project_id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectRoleRead(ProjectRoleBase, _Read):
    pass


# -------------------------------------------------------------------- ProjectEmployee
class ProjectEmployeeBase(BaseModel):
    project_id: UUID
    employee_id: UUID
    role_id: UUID
    allocation_percent: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class ProjectEmployeeCreate(ProjectEmployeeBase):
    pass


class ProjectEmployeeUpdate(BaseModel):
    project_id: Optional[UUID] = None
    employee_id: Optional[UUID] = None
    role_id: Optional[UUID] = None
    allocation_percent: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class ProjectEmployeeRead(ProjectEmployeeBase, _Read):
    pass


# -------------------------------------------------------------------- ProjectArtifact
class ProjectArtifactBase(BaseModel):
    project_id: UUID
    name: str
    artifact_type: ArtifactType = ArtifactType.DOCUMENT
    location: Optional[str] = None
    description: Optional[str] = None


class ProjectArtifactCreate(ProjectArtifactBase):
    pass


class ProjectArtifactUpdate(BaseModel):
    project_id: Optional[UUID] = None
    name: Optional[str] = None
    artifact_type: Optional[ArtifactType] = None
    location: Optional[str] = None
    description: Optional[str] = None


class ProjectArtifactRead(ProjectArtifactBase, _Read):
    pass


# ------------------------------------------------------------------ ProjectCapability
class ProjectCapabilityBase(BaseModel):
    project_id: UUID
    name: str
    capability_type: CapabilityType
    description: Optional[str] = None
    details: Optional[str] = None


class ProjectCapabilityCreate(ProjectCapabilityBase):
    pass


class ProjectCapabilityUpdate(BaseModel):
    project_id: Optional[UUID] = None
    name: Optional[str] = None
    capability_type: Optional[CapabilityType] = None
    description: Optional[str] = None
    details: Optional[str] = None


class ProjectCapabilityRead(ProjectCapabilityBase, _Read):
    pass


# ---------------------------------------------------------------------- ProjectDomain
class ProjectDomainBase(BaseModel):
    project_id: UUID
    name: str
    description: Optional[str] = None
    parent_domain_id: Optional[UUID] = None


class ProjectDomainCreate(ProjectDomainBase):
    pass


class ProjectDomainUpdate(BaseModel):
    project_id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    parent_domain_id: Optional[UUID] = None


class ProjectDomainRead(ProjectDomainBase, _Read):
    pass


# --------------------------------------------------------------- ProjectKnowledgeBase
class ProjectKnowledgeBaseBase(BaseModel):
    project_id: UUID
    name: str
    kb_type: KnowledgeBaseType = KnowledgeBaseType.DOCUMENT_SET
    location: Optional[str] = None
    description: Optional[str] = None


class ProjectKnowledgeBaseCreate(ProjectKnowledgeBaseBase):
    pass


class ProjectKnowledgeBaseUpdate(BaseModel):
    project_id: Optional[UUID] = None
    name: Optional[str] = None
    kb_type: Optional[KnowledgeBaseType] = None
    location: Optional[str] = None
    description: Optional[str] = None


class ProjectKnowledgeBaseRead(ProjectKnowledgeBaseBase, _Read):
    pass


# ------------------------------------------------------------------- ProjectTechStack
class ProjectTechStackBase(BaseModel):
    project_id: UUID
    name: str
    category: TechStackCategory = TechStackCategory.OTHER
    version: Optional[str] = None


class ProjectTechStackCreate(ProjectTechStackBase):
    pass


class ProjectTechStackUpdate(BaseModel):
    project_id: Optional[UUID] = None
    name: Optional[str] = None
    category: Optional[TechStackCategory] = None
    version: Optional[str] = None


class ProjectTechStackRead(ProjectTechStackBase, _Read):
    pass


# ------------------------------------------------------------ ProjectDependencyGroup
class ProjectDependencyGroupBase(BaseModel):
    project_id: UUID
    name: str
    description: Optional[str] = None


class ProjectDependencyGroupCreate(ProjectDependencyGroupBase):
    pass


class ProjectDependencyGroupUpdate(BaseModel):
    project_id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectDependencyGroupRead(ProjectDependencyGroupBase, _Read):
    pass


# ----------------------------------------------------------------- ProjectDependency
class ProjectDependencyBase(BaseModel):
    project_id: UUID
    depends_on_project_id: UUID
    depends_on_capability_id: Optional[UUID] = None
    group_id: Optional[UUID] = None
    description: Optional[str] = None


class ProjectDependencyCreate(ProjectDependencyBase):
    pass


class ProjectDependencyUpdate(BaseModel):
    project_id: Optional[UUID] = None
    depends_on_project_id: Optional[UUID] = None
    depends_on_capability_id: Optional[UUID] = None
    group_id: Optional[UUID] = None
    description: Optional[str] = None


class ProjectDependencyRead(ProjectDependencyBase, _Read):
    pass


# --------------------------------------------------------------- ProjectClientGroup
class ProjectClientGroupBase(BaseModel):
    project_id: UUID
    name: str
    description: Optional[str] = None


class ProjectClientGroupCreate(ProjectClientGroupBase):
    pass


class ProjectClientGroupUpdate(BaseModel):
    project_id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectClientGroupRead(ProjectClientGroupBase, _Read):
    pass


# -------------------------------------------------------------------- ProjectClient
class ProjectClientBase(BaseModel):
    project_id: UUID
    client_project_id: UUID
    client_capability_id: Optional[UUID] = None
    group_id: Optional[UUID] = None
    description: Optional[str] = None


class ProjectClientCreate(ProjectClientBase):
    pass


class ProjectClientUpdate(BaseModel):
    project_id: Optional[UUID] = None
    client_project_id: Optional[UUID] = None
    client_capability_id: Optional[UUID] = None
    group_id: Optional[UUID] = None
    description: Optional[str] = None


class ProjectClientRead(ProjectClientBase, _Read):
    pass
