"""
CEA Digital B2B Intelligence Python SDK (`ceadigital-b2a`).
Provides typed Python methods, CLI commands, and a zero-dependency Stdio MCP server
for all 8 https://ceadigital.io/v1/tools/* Pure-HTTP engines with automatic free-preview fallback.
"""
from __future__ import annotations

from .client import EIGHT_TOOLS, CeaDigitalB2AClient, call_tool, resolve_tool

__version__ = "1.0.0"
__all__ = [
    "CeaDigitalB2AClient",
    "EIGHT_TOOLS",
    "call_tool",
    "resolve_tool",
    "__version__",
]
