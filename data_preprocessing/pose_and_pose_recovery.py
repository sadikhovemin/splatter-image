import pywavefront
import numpy as np
import matplotlib.pyplot as plt
import json
import trimesh

# Load the .obj model
# obj_file = "/storage/group/dataset_mirrors/01_incoming/3DFront/3D-FUTURE-model/3062da49-9d90-3894-8c6a-207b131a7f1f/normalized_model.obj"
obj_file = "/storage/group/dataset_mirrors/01_incoming/3DFront/3D-FUTURE-model/c1cdca71-d544-4300-8351-f4034eb140b7/normalized_model.obj"
scene = pywavefront.Wavefront(obj_file, collect_faces=True)
vertices = np.array(scene.vertices)

# Load the JSON file containing the pose data
# json_file = "/storage/group/dataset_mirrors/01_incoming/3DFront/3D-FUTURE-scene/GT/test_set.json"
# with open(json_file, "r") as file:
#     data = json.load(file)
#     pose = data["annotations"][0][
#         "pose"
#     ]  # Adjust this according to the actual JSON structure

# # Extract rotation and translation from the pose data
# R = np.array(pose["rotation"])
# T = np.array(pose["translation"])


matrix = np.array(
    [
        [0.97244893, 0.0, 0.23307221, -0.20811252],
        [0.01788679, 0.99705087, -0.07462918, -0.87410725],
        [-0.23238484, 0.07674355, 0.96958104, -2.40567632],
        [0.0, 0.0, 0.0, 1.0],
    ]
)

R = matrix[:3, :3]

T = matrix[:3, 3]

print("R", R)
print("T", T)

# Apply transformation to get vertices as seen in the scene
new_vertices = vertices @ R.T - T


# Plot original vertices
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(vertices[:, 0], vertices[:, 1], "o")
plt.title("Original Vertices")

# Plot transformed vertices
plt.subplot(1, 2, 2)
plt.plot(new_vertices[:, 0], new_vertices[:, 1], "o")
plt.title("Transformed Vertices")

# Save the figure
plt.savefig("/usr/prakt/s0091/github/splatter-image/pose_figure.png")
plt.close()


# ----------- VERIFICATION -----------

# Assume M_prime, R, and T are already defined or obtained from earlier in the code
# M_prime is new_vertices in your current code

# Reverse the translation
corrected_vertices = new_vertices + T

# Reverse the rotation
original_vertices = (
    corrected_vertices @ R
)  # Since R.T @ R = I (Identity matrix) if R is a proper rotation matrix


# Plotting for verification
plt.figure(figsize=(10, 10))
plt.subplot(2, 2, 1)
plt.plot(vertices[:, 0], vertices[:, 1], "o")
plt.title("Original Vertices M")

plt.subplot(2, 2, 2)
plt.plot(new_vertices[:, 0], new_vertices[:, 1], "o")
plt.title("Transformed Vertices M'")

plt.subplot(2, 2, 3)
plt.plot(original_vertices[:, 0], original_vertices[:, 1], "o")
plt.title("Recovered Vertices M")

plt.savefig("/usr/prakt/s0091/github/splatter-image/verification_figure_for_pose.png")
plt.close()
