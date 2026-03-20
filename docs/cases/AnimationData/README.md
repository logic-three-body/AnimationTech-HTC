# AnimationData Case Notes

This document records the local environment mapping and startup flow for the case named `AnimationData`.

In this repository, `AnimationData` maps to the automated case slug `animation_format`.

## Case Mapping

| Item | Value |
| --- | --- |
| Case alias used in docs | `AnimationData` |
| Case slug in automation | `animation_format` |
| Source notebook | `labs/AnimationPapers/Animation Format.ipynb` |
| Notebook family | `Animation Papers` |
| Template requirements | `tools/templates/papers-core.txt` |
| Validation mode | `manual_smoke` |
| Latest verified automated status | `passed` |
| Latest verified status snapshot | `.reports/status/animation_format.json` |

As verified locally on 2026-03-20, automated execution passed and the repo still marks this case as requiring a manual JupyterLab smoke check for visual confirmation.

## Environment Mapping

| Concern | Path / Value |
| --- | --- |
| Conda prefix environment | `.envs/animation_format` |
| Python executable | `.envs/animation_format/python.exe` |
| Registered kernel name | `animationtech-animation_format` |
| Kernel display name | `AnimationTech (animation_format)` |
| Kernel spec | `.jupyter/share/jupyter/kernels/animationtech-animation_format/kernel.json` |
| Local Jupyter root | `.jupyter/` |
| Prepared execution notebook | `labs/AnimationPapers/.animationtech_prepared_animation_format.ipynb` |
| Executed notebook output | `.reports/executed/animation_format/animation_format.ipynb` |
| Execution log | `.reports/logs/animation_format.log` |
| Lock file | `.reports/locks/animation_format.txt` |
| Status snapshot | `.reports/status/animation_format.json` |

## Assets And Runtime Inputs

| Type | Source |
| --- | --- |
| BVH dataset | `resources/lafan1/bvh` |
| Character / viewer assets | `ipyanimlab` package assets |
| Notebook working directory during execution | `labs/AnimationPapers` |

The runner prepares `lafan1` automatically through `tools/prepare_assets.ps1` when the asset is missing.

## Template Package Baseline

The `papers-core` template installs these baseline packages:

- `numpy`
- `scipy`
- `scikit-learn`
- `matplotlib`
- `ipympl`
- `ipywidgets`
- `ipycanvas`
- `jupyterlab`
- `nbconvert`
- `nbclient`
- `ipykernel`
- `ipyanimlab==1.2.1`
- `ipywebgl`
- `usd-core`

The resolved environment for this case is captured in `.reports/locks/animation_format.txt`. The local verification run used Python `3.10.20`.

## Startup Flow

### 1. Optional asset preparation

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\prepare_assets.ps1
```

### 2. Standard automated execution

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\run_case.ps1 animation_format
```

This step will:

1. Ensure `resources/lafan1/bvh` is present.
2. Ensure `.envs/animation_format` exists.
3. Install the `papers-core` template packages when needed.
4. Register the local kernel `animationtech-animation_format`.
5. Generate the prepared execution copy.
6. Execute the notebook with `nbconvert`.
7. Write logs, lock data, executed notebook output, and status snapshots.

### 3. Interactive JupyterLab launch

Use the case-local environment and the repo-local Jupyter directories:

```powershell
$env:JUPYTER_CONFIG_DIR = "$PWD\.jupyter\config"
$env:JUPYTER_DATA_DIR = "$PWD\.jupyter"
$env:JUPYTER_PATH = "$PWD\.jupyter\share\jupyter"
$env:IPYTHONDIR = "$PWD\.jupyter\ipython"

& "$PWD\.envs\animation_format\Scripts\jupyter-lab.exe" `
  --no-browser `
  --ServerApp.root_dir="$PWD" `
  --ServerApp.preferred_dir="$PWD\labs\AnimationPapers"
```

After the server starts, query the access URL and token with:

```powershell
& "$PWD\.envs\animation_format\Scripts\jupyter.exe" server list
```

Then open:

- `labs/AnimationPapers/Animation Format.ipynb`

If Jupyter does not auto-select the case kernel, switch to:

- `AnimationTech (animation_format)`

### Preview Recommendation

For this case, use browser JupyterLab as the primary interactive preview surface.

- Recommended: browser JupyterLab
- Acceptable: VSCode for editing and non-widget code execution
- Not recommended for final preview: VSCode notebook widget rendering for `ipyanimlab` / `ipywebgl`

## What To Check After Startup

- The notebook opens from `labs/AnimationPapers/Animation Format.ipynb`.
- The kernel is `AnimationTech (animation_format)`.
- The viewer cells render without missing asset errors.
- The animation data load cell can read `../../resources/lafan1/bvh/aiming1_subject1.bvh`.
- The latest automated status remains `passed` in `.reports/status/animation_format.json`.
