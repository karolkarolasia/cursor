"""Auto-discovery and registry of all tools found under tools/."""
from __future__ import annotations

import importlib
import inspect
import pkgutil
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.base_tool import BaseTool

_TOOLS_DIR = Path(__file__).parent.parent / "tools"


def _discover() -> dict[str, "BaseTool"]:
    from core.base_tool import BaseTool  # local import avoids circular

    registry: dict[str, BaseTool] = {}

    for finder, pkg_name, _is_pkg in pkgutil.iter_modules([str(_TOOLS_DIR)]):
        try:
            module = importlib.import_module(f"tools.{pkg_name}.tool")
        except ModuleNotFoundError:
            continue

        for _attr_name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseTool) and obj is not BaseTool:
                instance = obj()
                registry[instance.name] = instance

    return registry


# Module-level singleton – populated on first import
REGISTRY: dict[str, "BaseTool"] = _discover()


def get(name: str) -> "BaseTool":
    if name not in REGISTRY:
        available = ", ".join(sorted(REGISTRY.keys())) or "(none)"
        raise KeyError(f"Tool '{name}' not found. Available: {available}")
    return REGISTRY[name]


def list_tools() -> list[dict]:
    return [
        {"name": t.name, "description": t.description, "version": t.version}
        for t in sorted(REGISTRY.values(), key=lambda t: t.name)
    ]
