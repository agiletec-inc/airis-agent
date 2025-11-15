# Airis Agent Troubleshooting Guide 🔧

Quick fixes to advanced diagnostics for Airis Agent issues.

## Quick Fixes (90% of problems)

**Installation Verification:**
```bash
python3 -m Airis Agent --version    # Should show 4.1.5
Airis Agent install --list-components
```

**Command Issues:**
```bash
# Test in Claude Code:
/airis:brainstorm "test project"        # Should ask discovery questions

# If no response: Restart Claude Code session
```

**Resolution Checklist:**
- [ ] Version commands work and show 4.1.5
- [ ] `/airis:` commands respond in Claude Code  
- [ ] MCP servers listed: `Airis Agent install --list-components | grep mcp`

## Common Issues

### Installation Problems

**Package Installation Fails:**
```bash
# For pipx users
pipx uninstall Airis Agent
pipx install Airis Agent

# For pip users
pip uninstall Airis Agent
pip install --upgrade pip
pip install Airis Agent
```

**Permission Denied / PEP 668 Error:**
```bash
# Option 1: Use pipx (recommended)
pipx install Airis Agent

# Option 2: Use pip with --user flag
pip install --user Airis Agent

# Option 3: Fix permissions
sudo chown -R $USER ~/.claude

# Option 4: Force installation (use with caution)
pip install --break-system-packages Airis Agent
```

**Component Missing:**
```bash
python3 -m Airis Agent install --components core commands agents modes --force
```

### Command Issues

**Commands Not Recognized:**
1. Restart Claude Code completely
2. Verify: `python3 -m Airis Agent --version`
3. Test: `/airis:brainstorm "test"`

**Agents Not Activating:**
- Use specific keywords: `/airis:implement "secure JWT authentication"`
- Manual activation: `@agent-security "review auth code"`

**Slow Performance:**
```bash
/airis:analyze . --no-mcp               # Test without MCP servers
/airis:analyze src/ --scope file        # Limit scope
```

### MCP Server Issues

**Server Connection Fails:**
```bash
ls ~/.claude/.claude.json            # Check config exists
node --version                       # Verify Node.js 16+
Airis Agent install --components mcp --force
```

**API Key Required (Magic/Morphllm):**
```bash
export TWENTYFIRST_API_KEY="your_key"
export MORPH_API_KEY="your_key"
# Or use: /airis:command --no-mcp
```

## Advanced Diagnostics

**System Analysis:**
```bash
Airis Agent install --diagnose
cat ~/.claude/logs/superagent.log | tail -50
```

**Component Analysis:**
```bash
ls -la ~/.claude/                    # Check installed files
grep -r "@" ~/.claude/CLAUDE.md      # Verify imports
```

**Reset Installation:**
```bash
Airis Agent backup --create          # Backup first
Airis Agent uninstall
Airis Agent install --fresh
```

## Get Help

**Documentation:**
- [Installation Guide](../getting-started/installation.md) - Setup issues
- [Commands Guide](../user-guide/commands.md) - Usage issues

**Community:**
- [GitHub Issues](https://github.com/agiletec-inc/airis-agent/issues)
- Include: OS, Python version, error message, steps to reproduce