"""Airis Agent MCP Server - Exposes confidence, repo_index, and deep_research as MCP tools."""

from __future__ import annotations

import asyncio
import json
from typing import Any

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

from airis_agent.api.confidence import ConfidenceRequest, evaluate_confidence
from airis_agent.api.deep_research import ResearchRequest, perform_research
from airis_agent.api.repo_index import RepoIndexRequest, generate_repo_index

server = Server("airis-agent")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List all available tools."""
    return [
        types.Tool(
            name="confidence_check",
            description=(
                "Pre-implementation confidence assessment. "
                "Returns score (0.0-1.0), action (proceed/investigate/stop), and checklist. "
                "Prevents wrong-direction work: 25-250x token savings."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Description of the task to assess",
                    },
                    "duplicate_check_complete": {
                        "type": "boolean",
                        "description": "Whether duplicate work has been checked",
                        "default": False,
                    },
                    "architecture_check_complete": {
                        "type": "boolean",
                        "description": "Whether architecture compliance has been verified",
                        "default": False,
                    },
                    "official_docs_verified": {
                        "type": "boolean",
                        "description": "Whether official documentation has been reviewed",
                        "default": False,
                    },
                    "oss_reference_complete": {
                        "type": "boolean",
                        "description": "Whether OSS references have been consulted",
                        "default": False,
                    },
                    "root_cause_identified": {
                        "type": "boolean",
                        "description": "Whether root cause has been identified (for bugs)",
                        "default": False,
                    },
                },
                "required": ["task"],
            },
        ),
        types.Tool(
            name="repo_index",
            description=(
                "Generates PROJECT_INDEX.{md,json} with codebase structure. "
                "Optional on-disk output. 94% token reduction for context."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Absolute path to the repository",
                    },
                    "mode": {
                        "type": "string",
                        "description": "Indexing depth: quick, full, update",
                        "enum": ["quick", "full", "update"],
                        "default": "full",
                    },
                    "include_docs": {
                        "type": "boolean",
                        "description": "Include documentation files",
                        "default": True,
                    },
                    "include_tests": {
                        "type": "boolean",
                        "description": "Include test files",
                        "default": True,
                    },
                    "max_entries": {
                        "type": "integer",
                        "description": "Maximum entries per category",
                        "default": 10,
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "Optional directory to write index files",
                    },
                },
                "required": ["repo_path"],
            },
        ),
        types.Tool(
            name="deep_research",
            description=(
                "Creates wave/queries plan for multi-step research. "
                "Returns findings, sources, and confidence scores. "
                "Integrates with Tavily (web search) and Context7 (official docs)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Research query to investigate",
                    },
                    "depth": {
                        "type": "string",
                        "description": "Research depth level",
                        "enum": ["quick", "standard", "deep", "exhaustive"],
                        "default": "standard",
                    },
                    "constraints": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Additional constraints or focus areas",
                        "default": [],
                    },
                    "seed_sources": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Initial sources to start from",
                        "default": [],
                    },
                },
                "required": ["query"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[
    types.TextContent | types.ImageContent | types.EmbeddedResource
]:
    """Handle tool execution."""
    if arguments is None:
        arguments = {}

    try:
        if name == "confidence_check":
            request = ConfidenceRequest(
                task=arguments["task"],
                duplicate_check_complete=arguments.get("duplicate_check_complete", False),
                architecture_check_complete=arguments.get("architecture_check_complete", False),
                official_docs_verified=arguments.get("official_docs_verified", False),
                oss_reference_complete=arguments.get("oss_reference_complete", False),
                root_cause_identified=arguments.get("root_cause_identified", False),
                metadata=arguments.get("metadata", {}),
            )
            response = evaluate_confidence(request)
            result = {
                "score": response.score,
                "action": response.action,
                "checks": response.checks,
            }
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        if name == "repo_index":
            request = RepoIndexRequest(
                repo_path=arguments["repo_path"],
                mode=arguments.get("mode", "full"),
                include_docs=arguments.get("include_docs", True),
                include_tests=arguments.get("include_tests", True),
                max_entries=arguments.get("max_entries", 10),
                output_dir=arguments.get("output_dir"),
            )
            response = generate_repo_index(request)
            result = {
                "markdown": response.markdown,
                "stats": response.stats,
                "output_paths": [str(path) for path in response.output_paths],
            }
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        if name == "deep_research":
            request = ResearchRequest(
                query=arguments["query"],
                depth=arguments.get("depth", "standard"),
                constraints=arguments.get("constraints", []),
                seed_sources=arguments.get("seed_sources", []),
            )
            response = perform_research(request)
            result = {
                "summary": response.summary,
                "plan": response.plan,
                "findings": response.findings,
                "sources": response.sources,
                "confidence": response.confidence,
            }
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        raise ValueError(f"Unknown tool: {name}")

    except Exception as exc:  # pragma: no cover - returned to caller
        return [types.TextContent(type="text", text=f"Error: {exc}")]


async def main() -> None:
    """Run the MCP server using stdio transport."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def run() -> None:
    """Entry point for the airis-agent-mcp command."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
