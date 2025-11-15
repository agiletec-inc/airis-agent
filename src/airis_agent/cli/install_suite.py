"""Utility helpers to install the OSS Airis Suite repositories."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

DEFAULT_BASE_DIR = Path("~/github").expanduser()


@dataclass(frozen=True)
class SuiteRepo:
    """Metadata describing an Airis Suite repository."""

    name: str
    slug: str
    branch: str = "main"

    @property
    def target_dir(self) -> str:
        return self.name

    def get_url(self, protocol: str) -> str:
        if protocol == "ssh":
            return f"git@github.com:{self.slug}.git"
        if protocol == "https":
            return f"https://github.com/{self.slug}.git"
        raise ValueError(f"Unsupported protocol '{protocol}'")


DEFAULT_SUITE_REPOS: tuple[SuiteRepo, ...] = (
    SuiteRepo("airis-mcp-gateway", "agiletec-inc/airis-mcp-gateway"),
    SuiteRepo("airis-workspace", "agiletec-inc/airis-workspace"),
    SuiteRepo("airiscode", "agiletec-inc/airiscode"),
    SuiteRepo("mindbase", "agiletec-inc/mindbase"),
)


class SuiteInstallError(RuntimeError):
    """Raised when git commands fail while installing the suite."""


def _run_git_command(args: list[str], cwd: Path | None = None) -> None:
    """Execute a git command and raise SuiteInstallError on failure."""

    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        message = stderr or stdout or "Unknown git error"
        raise SuiteInstallError(f"git {' '.join(args)} failed: {message}")


def _clone_repo(repo: SuiteRepo, dest: Path, protocol: str) -> None:
    url = repo.get_url(protocol)
    args = ["clone", url, str(dest)]
    if repo.branch:
        args.insert(1, "--branch")
        args.insert(2, repo.branch)
    _run_git_command(args)


def _update_repo(dest: Path) -> None:
    _run_git_command(["pull", "--ff-only"], cwd=dest)


def install_airis_suite(
    base_dir: Path = DEFAULT_BASE_DIR,
    *,
    repos: Iterable[SuiteRepo] | None = None,
    update_existing: bool = False,
    force_reinstall: bool = False,
    protocol: str = "ssh",
) -> List[dict[str, str]]:
    """Install or update the OSS Airis Suite repositories.

    Args:
        base_dir: The directory that should contain all cloned repositories.
        repos: Optional custom iterable of SuiteRepo definitions.
        update_existing: If True, `git pull --ff-only` is executed for repos that already exist.
        force_reinstall: If True, existing directories are removed before cloning.

    Returns:
        A list of status dictionaries per repository:
        {"name": str, "status": str, "path": str, "message": str}
    """

    repo_list = tuple(repos) if repos is not None else DEFAULT_SUITE_REPOS
    if protocol not in {"ssh", "https"}:
        raise ValueError("protocol must be 'ssh' or 'https'")

    base_dir = base_dir.expanduser()
    base_dir.mkdir(parents=True, exist_ok=True)

    results: List[dict[str, str]] = []

    for repo in repo_list:
        target = base_dir / repo.target_dir
        status: dict[str, str] = {"name": repo.name, "path": str(target)}

        try:
            if target.exists():
                if force_reinstall:
                    shutil.rmtree(target)
                    _clone_repo(repo, target, protocol)
                    status["status"] = "reinstalled"
                    status["message"] = "Removed existing directory and cloned again"
                elif update_existing:
                    _update_repo(target)
                    status["status"] = "updated"
                    status["message"] = "Repository already existed; pulled latest changes"
                else:
                    status["status"] = "exists"
                    status["message"] = "Repository already exists; skipped"
            else:
                _clone_repo(repo, target, protocol)
                status["status"] = "cloned"
                status["message"] = "Repository cloned"
        except SuiteInstallError as exc:
            status["status"] = "error"
            status["message"] = str(exc)

        results.append(status)

    return results


__all__ = [
    "DEFAULT_BASE_DIR",
    "DEFAULT_SUITE_REPOS",
    "SuiteRepo",
    "SuiteInstallError",
    "install_airis_suite",
]
