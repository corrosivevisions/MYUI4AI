"""Utility helpers for the ComfyUI auto-setup kit.

This module centralises logging, subprocess execution and a handful of
cross-platform helpers shared by the setup scripts.
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Mapping, Optional, Sequence


PROJECT_ROOT = Path(__file__).resolve().parent


def _log(prefix: str, message: str) -> None:
    print(f"[{prefix}] {message}")


def log_info(message: str) -> None:
    _log("INFO", message)


def log_warning(message: str) -> None:
    _log("WARN", message)


def log_error(message: str) -> None:
    _log("ERROR", message)


class RunError(RuntimeError):
    """Raised when a subprocess exits with a non-zero return code."""


def run(
    cmd: Sequence[str] | str,
    cwd: Optional[Path | str] = None,
    env: Optional[Mapping[str, str]] = None,
    check: bool = True,
) -> int:
    """Run a command, streaming stdout/stderr to the console.

    Args:
        cmd: Command and arguments. If a string is provided it is executed
            through the platform shell.
        cwd: Optional working directory.
        env: Optional environment variables to pass to the command.
        check: Whether to raise :class:`RunError` on non-zero exit status.

    Returns:
        The command's return code.
    """

    shell = isinstance(cmd, str)
    process = subprocess.Popen(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=dict(env) if env else None,
        shell=shell,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    assert process.stdout is not None
    for line in process.stdout:
        print(line.rstrip())

    return_code = process.wait()
    if check and return_code != 0:
        raise RunError(f"Command {cmd!r} failed with exit code {return_code}")
    return return_code


def detect_os() -> str:
    return platform.system().lower()


def is_windows() -> bool:
    return detect_os().startswith("win")


def is_macos() -> bool:
    return detect_os() == "darwin"


def is_linux() -> bool:
    return detect_os() == "linux"


def project_path(*parts: str | os.PathLike[str]) -> Path:
    return PROJECT_ROOT.joinpath(*parts)


def venv_path() -> Path:
    return project_path(".venv")


def venv_python() -> Path:
    base = venv_path()
    if is_windows():
        candidate = base / "Scripts" / "python.exe"
    else:
        candidate = base / "bin" / "python"
    return candidate


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def python_meets_requirement(min_version: tuple[int, int]) -> bool:
    return sys.version_info >= min_version


def ensure_python_requirement(min_version: tuple[int, int]) -> None:
    if not python_meets_requirement(min_version):
        version = ".".join(str(part) for part in sys.version_info[:3])
        raise RuntimeError(
            f"Python {min_version[0]}.{min_version[1]} or newer is required. "
            f"Detected {version}."
        )


def ensure_git_available() -> None:
    if shutil.which("git") is None:
        raise RuntimeError("Git must be available on PATH to continue.")


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def read_git_config(key: str) -> str:
    try:
        result = subprocess.run(
            ["git", "config", "--global", key],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def write_git_config(key: str, value: str) -> None:
    run(["git", "config", "--global", key, value])


def read_json(path: Path) -> list[dict[str, object]]:
    import json

    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)

