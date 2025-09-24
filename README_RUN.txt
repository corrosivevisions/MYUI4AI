ComfyUI Auto-Setup Kit
=======================

This repository provides a set of Python 3.11+ scripts that automatically
prepare ComfyUI with sensible defaults. Each script is idempotent: running them
multiple times will not duplicate work.

Prerequisites
-------------

* Python 3.11 or newer available on your PATH.
* Git available on your PATH.

Running the workflow
--------------------

To perform the entire setup in one go, run:

    python run_all.py

`run_all.py` will create (or reuse) a `.venv` virtual environment, clone or
update ComfyUI, install dependencies (including the appropriate PyTorch build),
prepare model directories, configure optional nodes, prompt for Git identity and
optionally log into Hugging Face. It finishes by launching ComfyUI.

Running individual steps
------------------------

You can also execute each step manually in the numbered order:

1. `python 00_env_check.py` – validate prerequisites and create `.venv`.
2. `python 01_clone_comfyui.py` – clone or update the ComfyUI repository.
3. `.venv/bin/python 02_setup_venv_and_torch.py` (or `.venv\Scripts\python.exe`
   on Windows) – upgrade pip tooling, install the appropriate PyTorch variant,
   ComfyUI requirements, `huggingface_hub`, and `python-dotenv`.
4. `.venv/bin/python 03_models_and_paths.py` – create the shared model folders
   and generate `extra_model_paths.yaml` if it does not exist.
5. `.venv/bin/python 04_install_manager_and_nodes.py` – install or update the
   ComfyUI-Manager extension and any enabled optional nodes.
6. `.venv/bin/python 05_hf_and_github_login.py` – ensure Git has your user name
   and email configured, and optionally log into Hugging Face using a token.
7. `.venv/bin/python 06_first_run.py` – start ComfyUI using the prepared
   environment. Stop it with `Ctrl+C` when you're ready.

Optional environment variables
------------------------------

* `TORCH_CHANNEL` – override the auto-detected PyTorch build. Valid values are
  `cuda`, `cpu`, and `mps`.
* `COMFY_MODELS_DIR` – set a custom location for the shared `models/` directory
  used by ComfyUI. If unset, a `models` folder is created in the project root.
* `HUGGINGFACE_TOKEN` – supply a Hugging Face token for non-interactive login.
  If unset, the login script prompts for a token and can be skipped.

Popular nodes configuration
---------------------------

Optional nodes managed by `04_install_manager_and_nodes.py` are configured via
`popular_nodes.json`. Each entry can be enabled by setting its `"enabled"`
property to `true` before running the script. Disabled entries are skipped.
