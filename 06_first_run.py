"""Launch ComfyUI using the configured virtual environment."""

from __future__ import annotations

import sys

from utils import log_info, project_path, run


def main() -> None:
    comfy_root = project_path("ComfyUI")
    log_info("Starting ComfyUI. Press Ctrl+C to stop.")
    try:
        run([sys.executable, "main.py"], cwd=comfy_root, check=False)
    except KeyboardInterrupt:
        log_info("ComfyUI run interrupted by user.")


if __name__ == "__main__":
    main()
