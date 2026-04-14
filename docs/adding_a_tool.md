# How to add a new tool

See the README for a quick-start example. This page covers more detail.

## File layout

```
tools/
└── my_tool/
    ├── __init__.py    # empty, marks it as a Python package
    ├── tool.py        # must contain exactly one BaseTool subclass
    └── README.md      # optional, documents params and examples
```

## ToolResult fields

| Field | Type | Meaning |
|---|---|---|
| `success` | `bool` | Whether the tool ran without errors |
| `output` | `Any` | The main result (str, dict, list …) |
| `error` | `str \| None` | Human-readable error message when success=False |
| `metadata` | `dict` | Extra data (timing, version, …) |

## params_schema

Override `params_schema()` to declare accepted parameters:

```python
def params_schema(self) -> dict:
    return {
        "timeout": {"type": "int", "default": 30},
        "url":     {"type": "str", "required": True},
    }
```

This is used by `tool.help()` and will eventually drive auto-generated documentation.

## Using secrets / environment variables

Tools running in GitHub Actions can read secrets injected as env vars:

```python
import os
api_key = os.environ.get("MY_API_KEY", "")
```

Add the secret in **Settings → Secrets and variables → Actions** and reference it in the workflow:

```yaml
env:
  MY_API_KEY: ${{ secrets.MY_API_KEY }}
```
