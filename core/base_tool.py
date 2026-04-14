"""Base class that every tool must inherit from."""
from __future__ import annotations

import abc
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolResult:
    """Standardised return value from any tool run."""

    success: bool
    output: Any = None
    error: str | None = None
    metadata: dict = field(default_factory=dict)

    def __str__(self) -> str:
        if self.success:
            return str(self.output)
        return f"ERROR: {self.error}"


class BaseTool(abc.ABC):
    """
    Every tool must inherit BaseTool and implement:
        - name          : str  – unique snake_case identifier
        - description   : str  – one-line human description
        - run(params)   : ToolResult
    """

    name: str
    description: str
    version: str = "0.1.0"

    @abc.abstractmethod
    def run(self, params: dict | None = None) -> ToolResult:
        """Execute the tool logic and return a ToolResult."""

    def help(self) -> str:
        return (
            f"Tool   : {self.name} v{self.version}\n"
            f"Desc   : {self.description}\n"
            f"Params : {self.params_schema()}"
        )

    def params_schema(self) -> dict:
        """Override to declare expected params with types and defaults."""
        return {}
