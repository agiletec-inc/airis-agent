"""
Super Agent CLI Main Entry Point

Provides command-line interface for Super Agent operations.
"""

import sys
from pathlib import Path

import click

# Add parent directory to path to import airis_agent
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from superagent import __version__


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
        superagent install-skill pm-agent
        superagent install-skill pm-agent --target ~/.claude/skills --force
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


if __name__ == "__main__":
    main()
