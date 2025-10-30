# AIRIS MCP Gateway – Unified MCP Management API Plan

## Goals

- Provide a single JSON API that exposes MCP server metadata, enablement state, secret storage, and lifecycle operations.
- Allow three clients to use the same surface:
  1. **Settings UI** (existing Vite app) – keep UX for beginners.
  2. **`airis-mcp-cli`** – power users / automation.
  3. **Super Agents** (SuperClaude, Codex, others) – programmatic orchestration.
- Avoid direct database access from clients; enforce validation and auditing inside the Gateway.
- Supply IDE-specific config renderers (Claude Code, Cursor, Windsurf, etc.) from one canonical model.

## Architectural Overview

```
Clients (UI / CLI / Super Agent)
        │
        ▼
    Gateway API (FastAPI)
        │
        ├── Persistence (Postgres for secrets, profiles for defaults)
        ├── Runtime state (enabled servers, health, logs)
        └── Renderer Layer (per IDE config adapters)
```

## Data Model

*Canonical MCP server descriptor* (`ServerDescriptor`):

```jsonc
{
  "id": "tavily",
  "name": "Tavily Web Search",
  "description": "Web search API for research tasks",
  "category": "research",
  "recommended": true,
  "builtin": false,
  "command": "tavily-mcp-server",
  "args": ["--port", "${PORT}"],
  "env": {
    "TAVILY_API_KEY": "${secret:tavily_api_key}"
  },
  "requiresSecrets": [
    {
      "key": "tavily_api_key",
      "label": "Tavily API Key",
      "description": "Obtain from https://tavily.com",
      "type": "string",
      "required": true
    }
  ],
  "tags": ["web", "search"]
}
```

*State payload* (`ServerState`):

```jsonc
{
  "id": "tavily",
  "enabled": true,
  "lastValidatedAt": "2025-10-28T11:20:00Z",
  "status": "connected", // "disconnected" | "error"
  "errorMessage": null
}
```

*Secret payload* (`SecretEntry`):

```jsonc
{
  "serverId": "tavily",
  "key": "tavily_api_key",
  "value": "…",          // encrypted at rest
  "updatedAt": "2025-10-28T11:21:00Z"
}
```

## Proposed API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/api/v1/mcp/servers` | List catalog entries (defaults + installed custom). |
| `POST` | `/api/v1/mcp/servers` | Add/update a server descriptor (for custom definitions). |
| `DELETE` | `/api/v1/mcp/servers/{id}` | Remove custom server (builtin entries remain read-only). |
| `GET`  | `/api/v1/mcp/state` | Return enablement and runtime status for all servers. |
| `PATCH` | `/api/v1/mcp/state/{id}` | Enable / disable server (`{"enabled": true}`) and trigger restart if needed. |
| `POST` | `/api/v1/mcp/secrets/{id}` | Create/update secrets (payload with key/value map). |
| `DELETE` | `/api/v1/mcp/secrets/{id}` | Remove stored secrets for a server. |
| `POST` | `/api/v1/mcp/validate/{id}` | Run health check; returns validation report. |
| `POST` | `/api/v1/mcp/restart` | Restart gateway services after configuration changes. |
| `GET`  | `/api/v1/mcp/catalog` | Union of builtin profiles + external catalog (Docker Hub, community registry). |
| `GET`  | `/api/v1/mcp/render/{target}` | Render IDE-specific config (e.g. `target=claude-code`, `target=cursor`). |

Authentication: initial implementation can rely on loopback + API token (`X-AIRIS-Token`), later extend to OAuth for remote usage.

## Client Responsibilities

### Settings UI
- Replace direct JSON mutations with API calls.
- Use `catalog` endpoint to populate “Add MCP” modal.
- Leverage `render/{target}` to show copy-paste config previews.

### `airis-mcp-cli`
- Thin wrapper over API (e.g. `airis-mcp list`, `airis-mcp enable tavily`, `airis-mcp secret tavily tavily_api_key`).
- Support scripting via JSON output (`--json`).

### Super Agents
- Detect missing capabilities (language, domain, research) → query `catalog` and propose install.
- Schedule automatic validation and restart via API.
- Persist decisions (e.g., “enable Rust toolchain when project == Rust”) via automation config.

## IDE-specific Rendering

Renderer layer takes canonical descriptor + state + secrets and produces config blocks:

1. **Claude Code**: snippet for `.claude/mcp.json`.
2. **Cursor**: `settings.json` fragment.
3. **Windsurf**: server definitions for `settings.yml`.
4. **OpenHands/Codex**: `.openhands/mcp.json` or CLI invocation.

Each renderer must account for:
- Path mapping (local vs container).
- Secret interpolation (`${secret:key}` → actual value or placeholder depending on target).
- Optional per-IDE flags (e.g. enabling SSE endpoints).

## Roadmap

1. Inventory existing persistence (`profiles/`, DB tables) and align schema with `ServerDescriptor`.
2. Implement FastAPI routes + pydantic schemas, including validation logic.
3. Update Settings UI to consume API.
4. Build CLI client (Python or Node) against the new endpoints.
5. Integrate Super Agent (SuperClaude) with the API.
6. Extend renderers for Cursor, Windsurf, Codex.
7. Add catalog ingestion from external registries (Docker Hub, community JSON feeds).
8. Document API usage in `docs/api/` and generate OpenAPI spec.

## Open Questions

- Authentication model for remote access (CLI on another machine).
- Rate limiting / throttling when Super Agent performs bulk operations.
- Versioning strategy for descriptors (support for schema evolution).
- Secret migration path when renaming server IDs or keys.

This plan aligns Gateway, CLI、Super Agent, and IDE integrations around one responsibility boundary. Implementation should proceed iteratively, starting with read-only catalog exposure, then state mutation, then secret management.
