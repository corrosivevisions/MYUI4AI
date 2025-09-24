"""Prepare the virtual environment and install PyTorch + dependencies."""

from __future__ import annotations

import os
import sys
from utils import (
    command_exists,
    is_macos,
    log_info,
    log_warning,
    project_path,
    run,
)


TORCH_CHANNEL_URLS = {
    "cuda": "https://download.pytorch.org/whl/cu121",
    "cpu": "https://download.pytorch.org/whl/cpu",
    "mps": None,
}


def select_torch_channel() -> str:
    forced = os.getenv("TORCH_CHANNEL")
    if forced:
        forced = forced.strip().lower()
        if forced in TORCH_CHANNEL_URLS:
            log_info(f"Using forced TORCH_CHANNEL setting: {forced}")
            return forced
        log_warning(f"Unknown TORCH_CHANNEL '{forced}'. Falling back to auto-detection.")

    if command_exists("nvidia-smi"):
        log_info("Detected NVIDIA GPU via nvidia-smi.")
        return "cuda"

    if is_macos():
        log_info("Detected macOS environment; using MPS wheels.")
        return "mps"

    return "cpu"


def pip(args: list[str]) -> None:
    run([sys.executable, "-m", "pip", *args])


def install_torch(channel: str) -> None:
    base_args = ["install", "--upgrade", "torch", "torchvision", "torchaudio"]
    index_url = TORCH_CHANNEL_URLS[channel]
    if index_url:
        base_args.extend(["--index-url", index_url])
    log_info(f"Installing PyTorch ({channel})...")
    pip(base_args)


def main() -> None:
    log_info("Upgrading pip, setuptools and wheel...")
    pip(["install", "--upgrade", "pip", "setuptools", "wheel"])

    channel = select_torch_channel()
    install_torch(channel)

    requirements = project_path("ComfyUI", "requirements.txt")
    if requirements.exists():
        log_info("Installing ComfyUI requirements...")
        pip(["install", "-r", str(requirements)])
    else:
        log_warning("ComfyUI requirements.txt not found; skipping requirement installation.")

    log_info("Installing additional helper packages...")
    pip(["install", "--upgrade", "huggingface_hub", "python-dotenv"])
    log_info("Virtual environment setup complete.")


if __name__ == "__main__":
    main()
