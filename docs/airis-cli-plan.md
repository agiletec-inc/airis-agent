# `airis-mcp-cli` – Unified CLI UX Plan

## Goals

- Provide a single command-line entry point to inspect and manage MCP servers exposed by AIRIS MCP Gateway.
- Mirror the HTTP API (`docs/mcp-api-plan.md`) so CLI and Airis Agent share the same surface.
- Support both human-readable output and JSON for scripting.
- Offer guardrails (validation, secret prompts) so users avoid invalid configurations.

## Command Surface (initial draft)

```
airis-mcp
  catalog                     # list available servers (builtin + external)
  list                        # show installed servers with status/enablement
  show <id>                   # detailed view (descriptor + state + secrets mask)
  add <id> [--from <url>]     # install server from catalog or custom descriptor
  enable <id>
  disable <id>
  remove <id>                 # remove custom server (builtin → error)
  secret set <id> <key>       # prompt for value (masked input)
  secret remove <id> <key>
  validate <id>               # run health check via API
  render <target> [--output <path>]  # generate IDE config snippet
  restart                     # trigger gateway restart
  doctor                      # ping API / show summary
```

Global options:
- `--api-url` (default `http://api.gateway.local` as configured)
- `--token` or `AIRIS_MCP_TOKEN`
- `--json` for machine-parseable output
- `--yes` for non-interactive confirmations

## Implementation Sketch

- Language: Python (click + httpx) or Node (commander + axios). Python aligns with Gateway backend and existing tooling.
- Structure:
  - `airis_mcp_cli/api.py` – thin wrapper around HTTP endpoints
  - `airis_mcp_cli/renderers.py` – uses `/render/{target}` when available; fallback to client-side template
  - `airis_mcp_cli/utils.py` – formatting, prompts, secret input (`getpass`)
  - `airis_mcp_cli/main.py` – command definitions
- Packaging: distribute as pip package (`pipx install airis-mcp-cli`) + binary entry point via `setuptools`.
- Testing: 
  - unit tests with `pytest` using mocked responses
  - integration tests executed inside dev container hitting local API

## UX Notes

- `list` default columns: ID, Category, Enabled, Status, Recommended.
- `list --json` returns array of `ServerDescriptor` merged with state.
- `add` flows:
  1. `airis-mcp add tavily` – fetch from catalog, create descriptor via POST `/servers`.
  2. `airis-mcp add custom --from path/to/descriptor.json` – upload entire JSON.
  3. After add, automatically prompt for required secrets and optionally enable.
- Errors from API should be surfaced with a friendly message; `--debug` prints raw details.

## Integration with Airis Agent

- Airis Agent can shell out to CLI (quick win) or use shared library (`airis_mcp_cli.api`).
- Expose Python API entry points so Airis Agent imports functions directly without subprocess overhead.
- Example:
  ```python
  from airis_mcp_cli.api import GatewayClient
  client = GatewayClient(base_url="http://gateway.local", token="...")
  descriptor = client.get_server("tavily")
  if not descriptor.enabled:
      client.enable_server("tavily")
  ```

## Milestones

1. Scaffold package with minimal `catalog` / `list` commands (read-only).
2. Add secret management and enable/disable toggles.
3. Implement `render` for Claude Code + Cursor.
4. Integrate `doctor` and `restart`.
5. Write documentation (`README` + usage examples).
6. Bundle into installer (`make install` optionally installs CLI via pipx).

## Open Questions

- Auth handshake for remote use (token vs mutual TLS).
- Offline catalog caching strategy.
- How to handle MCP server versions / updates (maybe `airis-mcp update`).
- Should CLI support profile export/import (e.g., `airis-mcp profile save dev.json`)?

This CLI plan keeps the UX coherent across novices (UI), pros (CLI), and automation (Airis Agent).
