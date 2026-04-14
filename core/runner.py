"""CLI-facing runner: parses args, calls registry, formats output."""
from __future__ import annotations

import json
import sys

from core import registry


def run_cli(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        _print_help()
        return 0

    if args[0] == "list":
        tools = registry.list_tools()
        if not tools:
            print("No tools registered.")
        else:
            print(f"{'NAME':<25} {'VERSION':<10} DESCRIPTION")
            print("-" * 70)
            for t in tools:
                print(f"{t['name']:<25} {t['version']:<10} {t['description']}")
        return 0

    tool_name = args[0]
    raw_params = args[1] if len(args) > 1 else "{}"

    try:
        params = json.loads(raw_params)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON params: {exc}", file=sys.stderr)
        return 1

    try:
        tool = registry.get(tool_name)
    except KeyError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    result = tool.run(params)

    if result.success:
        if isinstance(result.output, (dict, list)):
            print(json.dumps(result.output, indent=2, ensure_ascii=False))
        else:
            print(result.output)
        return 0
    else:
        print(str(result), file=sys.stderr)
        return 2


def _print_help() -> None:
    print(
        "cursor-tools — self-expanding toolkit\n"
        "\n"
        "Usage:\n"
        "  python run.py list                         list all available tools\n"
        "  python run.py <tool_name>                  run tool with no params\n"
        "  python run.py <tool_name> '<json_params>'  run tool with JSON params\n"
        "\n"
        "Examples:\n"
        "  python run.py list\n"
        "  python run.py hello_world\n"
        '  python run.py http_probe \'{"url":"https://example.com"}\'\n'
    )
