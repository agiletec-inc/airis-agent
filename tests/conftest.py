"""
Pytest Configuration for Super Agent Tests

Provides fixtures and configuration for all test modules.
The Super Agent pytest plugin is auto-loaded via entry points.
"""

from pathlib import Path
from typing import Generator

import pytest

# ============================================================================
# Super Agent pytest plugin auto-loads these fixtures:
# - confidence_checker
# - self_check_protocol
# - reflexion_pattern
# - token_budget
# - pm_context
# ============================================================================


@pytest.fixture
def project_root() -> Path:
    """Return project root directory"""
    return Path(__file__).parent.parent


@pytest.fixture
def test_data_dir(project_root: Path) -> Path:
    """Return test data directory"""
    return project_root / "tests" / "data"


@pytest.fixture
def temp_repo(tmp_path: Path) -> Generator[Path, None, None]:
    """Create temporary repository for testing"""
    repo_dir = tmp_path / "test_repo"
    repo_dir.mkdir()

    # Initialize git repo
    import subprocess
    subprocess.run(["git", "init"], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=repo_dir,
        check=True,
        capture_output=True
    )
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo_dir,
        check=True,
        capture_output=True
    )

    yield repo_dir


@pytest.fixture
def mock_mindbase_available() -> bool:
    """Mock mindbase availability"""
    return True


@pytest.fixture
def mock_mindbase_unavailable() -> bool:
    """Mock mindbase unavailability (fallback mode)"""
    return False
