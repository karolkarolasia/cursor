"""Basic file-system utilities: list, stat, read text, checksum."""
import hashlib
import os
from pathlib import Path

from core.base_tool import BaseTool, ToolResult


class FileUtilsTool(BaseTool):
    name = "file_utils"
    description = "List directory, stat a file, read text, compute SHA-256"
    version = "0.1.0"

    def params_schema(self) -> dict:
        return {
            "action": {
                "type": "str",
                "required": True,
                "choices": ["list", "stat", "read", "sha256"],
            },
            "path": {"type": "str", "required": True},
        }

    def run(self, params: dict | None = None) -> ToolResult:
        params = params or {}
        action = params.get("action", "")
        raw_path = params.get("path", "")

        if not action or not raw_path:
            return ToolResult(success=False, error="'action' and 'path' are required")

        path = Path(raw_path).expanduser().resolve()

        if action == "list":
            if not path.is_dir():
                return ToolResult(success=False, error=f"Not a directory: {path}")
            entries = []
            for entry in sorted(path.iterdir()):
                entries.append(
                    {
                        "name": entry.name,
                        "type": "dir" if entry.is_dir() else "file",
                        "size": entry.stat().st_size if entry.is_file() else None,
                    }
                )
            return ToolResult(success=True, output=entries)

        elif action == "stat":
            if not path.exists():
                return ToolResult(success=False, error=f"Path not found: {path}")
            s = path.stat()
            return ToolResult(
                success=True,
                output={
                    "path": str(path),
                    "type": "dir" if path.is_dir() else "file",
                    "size_bytes": s.st_size,
                    "modified": s.st_mtime,
                },
            )

        elif action == "read":
            if not path.is_file():
                return ToolResult(success=False, error=f"Not a file: {path}")
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
                return ToolResult(success=True, output=text)
            except OSError as exc:
                return ToolResult(success=False, error=str(exc))

        elif action == "sha256":
            if not path.is_file():
                return ToolResult(success=False, error=f"Not a file: {path}")
            h = hashlib.sha256()
            with path.open("rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    h.update(chunk)
            return ToolResult(
                success=True, output={"path": str(path), "sha256": h.hexdigest()}
            )

        return ToolResult(success=False, error=f"Unknown action: {action}")
