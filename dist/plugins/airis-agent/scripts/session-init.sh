#!/bin/bash
# Airis Agent SessionStart initialization script
# Auto-executed when Claude Code session starts

# 1. Check git status
if git status --porcelain > /dev/null 2>&1; then
    status=$(git status --porcelain)
    if [ -z "$status" ]; then
        echo "📊 Git: clean"
    else
        count=$(echo "$status" | wc -l | tr -d ' ')
        echo "📊 Git: ${count} files"
    fi
else
    echo "📊 Git: not a repo"
fi

# 2. CLAUDE.md optimization check
if [ -f "CLAUDE.md" ]; then
    lines=$(wc -l < CLAUDE.md | tr -d ' ')

    if [ "$lines" -gt 200 ]; then
        echo "⚠️  CLAUDE.md: ${lines} lines (推奨: 100-200)"
        echo "   💡 Optimize with: /init"
        echo "      (Re-analyzes codebase and refreshes CLAUDE.md)"
    elif [ "$lines" -gt 100 ]; then
        echo "✅ CLAUDE.md: ${lines} lines (適切な範囲)"
    else
        echo "📝 CLAUDE.md: ${lines} lines (良好)"
    fi
else
    echo "📝 CLAUDE.md: not found"
fi

# 3. PROJECT_INDEX.md freshness check
if [ -f "PROJECT_INDEX.md" ]; then
    # Cross-platform date check (macOS and Linux)
    if stat -f '%Sm' -t '%s' PROJECT_INDEX.md > /dev/null 2>&1; then
        # macOS
        index_date=$(stat -f '%Sm' -t '%s' PROJECT_INDEX.md)
    else
        # Linux
        index_date=$(stat -c '%Y' PROJECT_INDEX.md)
    fi

    current_date=$(date +%s)
    days_old=$(( (current_date - index_date) / 86400 ))

    if [ "$days_old" -gt 7 ]; then
        echo "⚠️  PROJECT_INDEX.md: ${days_old} days old (stale)"
        echo "   💡 Regenerate with: /airis-agent:index-repo"
    else
        echo "📦 PROJECT_INDEX.md: ${days_old} days old (fresh)"
    fi
else
    echo "📦 PROJECT_INDEX.md: not found"
    echo "   💡 Generate with: /airis-agent:index-repo"
fi

# 4. Context restoration from docs/memory/
if [ -d "docs/memory" ]; then
    echo "📂 Context available: docs/memory/"

    # Check next_actions.md
    if [ -f "docs/memory/next_actions.md" ]; then
        echo "📋 Next actions:"
        head -5 docs/memory/next_actions.md | sed 's/^/   /'
    fi

    # Check last_session.md
    if [ -f "docs/memory/last_session.md" ]; then
        if stat -f '%Sm' -t '%Y-%m-%d' docs/memory/last_session.md > /dev/null 2>&1; then
            # macOS
            last_date=$(stat -f '%Sm' -t '%Y-%m-%d' docs/memory/last_session.md)
        else
            # Linux
            last_date=$(stat -c '%y' docs/memory/last_session.md | cut -d' ' -f1)
        fi
        echo "🕐 Last session: ${last_date}"
    fi
fi

# 5. Remind token budget
echo ""
echo "💡 Use /context to monitor token usage."

# 6. Report core services
echo ""
echo "🛠️  Core Services Available:"
echo "  ✅ Confidence Check (pre-implementation validation)"
echo "  ✅ Deep Research (web/MCP integration)"
echo "  ✅ Repository Index (token-efficient exploration)"
echo ""
echo "Airis Agent ready — awaiting task assignment."

exit 0
