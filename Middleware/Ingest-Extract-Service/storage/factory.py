"""Selects the storage backend from configuration."""
from common.constants.constants import DATALAKE_BASE_PATH, STORAGE_BACKEND
from common.storage.interfaces.storage_backend import StorageBackendInterface
from storage.local_storage import LocalFileSystemStorage


def get_storage_backend() -> StorageBackendInterface:
    if STORAGE_BACKEND == "local":
        return LocalFileSystemStorage(DATALAKE_BASE_PATH)
    # Future: "aws_s3" -> S3Storage(...), "azure_blob" -> AzureBlobStorage(...)
    raise ValueError(f"Unsupported STORAGE_BACKEND: {STORAGE_BACKEND!r}")
