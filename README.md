# cursor-tools

> A self-expanding toolkit built entirely online — no desktop editor, only Cursor AI + GitHub.

This repository is an experiment: can meaningful software be written and evolved purely through Cursor's cloud agent interface, using GitHub as the execution environment?  
The answer is this project: a modular, auto-discovering collection of **tools** that can run locally, in CI, or be triggered manually through GitHub Actions.

---

## Concept

```
cursor-tools/
├── core/                  # Framework: BaseTool, Registry, Runner
├── tools/                 # Each sub-folder = one self-contained tool
│   ├── hello_world/
│   ├── system_info/
│   ├── http_probe/
│   └── file_utils/
├── tests/                 # Pytest smoke-tests for every tool
├── scripts/               # Helper shell scripts
├── docs/                  # Extended documentation
├── .github/workflows/
│   ├── ci.yml             # Auto-run on every push / PR
│   └── run_tool.yml       # Manual trigger: choose tool + JSON params
├── run.py                 # CLI entry point
└── requirements.txt
```

### Design principles

| Principle | Implementation |
|---|---|
| **Zero config** | Tools are auto-discovered by scanning `tools/*/tool.py` |
| **Uniform interface** | Every tool is a `BaseTool` subclass with `run(params) -> ToolResult` |
| **Composable** | Tools can import and call each other via the registry |
| **Cloud-native** | GitHub Actions workflows for CI and on-demand execution |
| **Self-expanding** | Adding a tool = create one folder + one Python file |

---

## Quick start

```bash
pip install -r requirements.txt

# list all tools
python run.py list

# run a tool
python run.py hello_world '{"name":"you"}'
python run.py system_info
python run.py http_probe '{"url":"https://example.com"}'
python run.py file_utils '{"action":"list","path":"."}'
```

### Run tests

```bash
pytest tests/ -v
```

---

## Running in the cloud (GitHub Actions)

### Automatic CI
Every push and pull request triggers `.github/workflows/ci.yml`, which smoke-tests all registered tools.

### Manual trigger
Go to **Actions → Run tool on demand → Run workflow**, fill in:

| Field | Example |
|---|---|
| `tool` | `http_probe` |
| `params` | `{"url":"https://github.com","method":"HEAD"}` |

---

## Adding a new tool

1. Create a folder under `tools/`:

```
tools/my_new_tool/
    __init__.py   (empty)
    tool.py
```

2. Write `tool.py`:

```python
from core.base_tool import BaseTool, ToolResult

class MyNewTool(BaseTool):
    name = "my_new_tool"
    description = "What it does in one line"
    version = "0.1.0"

    def run(self, params: dict | None = None) -> ToolResult:
        params = params or {}
        # ... your logic ...
        return ToolResult(success=True, output="done")
```

3. That's it. The registry auto-discovers it on the next run.

---

## Roadmap ideas

- **secret_store** – read secrets from env / GitHub Secrets and pass them to tools  
- **scheduler** – cron-triggered workflows for periodic tasks  
- **notifier** – send results to Slack / email / webhook  
- **shell_exec** – run arbitrary shell commands (sandboxed)  
- **ai_prompt** – call an LLM API with a prompt, return the response  
- **data_fetch** – download CSV/JSON from a URL, parse and summarise  
- **git_stats** – analyse commit history of any repo  
- **docker_run** – spin up a container task and return its output  

---

## Philosophy

This project grows through Cursor cloud agents.  
Each conversation can add a tool, improve the core, write tests, or trigger a workflow.  
The git history *is* the documentation of what was built and when.
