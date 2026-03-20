# Skill Closure

This repository is now set up as a repeatable local validation system instead of a loose notebook collection.

## What Was Closed

- Case discovery and metadata were normalized into `tools/cases.yaml`.
- Each case now runs in its own repo-local Conda prefix environment.
- Jupyter kernels are stored under `.jupyter/` instead of the global user profile.
- Public assets are prepared in deterministic local paths.
- Heavy notebooks run from prepared execution copies instead of mutating source notebooks.
- Execution logs, lock files, and status snapshots are written to `.reports/`.
- The remaining external blockers were removed, including the former Halo 4 Maya-only path.

## Reusable Workflow

1. Describe the matrix in `tools/cases.yaml`.
2. Keep dependency drift under control with a small set of template requirement files.
3. Create one environment per case under `.envs/<slug>`.
4. Execute notebooks from their own directories so relative paths keep working.
5. Use a prepared notebook copy when hidden precompute steps or workload reduction are needed.
6. Write status back to both the manifest and `.reports/status/`.
7. Regenerate the human-readable docs after the matrix changes.

## Concrete Fixes That Matter

- `lafan1` is fetched from a direct archive URL and unpacked into `resources/lafan1/bvh`.
- `run_case.ps1` uses repo-local Jupyter paths and env-local executables.
- `run_case.ps1` now skips Jupyter kernel registration for non-notebook cases.
- `run_case.ps1` now handles the Halo exporter as an executable script instead of an import-only check.
- `run_case.ps1` now generates a local synthetic Halo facial asset when requested by a case.
- `prepare_notebook.py` now contains execution-only rewrites for:
  - `motion_fields_for_interactive_character_animation`
  - `real_time_planning_for_parameterized_human_motion`
  - `knowing_when_to_put_your_foot_down`
- `motion_fields_for_interactive_character_animation` no longer depends on CUDA for automated validation.
- `motion_fields_for_interactive_character_animation` now defaults to CPU in auto mode because the benchmark dual-4090 machine was still faster on CPU end to end.
- `real_time_planning_for_parameterized_human_motion` now caps CPU parallelism through explicit worker and tree-job controls instead of letting nested parallelism overrun the machine.
- `Halo 4 exporter from maya.py` now works in two modes:
  - real Maya export when `maya.cmds` is available
  - synthetic fallback generation when Maya is unavailable

## Lessons Learned

- The real failure mode in notebook repositories is usually hidden runtime context, not Python syntax.
- Relative paths, generated `.dat` files, and widget-only cells need explicit handling.
- Treating external blockers as explicit state is better than silently skipping work.
- Prepared notebook copies are the cleanest place to turn on hidden precompute paths and scale down workloads for unattended validation.
- More hardware is not automatically better for notebook-style pipelines. In this repo, the best `motion_fields` result stayed on CPU, while `real_time_planning` improved only up to a bounded worker count.
- Script paths with spaces need special handling in Windows process launch code.
- A per-case env model is workable as long as dependencies are template-driven.

## Subagent Pattern

The useful split was:
- Main agent owns shared scripts, manifest changes, and docs.
- Side agents investigate isolated blockers such as missing assets or notebook-specific runtime assumptions.
- Workers should not edit shared manifest or docs in parallel with the main agent.

## Current End State

- Automated validation result: 26 passed, 0 failed, 0 blocked.
- Halo cases are no longer external blockers.
- Viewer notebooks still benefit from optional manual JupyterLab smoke checks when visual confirmation is required.
