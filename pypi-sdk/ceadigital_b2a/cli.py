"""
CLI & Stdio MCP Server entry points for `ceadigital-b2a`.
"""
from __future__ import annotations

import json
import sys
from typing import Any

from .client import EIGHT_TOOLS, call_tool, resolve_tool


def _mcp_tool_definitions() -> list[dict[str, Any]]:
    return [
        {
            "name": t["mcp_name"],
            "description": f"{t['description']} (Free 1-row preview automatic when CEA_API_KEY is unset; Apify: {t['apify_actor']})",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": f"Primary target query, domain, URL, or identifier (default: '{t['default_query']}')",
                        "default": t["default_query"],
                    },
                    "secondary": {
                        "type": "string",
                        "description": "Optional secondary filter (address, condition, permit type, role keyword, or language).",
                        "default": t["default_secondary"],
                    },
                },
                "required": ["query"],
            },
        }
        for t in EIGHT_TOOLS
    ]


def run_mcp_stdio() -> None:
    """Zero-dependency Stdio JSON-RPC 2.0 MCP Server exposing all 8 tools."""
    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except Exception:
            continue
        req_id = msg.get("id")
        method = msg.get("method")
        if req_id is None:
            continue

        if method == "initialize":
            resp: dict[str, Any] = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "ceadigital-b2a", "version": "1.0.0"},
                },
            }
        elif method == "tools/list":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": _mcp_tool_definitions()},
            }
        elif method == "tools/call":
            params = msg.get("params") or {}
            tname = params.get("name") or ""
            args = params.get("arguments") or {}
            tool_def = resolve_tool(tname)
            if not tool_def:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32602,
                        "message": f"Unknown tool '{tname}'. Available: {[t['mcp_name'] for t in EIGHT_TOOLS]}",
                    },
                }
            else:
                out = call_tool(
                    tool_def["id"],
                    query=args.get("query"),
                    secondary=args.get("secondary"),
                )
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(out, indent=2),
                            }
                        ]
                    },
                }
        elif method == "ping":
            resp = {"jsonrpc": "2.0", "id": req_id, "result": {}}
        else:
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            }
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()


def _print_help() -> None:
    lines = [
        "CEA Digital B2B Intelligence Python CLI & MCP Server (ceadigital-b2a v1.0.0)",
        "Playground & Direct API Keys: https://ceadigital.io",
        "",
        "Usage:",
        "  ceadigital-b2a --list                        List all 8 B2B scraping & enrichment tools",
        "  ceadigital-b2a run <tool> [query] [secondary] Run a tool (uses free-preview if CEA_API_KEY unset)",
        "  ceadigital-b2a --mcp                         Start Stdio MCP Server",
        "",
        "Available Tools (8 Engines):",
    ]
    for idx, t in enumerate(EIGHT_TOOLS, 1):
        lines.append(f"  {idx}. {t['id']:18s} ({t['mcp_name']}) — {t['title']}")
    print("\n".join(lines))


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if "--help" in args or "-h" in args or (args and args[0] == "help"):
        _print_help()
        return 0

    if "--list" in args or (args and args[0] == "list"):
        print(
            json.dumps(
                {
                    "package": "ceadigital-b2a",
                    "playground": "https://ceadigital.io",
                    "tools": EIGHT_TOOLS,
                },
                indent=2,
            )
        )
        return 0

    if "--mcp" in args:
        run_mcp_stdio()
        return 0

    if args and (args[0] == "run" or resolve_tool(args[0]) is not None):
        explicit_run = args[0] == "run"
        tool_arg = args[1] if explicit_run and len(args) > 1 else args[0]
        query_arg = args[2] if explicit_run and len(args) > 2 else (args[1] if not explicit_run and len(args) > 1 else None)
        sec_arg = args[3] if explicit_run and len(args) > 3 else (args[2] if not explicit_run and len(args) > 2 else None)
        tdef = resolve_tool(tool_arg)
        if not tdef:
            sys.stderr.write(f"Unknown tool '{tool_arg}'. Run 'ceadigital-b2a --list' to see all 8 tools.\n")
            return 1
        res = call_tool(tdef["id"], query=query_arg, secondary=sec_arg)
        print(json.dumps(res, indent=2))
        return 0

    if not sys.stdin.isatty():
        run_mcp_stdio()
        return 0

    _print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
