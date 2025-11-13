"""Repository indexing service."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_IGNORE = {
    ".git",
    ".venv",
    ".idea",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".claude",
    ".pytest_cache",
}


@dataclass
class RepoIndexRequest:
    repo_path: str
    mode: str = "full"  # full | update | quick
    include_docs: bool = True
    include_tests: bool = True
    max_entries: int = 10
    output_dir: Optional[str] = None


@dataclass
class RepoIndexResponse:
    markdown: str
    data: Dict[str, any]
    stats: Dict[str, any]
    output_paths: List[Path] = field(default_factory=list)


def generate_repo_index(request: RepoIndexRequest) -> RepoIndexResponse:
    root = Path(request.repo_path).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Repository path not found: {root}")

    files = _collect_files(root, request.mode)
    stats = {
        "repo": str(root),
        "total_files": len(files),
        "mode": request.mode,
    }

    categories = _summarize_categories(root, request)
    entry_points = _find_entry_points(root)
    docs = _find_docs(root) if request.include_docs else []
    tests = _find_tests(root) if request.include_tests else []
    configs = _find_configs(root)

    data = {
        "metadata": stats,
        "structure": categories,
        "entry_points": entry_points,
        "documentation": docs,
        "configuration": configs,
        "tests": tests,
    }

    markdown = _render_markdown(root.name, stats, data)
    outputs: List[Path] = []

    if request.output_dir:
        out_dir = Path(request.output_dir).expanduser().resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        md_path = out_dir / "PROJECT_INDEX.md"
        json_path = out_dir / "PROJECT_INDEX.json"
        md_path.write_text(markdown, encoding="utf-8")
        json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        outputs.extend([md_path, json_path])

    return RepoIndexResponse(markdown=markdown, data=data, stats=stats, output_paths=outputs)


def _collect_files(root: Path, mode: str) -> List[Path]:
    files: List[Path] = []
    max_depth = {"full": 6, "update": 4, "quick": 2}.get(mode, 6)

    for dirpath, dirnames, filenames in os.walk(root):
        depth = Path(dirpath).relative_to(root).parts
        if len(depth) > max_depth:
            dirnames[:] = []
            continue

        dirnames[:] = [d for d in dirnames if d not in DEFAULT_IGNORE]
        for filename in filenames:
            files.append(Path(dirpath) / filename)

    return files


def _summarize_categories(root: Path, request: RepoIndexRequest) -> List[Dict[str, any]]:
    categories = []
    for child in sorted(root.iterdir()):
        if child.name in DEFAULT_IGNORE:
            continue
        if child.is_dir():
            categories.append(
                {
                    "path": str(child.relative_to(root)),
                    "type": "dir",
                    "file_count": sum(1 for _ in child.rglob("*") if _.is_file()),
                }
            )
        else:
            categories.append(
                {
                    "path": str(child.relative_to(root)),
                    "type": "file",
                    "size": child.stat().st_size,
                }
            )
        if len(categories) >= request.max_entries:
            break
    return categories


def _find_entry_points(root: Path) -> List[Dict[str, str]]:
    patterns = ["main.py", "cli.py", "__main__.py", "manage.py", "index.ts", "index.js"]
    entries: List[Dict[str, str]] = []
    for pattern in patterns:
        for path in root.rglob(pattern):
            entries.append(
                {
                    "file": str(path.relative_to(root)),
                    "hint": _describe_entry(path),
                }
            )
    return entries


def _describe_entry(path: Path) -> str:
    name = path.name
    if name == "main.py":
        return "Python main entry"
    if name == "cli.py":
        return "CLI entry"
    if name == "__main__.py":
        return "Package entry"
    if name == "manage.py":
        return "Django management"
    if name.endswith(".ts"):
        return "TypeScript entry"
    if name.endswith(".js"):
        return "JavaScript entry"
    return "Entry point candidate"


def _find_docs(root: Path) -> List[str]:
    docs = []
    for name in ["README.md"]:
        for path in root.glob(name):
            docs.append(str(path.relative_to(root)))
    for path in root.glob("docs/**/*.md"):
        docs.append(str(path.relative_to(root)))
    return sorted(set(docs))


def _find_tests(root: Path) -> List[str]:
    tests = []
    for path in root.rglob("tests"):
        if path.is_dir():
            tests.append(str(path.relative_to(root)))
    for file in root.rglob("test_*.py"):
        tests.append(str(file.relative_to(root)))
    return sorted(set(tests))


def _find_configs(root: Path) -> List[str]:
    configs = []
    for pattern in ["*.toml", "*.yaml", "*.yml", "*.json"]:
        for path in root.glob(pattern):
            configs.append(str(path.relative_to(root)))
    for path in root.rglob("pyproject.toml"):
        configs.append(str(path.relative_to(root)))
    return sorted(set(configs))


def _render_markdown(repo_name: str, stats: Dict[str, any], data: Dict[str, any]) -> str:
    lines = [
        f"# Project Index: {repo_name}",
        "",
        f"- Total files: {stats['total_files']}",
        f"- Mode: {stats['mode']}",
        "",
        "## 📁 Structure Snapshot",
    ]
    for item in data["structure"]:
        if item["type"] == "dir":
            lines.append(f"- 📁 `{item['path']}` ({item['file_count']} files)")
        else:
            lines.append(f"- 📄 `{item['path']}` ({item['size']} bytes)")

    lines.extend(["", "## 🚀 Entry Points"])
    for entry in data["entry_points"]:
        lines.append(f"- `{entry['file']}` — {entry['hint']}")

    if docs := data["documentation"]:
        lines.extend(["", "## 📚 Documentation"])
        for doc in docs[:15]:
            lines.append(f"- `{doc}`")
        if len(docs) > 15:
            lines.append(f"- ... ({len(docs) - 15} more)")

    if configs := data["configuration"]:
        lines.extend(["", "## ⚙️ Configuration"])
        for cfg in configs[:15]:
            lines.append(f"- `{cfg}`")
        if len(configs) > 15:
            lines.append(f"- ... ({len(configs) - 15} more)")

    if tests := data["tests"]:
        lines.extend(["", "## 🧪 Tests"])
        for test in tests[:15]:
            lines.append(f"- `{test}`")
        if len(tests) > 15:
            lines.append(f"- ... ({len(tests) - 15} more)")

    lines.append("")
    return "\n".join(lines)

