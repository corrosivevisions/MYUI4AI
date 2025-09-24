"""Create model directories and map them in ComfyUI."""

from __future__ import annotations

import os
from pathlib import Path

from utils import ensure_directory, log_info, log_warning, project_path


MODEL_FOLDERS = [
    "checkpoints",
    "vae",
    "clip",
    "controlnet",
    "lora",
    "ipadapter",
    "upscalers",
    "unet",
]


def determine_models_root() -> Path:
    env_path = os.getenv("COMFY_MODELS_DIR")
    if env_path:
        root = Path(env_path).expanduser().resolve()
        log_info(f"Using COMFY_MODELS_DIR override: {root}")
        return root
    root = project_path("models")
    log_info(f"Using default models directory: {root}")
    return root


def write_yaml(path: Path, mapping: dict[str, Path]) -> None:
    lines = []
    for key, target in mapping.items():
        lines.append(f"{key}:")
        lines.append(f"  - {target.as_posix()}")
    content = "\n".join(lines) + "\n"
    path.write_text(content, encoding="utf-8")


def main() -> None:
    models_root = determine_models_root()
    ensure_directory(models_root)

    mapping: dict[str, Path] = {}
    for folder in MODEL_FOLDERS:
        target = models_root / folder
        ensure_directory(target)
        mapping[folder] = target

    comfy_root = project_path("ComfyUI")
    if not comfy_root.exists():
        log_warning("ComfyUI directory not found. Run 01_clone_comfyui.py first.")
        return
    yaml_path = comfy_root / "extra_model_paths.yaml"

    if yaml_path.exists():
        log_info("extra_model_paths.yaml already exists. Skipping creation.")
        return

    log_info(f"Writing model mapping file at {yaml_path}...")
    write_yaml(yaml_path, mapping)
    log_info("Model directories configured.")


if __name__ == "__main__":
    main()
