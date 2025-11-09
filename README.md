# Super Agent

Host-agnostic orchestration runtime that unifies the former SuperClaude code into a reusable ABI. Super Agent exposes confidence gating, repository indexing, and deep-research planning so IDEs (Claude Code, Codex CLI, Gemini CLI, Cursor, etc.) can share the same workflow logic without duplicating Markdown slash-command specs.

## Why this repo exists

- **ABI-first**: Python modules under `src/superagent/api/` provide typed request/response DTOs so an MCP gateway or any CLI can call Super Agent capabilities directly.
- **Single source of truth**: The runtime (confidence gate, parallel executor, reflexion/self-check, repo indexer) lives in one package and the Claude plugin artifacts (`plugins/superagent`) are generated from it. No more drifting copies under `~/.claude`.
- **Roadmap driven**: Everything is being rebuilt from scratch—the historical SuperClaude docs were mostly empty. This repository now tracks the fresh implementation.

## Current architecture

```
superagent/
├── src/superagent/
│   ├── api/                 # ABI endpoints (confidence, repo index, deep research)
│   ├── cli/                 # Typer CLI (install-skill, doctor, version)
│   ├── execution/           # Parallel executor, reflection, self-correction
│   ├── pm_agent/            # Confidence checker, self-check protocol, reflexion pattern
│   └── pytest_plugin.py     # Auto-loaded pytest integration
├── plugins/superagent/      # Claude plugin assets (commands, agents, hooks, scripts, skills)
├── docs/                    # Design notes, research, user/developer guides
├── tests/                   # Pytest suite (including ABI regression tests)
├── scripts/                 # Build/publish/cleanup helpers
└── Makefile                 # install/test/lint/build-plugin targets
```

### ABI endpoints

| Module | Purpose | Notes |
|--------|---------|-------|
| `superagent.api.confidence` | Pre-implementation confidence gate | wraps `ConfidenceChecker`, returns score/action/checklist |
| `superagent.api.repo_index` | Repository indexing service | generates `PROJECT_INDEX.{md,json}` with optional on-disk output |
| `superagent.api.deep_research` | Deep Research planning | creates wave/queries plan + findings/sources/confidence |

### Runtime building blocks

- **Parallel Executor** (`execution/parallel.py`) — wave-based dependency planner with thread pool execution.
- **Reflexion & Self-correction** (`execution/reflection.py`, `execution/self_correction.py`) — error learning, prevention rules, and failure signatures.
- **PM Agent Core** (`pm_agent/`) — confidence gate, self-check protocol, reflexion memory, token budgeting.
- **Pytest Plugin** (`pytest_plugin.py`) — injects fixtures and markers for Super Agent workflows.

### Plugin bundle

`plugins/superagent/` contains the Markdown command specs (`commands/*.md`), agents, hooks, session-init script, and the TypeScript skill (`skills/confidence-check`). Use `make build-plugin` to package into `dist/plugins/superagent/.claude-plugin`.

## Quick start

```bash
uv pip install -e .        # install Super Agent runtime
uv run superagent doctor   # verify installation
uv run pytest              # run full test suite
make build-plugin          # build Claude plugin assets
```

## Roadmap (2025)

1. **ABI hardening**
   - Finalize JSON schemas for confidence/repo-index/deep-research and document them under `docs/mcp-api-plan.md`.
   - Add streaming / partial responses so MCP gateways can surface progress updates.
2. **Gateway integrations**
   - Connect `airis-mcp-gateway` to these ABI endpoints (confidence gate first, then repo index, then research).
   - Publish sample Codex CLI that calls the ABI directly (no MCP) to prove host-agnostic behavior.
3. **Runtime enhancements**
   - Finish repo indexing script (diff-aware incremental mode, caching layer).
   - Expand deep-research planner to orchestrate actual MCP tool calls rather than stubbed plans.
   - Add trace logging + metrics for parallel executor.
4. **Docs & tooling**
   - Replace legacy SuperClaude documents with concise Super Agent guides (architecture, ABI usage, troubleshooting).
   - Write migration notes for anyone moving from LLM-specific slash commands to the new ABI.

## Contributing

- Run `uv run pytest` and `make lint` before submitting PRs.
- Use Conventional Commit messages (`feat:`, `fix:`, `refactor:` etc.).
- Open issues/PRs at [github.com/kazuki/superagent](https://github.com/kazuki/superagent).

## License

MIT — see [LICENSE](LICENSE).
