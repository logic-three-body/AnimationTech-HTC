import argparse
import pickle
import sys
from pathlib import Path

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None


TOOLS_DIR = Path(__file__).resolve().parents[2] / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from generate_halo_face_asset import write_synthetic_face_asset


FRAME_COUNT = 220


def export_from_maya(output_path: Path) -> Path:
    selected = cmds.ls(sl=True)
    if not selected:
        raise RuntimeError("No Maya object selected for export.")

    obj = selected[0]
    vertex_count = cmds.polyEvaluate(obj, v=True)
    face_count = cmds.polyEvaluate(obj, f=True)

    indices = [
        [int(a[0]), int(a[1]), int(a[2])]
        for a in [
            [
                x
                for x in str(cmds.polyInfo(f"{obj}.f[{f}]", faceToVertex=True)[0]).split(" ")
                if x
            ][2:5]
            for f in range(face_count)
        ]
    ]

    normals = [
        cmds.polyNormalPerVertex(f"{obj}.vtx[{i}]", query=True, xyz=True)[:3]
        for i in range(vertex_count)
    ]

    frames = []
    for frame in range(FRAME_COUNT):
        cmds.currentTime(frame)
        vertices = [cmds.xform(f"{obj}.vtx[{v}]", q=True, t=True) for v in range(vertex_count)]
        frames.append(vertices)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as handle:
        pickle.dump((indices, normals, frames), handle)
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Halo 4 facial animation data from Maya or generate a synthetic fallback.")
    parser.add_argument("--output", default=str(Path(__file__).with_name("animated_face.dat")))
    parser.add_argument("--force-synthetic", action="store_true")
    args = parser.parse_args()

    output_path = Path(args.output).resolve()
    if args.force_synthetic or cmds is None:
        write_synthetic_face_asset(output_path)
        print(output_path)
        return 0

    exported_path = export_from_maya(output_path)
    print(exported_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
