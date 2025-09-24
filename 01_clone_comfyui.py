"""Clone or update the ComfyUI repository."""

from __future__ import annotations

from utils import log_info, project_path, run


REPO_URL = "https://github.com/comfyanonymous/ComfyUI.git"
TARGET_DIR = project_path("ComfyUI")


def main() -> None:
    if TARGET_DIR.exists():
        log_info("ComfyUI repository already exists. Pulling latest changes...")
        run(["git", "pull"], cwd=TARGET_DIR)
    else:
        log_info("Cloning ComfyUI repository...")
        run(["git", "clone", REPO_URL, str(TARGET_DIR)])
    log_info("ComfyUI repository is up to date.")


if __name__ == "__main__":
    main()
