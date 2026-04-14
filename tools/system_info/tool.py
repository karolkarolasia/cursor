"""Report basic runtime environment info (useful in cloud runs)."""
import os
import platform
import sys

from core.base_tool import BaseTool, ToolResult


class SystemInfoTool(BaseTool):
    name = "system_info"
    description = "Show OS, Python version, CPU, memory and env metadata"
    version = "0.1.0"

    def run(self, params: dict | None = None) -> ToolResult:
        try:
            import psutil  # optional dependency

            mem = psutil.virtual_memory()
            mem_info = {
                "total_gb": round(mem.total / 1e9, 2),
                "available_gb": round(mem.available / 1e9, 2),
                "percent_used": mem.percent,
            }
            cpu_count = psutil.cpu_count(logical=True)
            cpu_freq = getattr(psutil.cpu_freq(), "current", None)
        except ImportError:
            mem_info = {"note": "install psutil for memory details"}
            cpu_count = os.cpu_count()
            cpu_freq = None

        output = {
            "os": platform.system(),
            "os_release": platform.release(),
            "machine": platform.machine(),
            "python": sys.version,
            "cpu_logical_cores": cpu_count,
            "cpu_freq_mhz": cpu_freq,
            "memory": mem_info,
            "cwd": os.getcwd(),
            "env_vars_count": len(os.environ),
        }
        return ToolResult(success=True, output=output)
