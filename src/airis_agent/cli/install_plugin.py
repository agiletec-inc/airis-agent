"""Helpers for configuring Claude Code to auto-install the Airis Agent plugin."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Tuple

DEFAULT_SETTINGS_PATH = Path("~/.claude/settings.json").expanduser()
DEFAULT_MARKETPLACE_NAME = "agiletec"
DEFAULT_REPO = "agiletec-inc/airis-agent"
DEFAULT_PLUGIN_NAME = "airis-agent"


def _load_settings(settings_path: Path) -> dict[str, Any]:
    if not settings_path.exists():
        return {}

    content = settings_path.read_text().strip()
    if not content:
        return {}
    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError(f"Invalid JSON in {settings_path}: {exc}") from exc


def ensure_airis_plugin(
    settings_path: Path = DEFAULT_SETTINGS_PATH,
    marketplace_name: str = DEFAULT_MARKETPLACE_NAME,
    repo: str = DEFAULT_REPO,
    plugin_name: str = DEFAULT_PLUGIN_NAME,
) -> Tuple[bool, str]:
    """Ensure Claude settings auto-enable the Airis Agent marketplace plugin."""

    settings_path = settings_path.expanduser()
    settings = _load_settings(settings_path)
    changed = False

    extra = settings.setdefault("extraKnownMarketplaces", {})
    expected_marketplace = {"source": {"source": "github", "repo": repo}}

    if extra.get(marketplace_name) != expected_marketplace:
        extra[marketplace_name] = expected_marketplace
        changed = True

    enabled = settings.setdefault("enabledPlugins", [])
    if not isinstance(enabled, list):
        raise ValueError("enabledPlugins must be a list in Claude settings.")

    plugin_identifier = f"{plugin_name}@{marketplace_name}"
    if plugin_identifier not in enabled:
        enabled.append(plugin_identifier)
        changed = True

    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")

    if changed:
        return True, f"Updated {settings_path} with marketplace '{marketplace_name}' and plugin '{plugin_identifier}'."
    return False, f"No changes needed; '{plugin_identifier}' already configured in {settings_path}."


__all__ = ["ensure_airis_plugin"]
