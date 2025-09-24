"""Install ComfyUI-Manager and optional custom nodes."""

from __future__ import annotations

from pathlib import Path

from utils import ensure_directory, log_info, log_warning, project_path, read_json, run


MANAGER_REPO = "https://github.com/ltdrdata/ComfyUI-Manager.git"


def ensure_repo(path: Path, repo: str) -> None:
    if path.exists():
        log_info(f"Updating repository in {path}...")
        run(["git", "pull"], cwd=path)
    else:
        log_info(f"Cloning {repo} into {path}...")
        run(["git", "clone", repo, str(path)])


def main() -> None:
    comfy_root = project_path("ComfyUI")
    custom_nodes = comfy_root / "custom_nodes"
    ensure_directory(custom_nodes)

    manager_path = custom_nodes / "ComfyUI-Manager"
    ensure_repo(manager_path, MANAGER_REPO)

    config_path = project_path("popular_nodes.json")
    if not config_path.exists():
        log_warning("popular_nodes.json not found; skipping optional nodes.")
        return

    entries = read_json(config_path)
    if not entries:
        log_info("No optional nodes enabled.")
        return

    for entry in entries:
        name = str(entry.get("name", "")).strip()
        repo = str(entry.get("repo", "")).strip()
        enabled = bool(entry.get("enabled", False))

        if not name or not repo:
            log_warning(f"Skipping malformed entry: {entry}")
            continue

        if not enabled:
            log_info(f"Node '{name}' is disabled. Skipping.")
            continue

        target = custom_nodes / name
        ensure_repo(target, repo)


if __name__ == "__main__":
    main()
