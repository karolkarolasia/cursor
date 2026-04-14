"""Simplest possible tool – sanity check and template."""
from core.base_tool import BaseTool, ToolResult


class HelloWorldTool(BaseTool):
    name = "hello_world"
    description = "Greet someone; the canonical 'does it work?' tool"
    version = "0.1.0"

    def params_schema(self) -> dict:
        return {"name": {"type": "str", "default": "World"}}

    def run(self, params: dict | None = None) -> ToolResult:
        params = params or {}
        who = params.get("name", "World")
        return ToolResult(success=True, output=f"Hello, {who}!")
