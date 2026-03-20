import argparse
import json
from pathlib import Path


MOTION_FIELDS_SLUG = "motion_fields_for_interactive_character_animation"
REALTIME_PLANNING_SLUG = "real_time_planning_for_parameterized_human_motion"
KNOWING_FOOT_DOWN_SLUG = "knowing_when_to_put_your_foot_down"


def get_motion_fields_settings(training_profile: str, torch_device: str) -> dict:
    use_gpu = torch_device.startswith("cuda")
    profiles = {
        "validate": {
            "umap_neighbors": 20,
            "state_ranges": {
                "add_states(2, slice(100,2800))\n": "add_states(2, slice(100,260))\n",
                "add_states(15, slice(1200,1800))\n": "add_states(15, slice(1200,1260))\n",
                "add_states(15, slice(3450,3860))\n": "add_states(15, slice(3450,3510))\n",
                "add_states(14, slice(180,800))\n": "add_states(14, slice(180,240))\n",
                "add_states(13, slice(200,2300))\n": "add_states(13, slice(200,320))\n",
            },
            "k_neighbors": 6,
            "theta_count": 9,
            "epoch": 20,
        },
        "adaptive_cpu": {
            "umap_neighbors": 30,
            "state_ranges": {
                "add_states(2, slice(100,2800))\n": "add_states(2, slice(100,500))\n",
                "add_states(15, slice(1200,1800))\n": "add_states(15, slice(1200,1320))\n",
                "add_states(15, slice(3450,3860))\n": "add_states(15, slice(3450,3570))\n",
                "add_states(14, slice(180,800))\n": "add_states(14, slice(180,320))\n",
                "add_states(13, slice(200,2300))\n": "add_states(13, slice(200,520))\n",
            },
            "k_neighbors": 8,
            "theta_count": 13,
            "epoch": 35,
        },
        "adaptive_gpu": {
            "umap_neighbors": 40,
            "state_ranges": {
                "add_states(2, slice(100,2800))\n": "add_states(2, slice(100,900))\n",
                "add_states(15, slice(1200,1800))\n": "add_states(15, slice(1200,1500))\n",
                "add_states(15, slice(3450,3860))\n": "add_states(15, slice(3450,3690))\n",
                "add_states(14, slice(180,800))\n": "add_states(14, slice(180,500))\n",
                "add_states(13, slice(200,2300))\n": "add_states(13, slice(200,900))\n",
            },
            "k_neighbors": 10,
            "theta_count": 17,
            "epoch": 80,
        },
        "quality_cpu": {
            "umap_neighbors": 45,
            "state_ranges": {
                "add_states(2, slice(100,2800))\n": "add_states(2, slice(100,1200))\n",
                "add_states(15, slice(1200,1800))\n": "add_states(15, slice(1200,1560))\n",
                "add_states(15, slice(3450,3860))\n": "add_states(15, slice(3450,3750))\n",
                "add_states(14, slice(180,800))\n": "add_states(14, slice(180,620))\n",
                "add_states(13, slice(200,2300))\n": "add_states(13, slice(200,1200))\n",
            },
            "k_neighbors": 10,
            "theta_count": 17,
            "epoch": 60,
        },
        "quality_gpu": {
            "umap_neighbors": 60,
            "state_ranges": {
                "add_states(2, slice(100,2800))\n": "add_states(2, slice(100,1800))\n",
                "add_states(15, slice(1200,1800))\n": "add_states(15, slice(1200,1700))\n",
                "add_states(15, slice(3450,3860))\n": "add_states(15, slice(3450,3820))\n",
                "add_states(14, slice(180,800))\n": "add_states(14, slice(180,720))\n",
                "add_states(13, slice(200,2300))\n": "add_states(13, slice(200,1800))\n",
            },
            "k_neighbors": 12,
            "theta_count": 17,
            "epoch": 120,
        },
    }

    if training_profile == "quality":
        return profiles["quality_gpu" if use_gpu else "quality_cpu"]
    if training_profile == "adaptive":
        return profiles["adaptive_gpu" if use_gpu else "adaptive_cpu"]
    return profiles["validate"]


def get_realtime_planning_settings(training_profile: str) -> dict:
    profiles = {
        "validate": {
            "replacements": [
                ("X = np.zeros([CLIP_COUNT, 100000])", "X = np.zeros([CLIP_COUNT, 20000])"),
                ("y = np.zeros([CLIP_COUNT, 100000])", "y = np.zeros([CLIP_COUNT, 20000])"),
                ("for path in range(800):", "for path in range(80):"),
                ("residuals = np.zeros([CLIP_COUNT * 100000])", "residuals = np.zeros([CLIP_COUNT * 20000])"),
                ("pre_compute_table_x = np.linspace(-1000, 1000, 1001)", "pre_compute_table_x = np.linspace(-300, 300, 201)"),
                ("pre_compute_table_z = np.linspace(-1000, 1000, 1001)", "pre_compute_table_z = np.linspace(-300, 300, 201)"),
                ("all_valid_states = np.zeros([1000000000, 4], dtype=np.float32)", "all_valid_states = np.zeros([300000, 4], dtype=np.float32)"),
                ("all_valid_states = np.zeros([100000000, 4], dtype=np.float32)", "all_valid_states = np.zeros([200000, 4], dtype=np.float32)"),
                ("for _ in range(100):", "for _ in range(5):"),
                ("EPOCH = 50", "EPOCH = 6"),
                ("RESTART_EPOCH = 10", "RESTART_EPOCH = 3"),
                ("for _ in range(20):", "for _ in range(2):"),
                ("EPOCH = 15", "EPOCH = 4"),
                ("RESTART_EPOCH = 100", "RESTART_EPOCH = 4"),
                ("clip_index = np.zeros([GROUP_VALUE_COUNT, 100000], dtype=np.uint32)", "clip_index = np.zeros([GROUP_VALUE_COUNT, 15000], dtype=np.uint32)"),
                ("X = np.zeros([GROUP_VALUE_COUNT, 100000, 2])", "X = np.zeros([GROUP_VALUE_COUNT, 15000, 2])"),
                ("y = np.zeros([GROUP_VALUE_COUNT, 100000])", "y = np.zeros([GROUP_VALUE_COUNT, 15000])"),
                ("dist = 500", "dist = 200"),
            ],
        },
        "adaptive": {
            "replacements": [
                ("X = np.zeros([CLIP_COUNT, 100000])", "X = np.zeros([CLIP_COUNT, 40000])"),
                ("y = np.zeros([CLIP_COUNT, 100000])", "y = np.zeros([CLIP_COUNT, 40000])"),
                ("for path in range(800):", "for path in range(200):"),
                ("residuals = np.zeros([CLIP_COUNT * 100000])", "residuals = np.zeros([CLIP_COUNT * 40000])"),
                ("pre_compute_table_x = np.linspace(-1000, 1000, 1001)", "pre_compute_table_x = np.linspace(-500, 500, 401)"),
                ("pre_compute_table_z = np.linspace(-1000, 1000, 1001)", "pre_compute_table_z = np.linspace(-500, 500, 401)"),
                ("all_valid_states = np.zeros([1000000000, 4], dtype=np.float32)", "all_valid_states = np.zeros([600000, 4], dtype=np.float32)"),
                ("all_valid_states = np.zeros([100000000, 4], dtype=np.float32)", "all_valid_states = np.zeros([350000, 4], dtype=np.float32)"),
                ("for _ in range(100):", "for _ in range(10):"),
                ("EPOCH = 50", "EPOCH = 10"),
                ("RESTART_EPOCH = 10", "RESTART_EPOCH = 4"),
                ("for _ in range(20):", "for _ in range(4):"),
                ("EPOCH = 15", "EPOCH = 6"),
                ("RESTART_EPOCH = 100", "RESTART_EPOCH = 6"),
                ("clip_index = np.zeros([GROUP_VALUE_COUNT, 100000], dtype=np.uint32)", "clip_index = np.zeros([GROUP_VALUE_COUNT, 30000], dtype=np.uint32)"),
                ("X = np.zeros([GROUP_VALUE_COUNT, 100000, 2])", "X = np.zeros([GROUP_VALUE_COUNT, 30000, 2])"),
                ("y = np.zeros([GROUP_VALUE_COUNT, 100000])", "y = np.zeros([GROUP_VALUE_COUNT, 30000])"),
                ("dist = 500", "dist = 300"),
            ],
        },
        "quality": {
            "replacements": [
                ("X = np.zeros([CLIP_COUNT, 100000])", "X = np.zeros([CLIP_COUNT, 70000])"),
                ("y = np.zeros([CLIP_COUNT, 100000])", "y = np.zeros([CLIP_COUNT, 70000])"),
                ("for path in range(800):", "for path in range(350):"),
                ("residuals = np.zeros([CLIP_COUNT * 100000])", "residuals = np.zeros([CLIP_COUNT * 70000])"),
                ("pre_compute_table_x = np.linspace(-1000, 1000, 1001)", "pre_compute_table_x = np.linspace(-700, 700, 601)"),
                ("pre_compute_table_z = np.linspace(-1000, 1000, 1001)", "pre_compute_table_z = np.linspace(-700, 700, 601)"),
                ("all_valid_states = np.zeros([1000000000, 4], dtype=np.float32)", "all_valid_states = np.zeros([1000000, 4], dtype=np.float32)"),
                ("all_valid_states = np.zeros([100000000, 4], dtype=np.float32)", "all_valid_states = np.zeros([600000, 4], dtype=np.float32)"),
                ("for _ in range(100):", "for _ in range(20):"),
                ("EPOCH = 50", "EPOCH = 14"),
                ("RESTART_EPOCH = 10", "RESTART_EPOCH = 5"),
                ("for _ in range(20):", "for _ in range(8):"),
                ("EPOCH = 15", "EPOCH = 10"),
                ("RESTART_EPOCH = 100", "RESTART_EPOCH = 8"),
                ("clip_index = np.zeros([GROUP_VALUE_COUNT, 100000], dtype=np.uint32)", "clip_index = np.zeros([GROUP_VALUE_COUNT, 50000], dtype=np.uint32)"),
                ("X = np.zeros([GROUP_VALUE_COUNT, 100000, 2])", "X = np.zeros([GROUP_VALUE_COUNT, 50000, 2])"),
                ("y = np.zeros([GROUP_VALUE_COUNT, 100000])", "y = np.zeros([GROUP_VALUE_COUNT, 50000])"),
                ("dist = 500", "dist = 400"),
            ],
        },
    }
    return profiles.get(training_profile, profiles["validate"])


def get_foot_down_settings(training_profile: str) -> dict:
    profiles = {
        "validate": {
            "ranges": "ranges = {\n    'walk1_subject5' : [(60, 320)],\n}\n",
            "clip_length": 60,
            "n_neighbors": 5,
        },
        "adaptive": {
            "ranges": "ranges = {\n    'walk1_subject5' : [(60, 720)],\n    'run1_subject2' : [(100, 520)],\n}\n",
            "clip_length": 120,
            "n_neighbors": 8,
        },
        "quality": {
            "ranges": "ranges = {\n    'walk1_subject5' : [(60, 1200)],\n    'run1_subject2' : [(100, 1000)],\n    'dance1_subject2' : [(100, 620)],\n}\n",
            "clip_length": 160,
            "n_neighbors": 10,
        },
    }
    return profiles.get(training_profile, profiles["validate"])


def get_profile_artifact_name(filename: str, training_profile: str, suffix_hint: str = "") -> str:
    if training_profile == "validate":
        return filename
    path = Path(filename)
    suffix = f"_{training_profile}"
    if suffix_hint:
        suffix += f"_{suffix_hint}"
    return f"{path.stem}{suffix}{path.suffix}"


def load_notebook(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def dump_notebook(path: Path, notebook: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(notebook, handle, indent=1, ensure_ascii=False)
        handle.write("\n")


def transform_source(slug: str, source: str, enable_precompute: bool, training_profile: str, torch_device: str) -> str:
    if slug == MOTION_FIELDS_SLUG:
        settings = get_motion_fields_settings(training_profile, torch_device)
        artifact_name = get_profile_artifact_name(
            "motion_fields_precomputed_all_states_tables.dat",
            training_profile,
            "gpu" if torch_device.startswith("cuda") else "cpu",
        )
        updated = source
        updated = updated.replace(
            "import torch\n",
            "import os\nimport torch\nTORCH_DEVICE_NAME = os.environ.get('ANIMATIONTECH_TORCH_DEVICE', 'cuda' if torch.cuda.is_available() else 'cpu')\nTORCH_DEVICE = torch.device(TORCH_DEVICE_NAME)\n",
        )
        updated = updated.replace("motion_fields_precomputed_all_states_tables.dat", artifact_name)
        updated = updated.replace("dtype=np.bool)\n", "dtype=np.bool_)\n")
        updated = updated.replace(
            "reducer = UMAP(n_components=3, metric='euclidean', n_neighbors = 80)",
            f"reducer = UMAP(n_components=3, metric='euclidean', n_neighbors={settings['umap_neighbors']}, random_state=42)",
        )
        for old, new in settings["state_ranges"].items():
            updated = updated.replace(old, new)
        updated = updated.replace("K_NEIGHBORS = 15\n", f"K_NEIGHBORS = {settings['k_neighbors']}\n")
        updated = updated.replace("theta_count = 17\n", f"theta_count = {settings['theta_count']}\n")
        updated = updated.replace("EPOCH = 300\n", f"EPOCH = {settings['epoch']}\n")
        updated = updated.replace(".to('cuda')", ".to(TORCH_DEVICE)")
        updated = updated.replace('device=\'cuda\'', "device=TORCH_DEVICE")
        if enable_precompute:
            updated = updated.replace("#_build_precomputed_tables()", "_build_precomputed_tables()")
        if "interact(" in updated and "viewer" in updated:
            return "print('AnimationTech automated run: skipped interactive UI cell.')\n"
        return updated

    if slug == REALTIME_PLANNING_SLUG:
        settings = get_realtime_planning_settings(training_profile)
        updated = source.replace("%%time\n", "")
        updated = updated.replace(
            "from sklearn.ensemble import ExtraTreesRegressor\n",
            "import os\nfrom sklearn.dummy import DummyRegressor\nfrom sklearn.ensemble import ExtraTreesRegressor\nANIMATIONTECH_MAX_WORKERS = int(os.environ.get('ANIMATIONTECH_MAX_WORKERS', '0') or '0')\nANIMATIONTECH_TREE_N_JOBS = int(os.environ.get('ANIMATIONTECH_TREE_N_JOBS', '1') or '1')\n",
            1,
        )
        updated = updated.replace(
            "from multiprocessing import Pool\n",
            "import os\nfrom multiprocessing import Pool\nANIMATIONTECH_MAX_WORKERS = int(os.environ.get('ANIMATIONTECH_MAX_WORKERS', '0') or '0')\nANIMATIONTECH_TREE_N_JOBS = int(os.environ.get('ANIMATIONTECH_TREE_N_JOBS', '1') or '1')\n",
        )
        replacements = [
            (
                "# with progress_output:\n#     physics_costs, delta_theta, delta_x, delta_z = pre_compute_transitions_costs(motion_clips, 'realtime_planning_animations_costs.dat')",
                "physics_costs, delta_theta, delta_x, delta_z = pre_compute_transitions_costs(motion_clips, 'realtime_planning_animations_costs.dat')",
            ),
            (
                "# with progress_output:\n#     value_functions_precompute, scores = train_optimal_policy()",
                "value_functions_precompute, scores = train_optimal_policy()",
            ),
            (
                "# with progress_output:\n#     physics_costs, delta_theta, delta_x, delta_z = pre_compute_transitions_costs(motion_groups, 'realtime_planning_animations_group_costs.dat')",
                "physics_costs, delta_theta, delta_x, delta_z = pre_compute_transitions_costs(motion_groups, 'realtime_planning_animations_group_costs.dat')",
            ),
        ]
        for old, new in replacements:
            updated = updated.replace(old, new)
        updated = updated.replace(
            "    value_functions_precompute, scores = train_optimal_policy()",
            "    value_functions_precompute, scores = train_optimal_policy()\n    globals()['value_functions_precompute'] = value_functions_precompute\n    globals()['scores'] = scores",
        )
        updated = updated.replace(
            "    value_functions_precompute, scores = pickle.load(f)",
            "    value_functions_precompute, scores = pickle.load(f)\n    globals()['value_functions_precompute'] = value_functions_precompute\n    globals()['scores'] = scores",
        )
        updated = updated.replace(
            "model = ExtraTreesRegressor(n_estimators=50, random_state=None, n_jobs=-1)",
            "model = ExtraTreesRegressor(n_estimators=50, random_state=None, n_jobs=ANIMATIONTECH_TREE_N_JOBS)",
        )
        updated = updated.replace(
            "                X_train, y_train = X[i, :count[i]], y[i, :count[i]]\n                model = ExtraTreesRegressor(n_estimators=50, random_state=None, n_jobs=ANIMATIONTECH_TREE_N_JOBS)\n                model.fit(X_train.reshape(-1, 1), y_train)\n                value_functions.append(model)",
            "                X_train, y_train = X[i, :count[i]], y[i, :count[i]]\n                if count[i] == 0:\n                    model = DummyRegressor(strategy='constant', constant=0.0)\n                    model.fit(np.zeros((1, 1)), np.zeros(1))\n                else:\n                    model = ExtraTreesRegressor(n_estimators=50, random_state=None, n_jobs=ANIMATIONTECH_TREE_N_JOBS)\n                    model.fit(X_train.reshape(-1, 1), y_train)\n                value_functions.append(model)",
        )
        updated = updated.replace(
            "                X_train, y_train = X[i, :count[i]], y[i, :count[i]]\n                refit_tree(value_functions[i], X_train.reshape(-1, 1), y_train)",
            "                X_train, y_train = X[i, :count[i]], y[i, :count[i]]\n                if count[i] > 0:\n                    refit_tree(value_functions[i], X_train.reshape(-1, 1), y_train)",
        )
        updated = updated.replace("with Pool() as pool:", "with Pool(processes=ANIMATIONTECH_MAX_WORKERS if ANIMATIONTECH_MAX_WORKERS > 0 else None) as pool:")
        for old, new in settings["replacements"]:
            updated = updated.replace(old, new)
        realtime_artifacts = [
            "realtime_planning_animations_costs.dat",
            "realtime_planning_orientation_value_functions.dat",
            "realtime_planning_reach_position_value_functions.dat",
            "realtime_planning_animations_group_costs.dat",
            "realtime_planning_reach_position_group_value_functions.dat",
        ]
        for artifact_name in realtime_artifacts:
            updated = updated.replace(artifact_name, get_profile_artifact_name(artifact_name, training_profile))
        return updated

    if slug == KNOWING_FOOT_DOWN_SLUG:
        settings = get_foot_down_settings(training_profile)
        updated = source.replace(
            "ranges = {\n    'walk1_subject5' : [(60, 7060)],\n    'walk3_subject1' : [(100, 900), (1300, 2500), (4400, 5200), (7150,7350)], \n    'run1_subject2' : [(100, 5100) ], \n    'dance1_subject2' : [(100, 1900) ], \n    'aiming2_subject2' : [(100, 4100), (4900, 6100), (8300,8900)], \n}\n",
            settings["ranges"],
        )
        updated = updated.replace("clip_length = 200\n", f"clip_length = {settings['clip_length']}\n")
        updated = updated.replace("n_neighbors = 10\n", f"n_neighbors = {settings['n_neighbors']}\n")
        if "# get the first range, to see if it works" in updated or "# get the worst labeling" in updated:
            return "print('AnimationTech automated run: skipped expensive nearest-neighbor demo cell.')\n"
        if "interact(" in updated or "display(buttons)" in updated or "display(canvas)" in updated or "display(viewer)" in updated:
            return "print('AnimationTech automated run: skipped interactive UI cell.')\n"
        return updated

    return source


def prepare_notebook(slug: str, notebook: dict, enable_precompute: bool, training_profile: str, torch_device: str) -> dict:
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        updated = transform_source(slug, source, enable_precompute, training_profile, torch_device)
        if updated != source:
            cell["source"] = updated.splitlines(keepends=True)
    return notebook


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an execution copy of a notebook.")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--input", required=True, dest="input_path")
    parser.add_argument("--output", required=True, dest="output_path")
    parser.add_argument("--enable-precompute", action="store_true")
    parser.add_argument("--training-profile", choices=["validate", "adaptive", "quality"], default="validate")
    parser.add_argument("--torch-device", default="cpu")
    args = parser.parse_args()

    input_path = Path(args.input_path)
    output_path = Path(args.output_path)

    notebook = load_notebook(input_path)
    prepared = prepare_notebook(args.slug, notebook, args.enable_precompute, args.training_profile, args.torch_device)
    dump_notebook(output_path, prepared)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
