# Super Agent Plugin Re-organization Plan

## Source of Truth

| Area | Current Repo | Target Location (Framework) | Notes |
|------|--------------|-----------------------------|-------|
| Agent docs (`agents/*.md`) | `Super Agent_Plugin/agents/` | `plugins/superagent/agents/` | Markdown instructions consumed by `/sc:*` commands. |
| Command definitions (`commands/*.md`) | `Super Agent_Plugin/commands/` | `plugins/superagent/commands/` | YAML frontmatter + markdown bodies. |
| Hook config | `Super Agent_Plugin/hooks/hooks.json` | `plugins/superagent/hooks/hooks.json` | SessionStart automation. |
| Skill source (`skills/confidence-check/`) | Divergent copies in both repos | **Single canonical copy in Framework** under `plugins/superagent/skills/confidence-check/` | Replace plugin repo copy with build artefact. |
| Session init scripts | `Super Agent_Plugin/scripts/*.sh` | `plugins/superagent/scripts/` | Executed via Claude Code hooks. |
| Plugin manifest (`.claude-plugin/plugin.json`, `marketplace.json`) | `Super Agent_Plugin/.claude-plugin/` | Generated from `plugins/superagent/manifest/` templates | Manifest fields will be parameterised for official distribution/local builds. |
| Confidence skill tests (`.claude-plugin/tests`) | `Super Agent_Plugin/.claude-plugin/tests/` | `plugins/superagent/tests/` | Keep with Framework to ensure tests run before packaging. |

## Proposed Layout in `superagent`

```
plugins/
  superagent/
    agents/
    commands/
    hooks/
    scripts/
    skills/
      confidence-check/
        SKILL.md
        confidence.ts
    manifest/
      plugin.template.json
      marketplace.template.json
    tests/
      confidence/
        test_cases.json
        expected_results.json
        run.py
```

## Build Workflow

1. `make build-plugin` (new target):
   - Validates skill tests (`uv run` / Node unit tests).
   - Copies `plugins/superagent/*` into a fresh `dist/plugins/superagent/.claude-plugin/…` tree.
   - Renders manifest templates with version/author pulled from `pyproject.toml` / git tags.
2. `make sync-plugin-repo`:
   - Rsyncs the generated artefacts into `../Super Agent_Plugin/`.
   - Cleans stale files before copy (to avoid drift).

## Next Steps

- [ ] Port existing assets from `Super Agent_Plugin` into the Framework layout.
- [ ] Update Framework docs (CLAUDE.md, README) to reference the new build commands.
- [ ] Strip direct edits in `Super Agent_Plugin` by adding a readme banner (“generated – do not edit”) and optional CI guard.
- [ ] Define the roadmap for expanding `/sc:*` commands (identify which legacy flows warrant reintroduction as optional modules).
