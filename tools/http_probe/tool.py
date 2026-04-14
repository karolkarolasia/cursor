"""Send an HTTP GET/HEAD request and report status, latency, headers."""
import time
import urllib.error
import urllib.request
from typing import Any

from core.base_tool import BaseTool, ToolResult


class HttpProbeTool(BaseTool):
    name = "http_probe"
    description = "Probe an HTTP/HTTPS URL – status, latency, headers"
    version = "0.1.0"

    def params_schema(self) -> dict:
        return {
            "url": {"type": "str", "required": True},
            "method": {"type": "str", "default": "GET", "choices": ["GET", "HEAD"]},
            "timeout": {"type": "int", "default": 10},
            "follow_redirects": {"type": "bool", "default": True},
        }

    def run(self, params: dict | None = None) -> ToolResult:
        params = params or {}
        url: str = params.get("url", "")
        if not url:
            return ToolResult(success=False, error="'url' param is required")

        method: str = params.get("method", "GET").upper()
        timeout: int = int(params.get("timeout", 10))

        req = urllib.request.Request(url, method=method)
        req.add_header("User-Agent", "cursor-tools/http_probe 0.1.0")

        start = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                elapsed_ms = round((time.perf_counter() - start) * 1000, 1)
                headers: dict[str, Any] = dict(resp.headers)
                output = {
                    "url": url,
                    "final_url": resp.url,
                    "status": resp.status,
                    "reason": resp.reason,
                    "latency_ms": elapsed_ms,
                    "headers": headers,
                }
        except urllib.error.HTTPError as exc:
            elapsed_ms = round((time.perf_counter() - start) * 1000, 1)
            output = {
                "url": url,
                "status": exc.code,
                "reason": exc.reason,
                "latency_ms": elapsed_ms,
                "error": str(exc),
            }
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))

        return ToolResult(success=True, output=output)
