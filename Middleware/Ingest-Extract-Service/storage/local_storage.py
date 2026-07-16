"""Local filesystem storage backend.

Layout:  <base>/datalake/pdfs/<ref_id>/<filename>
         <base>/datalake/pdfs/<ref_id>/manifest.json
"""
import json
from pathlib import Path

from common.storage.interfaces.storage_backend import StorageBackendInterface
from models.enums import StorageType


class LocalFileSystemStorage(StorageBackendInterface):
    def __init__(self, base_path: str) -> None:
        self.base = Path(base_path).expanduser()

    @property
    def storage_type(self) -> str:
        return StorageType.LOCAL_FILE_SYSTEM.value

    def _folder(self, ref_id: str) -> Path:
        folder = self.base / "datalake" / "pdfs" / ref_id
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def save_file(self, ref_id: str, filename: str, content: bytes) -> str:
        dest = self._folder(ref_id) / filename
        dest.write_bytes(content)
        return str(dest)

    def save_manifest(self, ref_id: str, manifest: dict) -> str:
        dest = self._folder(ref_id) / "manifest.json"
        dest.write_text(json.dumps(manifest, indent=2, default=str))
        return str(dest)
