import argparse
import math
import pickle
from pathlib import Path


FRAME_COUNT = 220
GRID_WIDTH = 12
GRID_HEIGHT = 10
GRID_SPACING = 12.0
BASE_HEIGHT = 165.0


def _grid_vertices():
    x_offset = (GRID_WIDTH - 1) * GRID_SPACING * 0.5
    z_offset = (GRID_HEIGHT - 1) * GRID_SPACING * 0.5
    vertices = []
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            x = col * GRID_SPACING - x_offset
            z = row * GRID_SPACING - z_offset
            vertices.append((x, BASE_HEIGHT, z))
    return vertices


def _grid_indices():
    triangles = []
    for row in range(GRID_HEIGHT - 1):
        for col in range(GRID_WIDTH - 1):
            top_left = row * GRID_WIDTH + col
            top_right = top_left + 1
            bottom_left = top_left + GRID_WIDTH
            bottom_right = bottom_left + 1
            triangles.append([top_left, bottom_left, top_right])
            triangles.append([top_right, bottom_left, bottom_right])
    return triangles


def _grid_normals():
    return [[0.0, 1.0, 0.0] for _ in range(GRID_WIDTH * GRID_HEIGHT)]


def build_synthetic_face_asset():
    base_vertices = _grid_vertices()
    indices = _grid_indices()
    normals = _grid_normals()
    frames = []
    for frame in range(FRAME_COUNT):
        phase = (2.0 * math.pi * frame) / FRAME_COUNT
        animated_vertices = []
        for vertex_index, (x, _, z) in enumerate(base_vertices):
            col = vertex_index % GRID_WIDTH
            row = vertex_index // GRID_WIDTH
            wave_a = math.sin(phase + col * 0.45)
            wave_b = math.cos((phase * 1.6) + row * 0.55)
            wave_c = math.sin((phase * 0.5) + (col + row) * 0.3)
            y = BASE_HEIGHT + (wave_a * 7.0) + (wave_b * 5.0) + (wave_c * 3.0)
            animated_vertices.append([x, y, z])
        frames.append(animated_vertices)
    return indices, normals, frames


def write_synthetic_face_asset(output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_synthetic_face_asset()
    with output_path.open("wb") as handle:
        pickle.dump(payload, handle)
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a synthetic Halo 4 facial animation asset.")
    parser.add_argument("--output", required=True, dest="output_path")
    args = parser.parse_args()

    output_path = write_synthetic_face_asset(Path(args.output_path))
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
