from pathlib import Path

from airis_agent.api.repo_index import RepoIndexRequest, generate_repo_index


def test_generate_repo_index_quick(tmp_path):
    repo_path = Path(__file__).resolve().parents[2]
    request = RepoIndexRequest(
        repo_path=str(repo_path),
        mode="quick",
        output_dir=str(tmp_path),
    )

    response = generate_repo_index(request)

    assert response.markdown.startswith("# Project Index")
    assert response.stats["total_files"] > 0
    assert response.output_paths  # PROJECT_INDEX files written
