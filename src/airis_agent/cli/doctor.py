"""
Super Agent Doctor Command

Health check for Super Agent installation.
"""

from pathlib import Path
from typing import Any, Dict


def run_doctor(verbose: bool = False) -> Dict[str, Any]:
    """
    Run Super Agent health checks

    Args:
        verbose: Include detailed diagnostic information

    Returns:
        Dict with check results
    """
    checks = []

    # Check 1: pytest plugin loaded
    plugin_check = _check_pytest_plugin()
    checks.append(plugin_check)

    # Check 2: Skills installed
    skills_check = _check_skills_installed()
    checks.append(skills_check)

    # Check 3: Configuration
    config_check = _check_configuration()
    checks.append(config_check)

    return {
        "checks": checks,
        "passed": all(check["passed"] for check in checks),
    }


def _check_pytest_plugin() -> Dict[str, Any]:
    """
    Check if pytest plugin is loaded

    Returns:
        Check result dict
    """
    try:
        import pytest

        # Try to get pytest config
        try:
            config = pytest.Config.fromdictargs({}, [])
            plugins = config.pluginmanager.list_plugin_distinfo()

            # Check if superagent plugin is loaded
            superagent_loaded = any(
                "airis-agent" in str(plugin[0]).lower()
                for plugin in plugins
            )

            if superagent_loaded:
                return {
                    "name": "pytest plugin loaded",
                    "passed": True,
                    "details": ["Super Agent pytest plugin is active"],
                }
            else:
                return {
                    "name": "pytest plugin loaded",
                    "passed": False,
                    "details": ["Super Agent plugin not found in pytest plugins"],
                }
        except Exception as e:
            return {
                "name": "pytest plugin loaded",
                "passed": False,
                "details": [f"Could not check pytest plugins: {e}"],
            }

    except ImportError:
        return {
            "name": "pytest plugin loaded",
            "passed": False,
            "details": ["pytest not installed"],
        }


def _check_skills_installed() -> Dict[str, Any]:
    """
    Check if any skills are installed

    Returns:
        Check result dict
    """
    skills_dir = Path("~/.claude/skills").expanduser()

    if not skills_dir.exists():
        return {
            "name": "Skills installed",
            "passed": True,  # Optional, so pass
            "details": ["No skills installed (optional)"],
        }

    # Find skills (directories with implementation.md)
    skills = []
    for item in skills_dir.iterdir():
        if item.is_dir() and (item / "implementation.md").exists():
            skills.append(item.name)

    if skills:
        return {
            "name": "Skills installed",
            "passed": True,
            "details": [f"{len(skills)} skill(s) installed: {', '.join(skills)}"],
        }
    else:
        return {
            "name": "Skills installed",
            "passed": True,  # Optional
            "details": ["No skills installed (optional)"],
        }


def _check_configuration() -> Dict[str, Any]:
    """
    Check Super Agent configuration

    Returns:
        Check result dict
    """
    # Check if package is importable
    try:
        import airis_agent
        version = superagent.__version__

        return {
            "name": "Configuration",
            "passed": True,
            "details": [f"Super Agent {version} installed correctly"],
        }
    except ImportError as e:
        return {
            "name": "Configuration",
            "passed": False,
            "details": [f"Could not import airis_agent: {e}"],
        }
