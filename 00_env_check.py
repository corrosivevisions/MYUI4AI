"""Environment pre-flight checks for the ComfyUI auto-setup kit."""

from __future__ import annotations

import subprocess
import sys
import venv

from utils import ensure_git_available, ensure_python_requirement, log_info, venv_path


MIN_VERSION = (3, 11)


def main() -> None:
    log_info("Running environment checks...")
    ensure_python_requirement(MIN_VERSION)
    ensure_git_available()

    log_info(f"Python version: {sys.version.split()[0]}")
    git_version = subprocess.run(
        ["git", "--version"], check=True, capture_output=True, text=True
    ).stdout.strip()
    log_info(f"{git_version}")

    venv_dir = venv_path()
    if venv_dir.exists():
        log_info(f"Virtual environment already present at {venv_dir}. Skipping creation.")
        return

    log_info(f"Creating virtual environment at {venv_dir}...")
    builder = venv.EnvBuilder(with_pip=True, clear=False, upgrade=False)
    builder.create(venv_dir)
    log_info("Virtual environment created successfully.")


if __name__ == "__main__":
    main()
