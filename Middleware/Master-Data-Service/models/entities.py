"""SQLAlchemy ORM models for the Master-Data-Service.

Entity map
----------
- Employee
- Project
- ProjectRole                 roles defined within a project
- ProjectEmployee             (project x employee x role) mapping; an employee may hold
                              multiple roles in a project and belong to multiple projects
- ProjectArtifact             artifacts produced by a project
- ProjectCapability           a capability a project provides (typed)
- ProjectDomain               hierarchical business (sub)domains within a project
- ProjectKnowledgeBase        knowledge-base entries attached to a project (many)
- ProjectTechStack            tech-stack entries (Java, Python, Spring, Drools, ...)
- ProjectDependencyGroup      groups related inter-project dependencies
- ProjectDependency           this project depends on another project's capability
- ProjectClientGroup          groups related clients
- ProjectClient               another project that consumes this project's capability

Foreign keys use ``ondelete="CASCADE"`` where a child cannot exist without its parent.
"""
from sqlalchemy import (
    Column,
    Date,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    String,
    Text,
    Uuid,
    UniqueConstraint,
)

from db.base import Base
from models.enums import (
    ArtifactType,
    CapabilityType,
    KnowledgeBaseType,
    RecordStatus,
    TechStackCategory,
)
from models.mixins import TimestampMixin, UUIDPkMixin


class Employee(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "employees"

    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    title = Column(String(160))
    status = Column(SAEnum(RecordStatus), default=RecordStatus.ACTIVE, nullable=False)


class Project(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "projects"

    name = Column(String(200), nullable=False, unique=True, index=True)
    code = Column(String(60), unique=True)
    description = Column(Text)
    status = Column(SAEnum(RecordStatus), default=RecordStatus.ACTIVE, nullable=False)


class ProjectRole(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "project_roles"
    __table_args__ = (UniqueConstraint("project_id", "name", name="uq_project_role_name"),)

    project_id = Column(Uuid, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(120), nullable=False)
    description = Column(Text)


class ProjectEmployee(UUIDPkMixin, TimestampMixin, Base):
    """Mapping of an employee to a project in a specific role.

    Multiple rows for the same (project, employee) express multiple roles.
    """
    __tablename__ = "project_employees"
    __table_args__ = (
        UniqueConstraint(
            "project_id", "employee_id", "role_id", name="uq_project_employee_role"
        ),
    )

    project_id = Column(Uuid, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    employee_id = Column(Uuid, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id = Column(Uuid, ForeignKey("project_roles.id", ondelete="CASCADE"), nullable=False, index=True)
    allocation_percent = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)


class ProjectArtifact(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "project_artifacts"

    project_id = Column(Uuid, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    artifact_type = Column(SAEnum(ArtifactType), default=ArtifactType.DOCUMENT, nullable=False)
    location = Column(String(1024))
    description = Column(Text)


class ProjectCapability(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "project_capabilities"

    project_id = Column(Uuid, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    capability_type = Column(SAEnum(CapabilityType), nullable=False)
    description = Column(Text)
    # Free-form endpoint / topic / connection detail for the capability.
    details = Column(String(1024))


class ProjectDomain(UUIDPkMixin, TimestampMixin, Base):
    """Hierarchical business (sub)domain within a project (self-referencing)."""
    __tablename__ = "project_domains"

    project_id = Column(Uuid, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    parent_domain_id = Column(
        Uuid, ForeignKey("project_domains.id", ondelete="CASCADE"), nullable=True, index=True
    )


class ProjectKnowledgeBase(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "project_knowledge_bases"

    project_id = Column(Uuid, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    kb_type = Column(SAEnum(KnowledgeBaseType), default=KnowledgeBaseType.DOCUMENT_SET, nullable=False)
    location = Column(String(1024))
    description = Column(Text)


class ProjectTechStack(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "project_tech_stacks"

    project_id = Column(Uuid, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(160), nullable=False)  # e.g. Java, Python, Spring, Drools
    category = Column(SAEnum(TechStackCategory), default=TechStackCategory.OTHER, nullable=False)
    version = Column(String(60))


class ProjectDependencyGroup(UUIDPkMixin, TimestampMixin, Base):
    """A named group bundling several inter-project dependencies as one logical unit."""
    __tablename__ = "project_dependency_groups"

    project_id = Column(Uuid, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)


class ProjectDependency(UUIDPkMixin, TimestampMixin, Base):
    """This project depends on another project's capability.

    ``project_id``            the dependent project (owner of this dependency)
    ``depends_on_project_id`` the provider project
    ``depends_on_capability_id`` the specific provider capability (optional)
    ``group_id``              optional dependency group this belongs to
    """
    __tablename__ = "project_dependencies"

    project_id = Column(Uuid, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    depends_on_project_id = Column(Uuid, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    depends_on_capability_id = Column(
        Uuid, ForeignKey("project_capabilities.id", ondelete="SET NULL"), nullable=True, index=True
    )
    group_id = Column(
        Uuid, ForeignKey("project_dependency_groups.id", ondelete="SET NULL"), nullable=True, index=True
    )
    description = Column(Text)


class ProjectClientGroup(UUIDPkMixin, TimestampMixin, Base):
    """A named group bundling several clients as one logical unit."""
    __tablename__ = "project_client_groups"

    project_id = Column(Uuid, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)


class ProjectClient(UUIDPkMixin, TimestampMixin, Base):
    """Another project that consumes this project's capability.

    ``project_id``           the provider project (owner of this client record)
    ``client_project_id``    the consumer project
    ``client_capability_id`` the specific provider capability consumed (optional)
    ``group_id``             optional client group this belongs to
    """
    __tablename__ = "project_clients"

    project_id = Column(Uuid, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    client_project_id = Column(Uuid, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    client_capability_id = Column(
        Uuid, ForeignKey("project_capabilities.id", ondelete="SET NULL"), nullable=True, index=True
    )
    group_id = Column(
        Uuid, ForeignKey("project_client_groups.id", ondelete="SET NULL"), nullable=True, index=True
    )
    description = Column(Text)
