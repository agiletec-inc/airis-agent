# Super Agent Plugin Installation Guide

This guide explains how to install and use the Super Agent plugin for Claude Code.

## Installation Methods

### Method 1: Direct Installation from GitHub (Recommended)

Install from the GitHub repository marketplace:

```bash
# In Claude Code, run:
/plugin marketplace add kazuki/superagent
/plugin install superagent
```

### Method 2: Auto-Installation for Teams

Add to your project's `.claude/settings.json` to automatically install for all team members:

```json
{
  "marketplaces": ["kazuki/superagent"],
  "enabledPlugins": ["superagent"]
}
```

When team members trust the repository folder, Claude Code will automatically:
1. Install the Super Agent marketplace
2. Enable the `superagent` plugin
3. Activate all commands and agents

### Method 3: Local Development

For plugin development or testing:

```bash
# 1. Clone the repository
git clone https://github.com/kazuki/superagent.git
cd superagent

# 2. Build the plugin
make build-plugin

# 3. Add local marketplace
/plugin marketplace add /path/to/superagent

# 4. Install plugin
/plugin install superagent
```

## What's Included

### Commands

- **`/agent`** - Session orchestrator
  - Auto-launches at session start
  - Coordinates confidence checks, research, and indexing
  - Manages implementation workflow

- **`/research`** - Deep research agent
  - Parallel web search with Tavily/Context7 integration
  - Evidence-based synthesis
  - Multiple depth levels (quick, standard, deep, exhaustive)

- **`/index-repo`** - Repository indexer
  - Generates PROJECT_INDEX.md (94% token reduction)
  - Analyzes codebase structure
  - Creates machine-readable PROJECT_INDEX.json

### Agents

- **`@deep-research`** - External knowledge gathering specialist
- **`@repo-index`** - Codebase briefing assistant
- **`@self-review`** - Post-implementation validation

### Skills

- **`@confidence-check`** - Pre-implementation validation
  - Confidence score ≥0.90 required before implementation
  - Returns checklist and action plan
  - 25-250x token savings ROI

### Auto-Activation

The plugin includes a SessionStart hook that:
1. Checks git status
2. Reports core services availability
3. Activates the `/agent` command automatically

## Verification

After installation, verify the plugin is active:

```bash
# Check available plugins
/plugin list

# Check if Super Agent is enabled
# You should see:
# - superagent (enabled)
```

## Usage Examples

### Basic Workflow

```bash
# 1. Plugin auto-activates at session start
# Output: "Super Agent ready — awaiting task assignment."

# 2. Assign a task
User: "Add user authentication to the API"

# 3. Agent runs confidence check automatically
# Output: "📊 Confidence: 0.85 - Gathering more information..."

# 4. Agent may trigger research if needed
# Uses @deep-research for official documentation

# 5. Implementation with self-review
# Uses @self-review to validate results
```

### Manual Commands

```bash
# Run deep research
/research "Best practices for JWT authentication in Python 2025"

# Index repository
/index-repo

# Update existing index
/index-repo mode=update
```

## Configuration

### Disable Auto-Activation

If you prefer manual activation, modify `hooks/hooks.json`:

```json
{
  "hooks": {
    "SessionStart": []
  }
}
```

### Customize Session Init

Edit `scripts/session-init.sh` to customize startup behavior.

## Troubleshooting

### Plugin Not Found

```bash
# Verify marketplace is added
/plugin marketplace list

# Re-add if needed
/plugin marketplace add kazuki/superagent
```

### Commands Not Available

```bash
# Check if plugin is enabled
/plugin list

# Enable if needed
/plugin enable superagent
```

### Auto-Activation Not Working

1. Check if SessionStart hook is configured in `hooks/hooks.json`
2. Verify `scripts/session-init.sh` is executable
3. Check Claude Code logs for hook execution errors

## Uninstallation

```bash
# Disable the plugin
/plugin disable superagent

# Remove the plugin completely
/plugin uninstall superagent

# Remove the marketplace
/plugin marketplace remove kazuki/superagent
```

## Development

### Building the Plugin

```bash
# Build plugin artifacts
make build-plugin

# Sync to distribution repo (if applicable)
make sync-plugin-repo PLUGIN_REPO=/path/to/dist-repo
```

### Testing

```bash
# Run plugin tests
uv run pytest plugins/superagent/tests/

# Run confidence check tests
uv run python dist/plugins/superagent/.claude-plugin/tests/run_confidence_tests.py
```

## Plugin Structure

```
dist/plugins/superagent/
├── .claude-plugin/
│   ├── plugin.json          # Plugin metadata
│   ├── marketplace.json     # Marketplace info
│   └── tests/               # Plugin tests
├── commands/                # Command definitions
│   ├── agent.md
│   ├── research.md
│   └── index-repo.md
├── agents/                  # Agent definitions
│   ├── deep-research.md
│   ├── repo-index.md
│   └── self-review.md
├── skills/                  # TypeScript skills
│   └── confidence-check/
├── hooks/                   # Hook configurations
│   └── hooks.json
└── scripts/                 # Utility scripts
    └── session-init.sh
```

## Support

- **Issues**: https://github.com/kazuki/superagent/issues
- **Documentation**: See `docs/` directory
- **CLAUDE.md**: Project-specific guidance for Claude Code

## License

MIT License - see LICENSE file for details
