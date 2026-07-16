"""Storage-backend contract.

Implementations persist an uploaded file and its manifest under a per-document key
(the datalake UUID). The local filesystem backend is implemented today; S3 / Azure
Blob / others plug in behind this same interface.
"""
from abc import ABC, abstractmethod


class StorageBackendInterface(ABC):
    @property
    @abstractmethod
    def storage_type(self) -> str:
        """A StorageType value, e.g. 'LOCAL_FILE_SYSTEM'."""

    @abstractmethod
    def save_file(self, ref_id: str, filename: str, content: bytes) -> str:
        """Persist the file; return its location (path/URI)."""

    @abstractmethod
    def save_manifest(self, ref_id: str, manifest: dict) -> str:
        """Persist the manifest JSON; return its location (path/URI)."""
