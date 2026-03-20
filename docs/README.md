# AnimationTech Local Runbook

As of 2026-03-19, all 26 cases in this repository pass automated validation with repo-local environments.

Everything stays inside the repository:
- `.envs/` holds one Conda prefix environment per case.
- `.jupyter/` holds local kernels and Jupyter state.
- `.reports/` holds logs, executed notebooks, lock files, and status snapshots.
- `resources/` and `labs/AnimationPapers/animated_face.dat` hold downloaded or generated assets required by the cases.

## Quick Commands

Prepare public assets:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\prepare_assets.ps1
```

Run one case:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\run_case.ps1 <slug>
```

Re-run the full matrix:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\validate_all.ps1
```

Read the latest summary:

```powershell
Get-Content .\.reports\summary.json -Raw
```

## Execution Model

- Every case gets its own local Conda prefix environment.
- Notebook execution always runs from the notebook directory so relative paths resolve correctly.
- Source notebooks are never edited in place for automation. Execution-only changes are applied to prepared copies.
- Logs are written to `.reports/logs/<slug>.log`.
- Executed notebooks are written to `.reports/executed/<slug>/`.
- Resolved package versions are written to `.reports/locks/<slug>.txt`.

## Special Handling

- `lafan1` is downloaded into `resources/lafan1/bvh` from a direct public archive URL instead of relying on the original Git LFS path.
- `Motion Fields For Interactive Character Animation.ipynb` runs from a prepared copy with CPU fallback, smaller state ranges, lighter UMAP settings, reduced training epochs, and precompute enabled when the `.dat` file is missing.
- `Real-Time Planning for Parameterized Human Motion.ipynb` runs from a prepared copy that turns on the hidden precompute path and scales down the workload for unattended validation.
- `Knowing When To Put Your Foot Down.ipynb` runs from a prepared copy that trims the dataset window and skips purely interactive demo cells.
- `Halo 4 Facial Animation.ipynb` is unblocked by a local synthetic `animated_face.dat` generator when Maya-exported data is unavailable.
- `Halo 4 exporter from maya.py` now exports from Maya when available and otherwise falls back to the same synthetic asset generator for unattended validation.

## Training Hardware Guidance

- The benchmark machine for the training-heavy cases was `Ryzen 9 7950X / 64 GB RAM / 2 x RTX 4090`.
- `Motion Fields For Interactive Character Animation.ipynb` is CPU-preferred on this implementation. Even with CUDA-enabled PyTorch available, the measured adaptive profile was faster on CPU than on either GPU.
- `Real-Time Planning for Parameterized Human Motion.ipynb` is CPU-only and benefits from capped parallelism. The best measured adaptive profile used `12` workers on the 7950X; pushing past that caused regressions.
- The dual-GPU setup is currently useful for running separate cases in parallel, not for accelerating a single notebook end to end.

## Manual Smoke

All viewer-heavy notebooks now pass automated execution. A manual JupyterLab smoke pass is still recommended for interactive `ipyanimlab` notebooks if visual validation is required.
