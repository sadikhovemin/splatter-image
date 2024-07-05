import os
import trimesh
import numpy as np
import json


def create_submesh(mesh, vertex_indices):
    # Create a mask for vertices to keep
    mask = np.zeros(len(mesh.vertices), dtype=bool)
    mask[vertex_indices] = True

    # Filter triangles where all vertices are included in vertex_indices
    sub_triangles = [i for i, triangle in enumerate(mesh.faces) if mask[triangle].all()]

    # Extract the submesh using the filtered triangles
    # Note: If only one submesh is expected, we directly access it without indexing
    sub_mesh = mesh.submesh([sub_triangles], only_watertight=False, append=True)

    return sub_mesh


def main():
    # Load the main mesh
    mesh = trimesh.load(
        "/storage/user/yez/scannet++/data/5d152fab1b/scans/mesh_aligned_0.05.ply"
    )

    output_directory = (
        "/usr/prakt/s0091/github/splatter-image/data_preprocessing/scannetpp_output"
    )

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Load the segments annotation JSON
    with open(
        "/storage/user/yez/scannet++/data/5d152fab1b/scans/segments_anno.json", "r"
    ) as file:
        segments_data = json.load(file)

    # Process each segment group
    for segment in segments_data["segGroups"]:
        try:
            object_id = segment["objectId"]
            label = segment["label"]
            segment_ids = segment["segments"]

            # Create submesh for the current object
            sub_mesh = create_submesh(mesh, segment_ids)

            # Define the filename and save the submesh as a PLY file
            filename = f"{output_directory}/output_mesh_{label}_{object_id}.ply"
            sub_mesh.export(filename)
            print(f"Saved {filename}")

        except Exception as e:
            print("Error processing segment {}: {}".format(object_id, str(e)))


if __name__ == "__main__":
    main()
