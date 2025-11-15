"""
Super Agent CLI Main Entry Point

Provides command-line interface for Super Agent operations.
"""

import sys
from pathlib import Path

import click

# Add parent directory to path to import airis_agent
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from airis_agent import __version__


@click.group()
@click.version_option(version=__version__, prog_name="Super Agent")
def main():
    """
    Super Agent - AI-enhanced development framework for Claude Code

    A pytest plugin providing PM Agent capabilities and optional skills system.
    """
    pass


@main.command()
@click.argument("skill_name")
@click.option(
    "--target",
    default="~/.claude/skills",
    help="Installation directory (default: ~/.claude/skills)",
)
@click.option(
    "--force",
    is_flag=True,
    help="Force reinstall if skill already exists",
)
def install_skill(skill_name: str, target: str, force: bool):
    """
    Install a Super Agent skill to Claude Code

    SKILL_NAME: Name of the skill to install (e.g., pm-agent)

    Example:
        airis-agent install-skill pm-agent
        airis-agent install-skill pm-agent --target ~/.claude/skills --force
    """
    from .install_skill import install_skill_command

    target_path = Path(target).expanduser()

    click.echo(f"📦 Installing skill '{skill_name}' to {target_path}...")

    success, message = install_skill_command(
        skill_name=skill_name,
        target_path=target_path,
        force=force
    )

    if success:
        click.echo(f"✅ {message}")
    else:
        click.echo(f"❌ {message}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--verbose",
    is_flag=True,
    help="Show detailed diagnostic information",
)
def doctor(verbose: bool):
    """
    Check Super Agent installation health

    Verifies:
        - pytest plugin loaded correctly
        - Skills installed (if any)
        - Configuration files present
    """
    from .doctor import run_doctor

    click.echo("🔍 Super Agent Doctor\n")

    results = run_doctor(verbose=verbose)

    # Display results
    for check in results["checks"]:
        status_symbol = "✅" if check["passed"] else "❌"
        click.echo(f"{status_symbol} {check['name']}")

        if verbose and check.get("details"):
            for detail in check["details"]:
                click.echo(f"    {detail}")

    # Summary
    click.echo()
    total = len(results["checks"])
    passed = sum(1 for check in results["checks"] if check["passed"])

    if passed == total:
        click.echo("✅ Super Agent is healthy")
    else:
        click.echo(f"⚠️  {total - passed}/{total} checks failed")
        sys.exit(1)


@main.command()
def version():
    """Show Super Agent version"""
    click.echo(f"Super Agent version {__version__}")


@main.command(name="install-claude-plugin")
@click.option(
    "--settings-path",
    default="~/.claude/settings.json",
    help="Claude settings file (default: ~/.claude/settings.json)",
)
@click.option(
    "--marketplace-name",
    default="agiletec",
    show_default=True,
    help="Marketplace identifier to register",
)
@click.option(
    "--repo",
    default="agiletec-inc/airis-agent",
    show_default=True,
    help="GitHub repo Claude should treat as a marketplace",
)
@click.option(
    "--plugin-name",
    default="airis-agent",
    show_default=True,
    help="Plugin name to auto-enable",
)
def install_claude_plugin(settings_path: str, marketplace_name: str, repo: str, plugin_name: str):
    """Ensure Claude Code auto-installs the Airis Agent plugin."""

    from .install_plugin import ensure_airis_plugin

    changed, message = ensure_airis_plugin(
        Path(settings_path),
        marketplace_name=marketplace_name,
        repo=repo,
        plugin_name=plugin_name,
    )

    click.echo(message)
    if changed:
        click.echo("✅ Claude will prompt once to enable the marketplace plugin.")
    else:
        click.echo("ℹ️  Existing configuration already enables the plugin.")


@main.command(name="install-suite")
@click.option(
    "--base-dir",
    default="~/github",
    show_default=True,
    help="Directory where the OSS Airis Suite repositories should be cloned",
)
@click.option(
    "--update/--no-update",
    default=False,
    help="Pull latest changes for repositories that already exist",
)
@click.option(
    "--force",
    is_flag=True,
    help="Remove and reclone repositories that already exist",
)
@click.option(
    "--protocol",
    type=click.Choice(["ssh", "https"], case_sensitive=False),
    default="ssh",
    show_default=True,
    help="Protocol to use for cloning repositories",
)
def install_suite(base_dir: str, update: bool, force: bool, protocol: str):
    """Install or update the OSS Airis Suite repositories."""

    from .install_suite import install_airis_suite

    target_dir = Path(base_dir).expanduser()
    click.echo(f"📦 Installing Airis Suite into {target_dir}")

    results = install_airis_suite(
        target_dir,
        update_existing=update,
        force_reinstall=force,
        protocol=protocol.lower(),
    )

    symbols = {
        "cloned": "✅",
        "updated": "🔄",
        "exists": "ℹ️ ",
        "reinstalled": "♻️",
        "error": "❌",
    }

    had_error = False
    for result in results:
        status = result.get("status", "unknown")
        symbol = symbols.get(status, "•")
        message = result.get("message", "")
        click.echo(f"{symbol} {result['name']}: {message} [{result['path']}]")
        if status == "error":
            had_error = True

    if had_error:
        click.echo("❌ Some repositories failed to install. Review the errors above.")
        sys.exit(1)

    click.echo("\n✅ Airis Suite repositories are ready.")


if __name__ == "__main__":
    main()
