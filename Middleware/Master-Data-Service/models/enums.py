"""Domain enumerations used across the Master-Data-Service models."""
from enum import Enum


class CapabilityType(str, Enum):
    """The kind of capability a project exposes or provides."""
    API = "API"
    EVENT_PUBLISH = "EVENT_PUBLISH"
    EVENT_CONSUMER = "EVENT_CONSUMER"
    ETL = "ETL"
    VECTOR_DATABASE = "VECTOR_DATABASE"
    MCP_SERVER = "MCP_SERVER"


class TechStackCategory(str, Enum):
    """Category of a tech-stack entry (Java, Python, Spring, Drools, ...)."""
    LANGUAGE = "LANGUAGE"
    FRAMEWORK = "FRAMEWORK"
    DATABASE = "DATABASE"
    RULE_ENGINE = "RULE_ENGINE"
    LIBRARY = "LIBRARY"
    PLATFORM = "PLATFORM"
    TOOL = "TOOL"
    OTHER = "OTHER"


class ArtifactType(str, Enum):
    """Type of a project artifact."""
    DOCUMENT = "DOCUMENT"
    DIAGRAM = "DIAGRAM"
    SPECIFICATION = "SPECIFICATION"
    SOURCE_REPO = "SOURCE_REPO"
    DATASET = "DATASET"
    MODEL = "MODEL"
    OTHER = "OTHER"


class KnowledgeBaseType(str, Enum):
    """Type of a project knowledge base entry."""
    WIKI = "WIKI"
    CONFLUENCE = "CONFLUENCE"
    VECTOR_STORE = "VECTOR_STORE"
    DOCUMENT_SET = "DOCUMENT_SET"
    FAQ = "FAQ"
    RUNBOOK = "RUNBOOK"
    OTHER = "OTHER"


class RecordStatus(str, Enum):
    """Generic lifecycle status for top-level records."""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ARCHIVED = "ARCHIVED"
