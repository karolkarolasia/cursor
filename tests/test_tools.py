"""Smoke tests for core framework and bundled tools."""
import pytest
from core import registry
from core.base_tool import BaseTool, ToolResult


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

def test_registry_not_empty():
    assert len(registry.REGISTRY) >= 1


def test_registry_list_tools_schema():
    tools = registry.list_tools()
    for t in tools:
        assert "name" in t
        assert "description" in t
        assert "version" in t


def test_registry_get_unknown_raises():
    with pytest.raises(KeyError):
        registry.get("__does_not_exist__")


# ---------------------------------------------------------------------------
# hello_world
# ---------------------------------------------------------------------------

def test_hello_world_default():
    tool = registry.get("hello_world")
    result = tool.run()
    assert result.success
    assert "World" in result.output


def test_hello_world_custom_name():
    tool = registry.get("hello_world")
    result = tool.run({"name": "Cursor"})
    assert result.success
    assert "Cursor" in result.output


# ---------------------------------------------------------------------------
# system_info
# ---------------------------------------------------------------------------

def test_system_info_returns_os():
    tool = registry.get("system_info")
    result = tool.run()
    assert result.success
    assert "os" in result.output
    assert "python" in result.output


# ---------------------------------------------------------------------------
# file_utils
# ---------------------------------------------------------------------------

def test_file_utils_list(tmp_path):
    (tmp_path / "a.txt").write_text("hello")
    (tmp_path / "sub").mkdir()
    tool = registry.get("file_utils")
    result = tool.run({"action": "list", "path": str(tmp_path)})
    assert result.success
    names = [e["name"] for e in result.output]
    assert "a.txt" in names
    assert "sub" in names


def test_file_utils_sha256(tmp_path):
    f = tmp_path / "test.txt"
    f.write_bytes(b"hello")
    tool = registry.get("file_utils")
    result = tool.run({"action": "sha256", "path": str(f)})
    assert result.success
    # sha256("hello") = 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
    assert result.output["sha256"].startswith("2cf24dba")


def test_file_utils_missing_params():
    tool = registry.get("file_utils")
    result = tool.run({})
    assert not result.success


# ---------------------------------------------------------------------------
# http_probe
# ---------------------------------------------------------------------------

def test_http_probe_missing_url():
    tool = registry.get("http_probe")
    result = tool.run({})
    assert not result.success
    assert "url" in result.error.lower()
