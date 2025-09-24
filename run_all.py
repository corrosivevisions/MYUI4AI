"""Run the complete ComfyUI auto-setup workflow."""

from __future__ import annotations

import sys

from utils import log_info, run, venv_python


SYSTEM_SCRIPTS = ["00_env_check.py", "01_clone_comfyui.py"]
VENV_SCRIPTS = [
    "02_setup_venv_and_torch.py",
    "03_models_and_paths.py",
    "04_install_manager_and_nodes.py",
    "05_hf_and_github_login.py",
    "06_first_run.py",
]


def run_with_python(python: str, script: str) -> None:
    log_info(f"Running {script} with {python}...")
    run([python, script])


def main() -> None:
    system_python = sys.executable
    for script in SYSTEM_SCRIPTS:
        run_with_python(system_python, script)

    venv_python_path = venv_python()
    if not venv_python_path.exists():
        raise RuntimeError(
            "Virtual environment Python interpreter not found. "
            "Did 00_env_check.py run successfully?"
        )

    for script in VENV_SCRIPTS:
        run_with_python(str(venv_python_path), script)


if __name__ == "__main__":
    main()
