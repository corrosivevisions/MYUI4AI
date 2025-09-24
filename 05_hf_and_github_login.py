"""Configure Git identity and Hugging Face authentication."""

from __future__ import annotations

import os
import sys
from getpass import getpass

from utils import log_info, log_warning, read_git_config, run, write_git_config


def ensure_git_identity() -> None:
    name = read_git_config("user.name")
    if name:
        log_info(f"Global git user.name is set to '{name}'.")
    else:
        name = input("Enter git user.name: ").strip()
        if name:
            write_git_config("user.name", name)
            log_info("Configured git user.name.")
        else:
            log_warning("git user.name not provided; leaving unset.")

    email = read_git_config("user.email")
    if email:
        log_info(f"Global git user.email is set to '{email}'.")
    else:
        email = input("Enter git user.email: ").strip()
        if email:
            write_git_config("user.email", email)
            log_info("Configured git user.email.")
        else:
            log_warning("git user.email not provided; leaving unset.")


def ensure_huggingface_login() -> None:
    token = os.getenv("HUGGINGFACE_TOKEN")
    if token:
        log_info("Using HUGGINGFACE_TOKEN environment variable.")
    else:
        token = getpass("Enter Hugging Face token (leave blank to skip): ").strip()
        if not token:
            log_info("No Hugging Face token provided. Skipping login.")
            return

    try:
        from huggingface_hub import login
    except ImportError:
        log_info("huggingface_hub not installed. Installing now...")
        run([sys.executable, "-m", "pip", "install", "--upgrade", "huggingface_hub"])
        from huggingface_hub import login

    log_info("Logging into Hugging Face...")
    login(token=token)
    log_info("Hugging Face authentication complete.")


def main() -> None:
    ensure_git_identity()
    ensure_huggingface_login()


if __name__ == "__main__":
    main()
