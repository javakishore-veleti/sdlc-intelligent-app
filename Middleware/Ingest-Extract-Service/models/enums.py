"""Enumerations for the ingest log."""
from enum import Enum


class IngestType(str, Enum):
    PDF = "PDF"
    EXCEL = "EXCEL"
    CSV = "CSV"
    IMAGE = "IMAGE"
    OTHER = "OTHER"


class StorageType(str, Enum):
    LOCAL_FILE_SYSTEM = "LOCAL_FILE_SYSTEM"
    AWS_S3 = "AWS_S3"
    AZURE_BLOB = "AZURE_BLOB"
    OTHER = "OTHER"


class IngestProcessStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
