import numpy as np

# file_path = "/usr/prakt/s0091/github/splatter-image/renders_3/images/000.npy"
file_path = "processed_front3D/3ffaa0a4-3ff5-364e-afec-0835c098d1ff/001.npy"
# file_path = (
# "/usr/prakt/s0091/front-3d-simplified/3062da49-9d90-3894-8c6a-207b131a7f1f/009.npy"
# )
data = np.load(file_path)


print("Loaded data:\n", data)
print("Shape of the loaded data:", data.shape)


if data.shape == (3, 4):
    print("Data is a 3x4 matrix, valid for rotation and translation.")
elif data.shape == (4, 4):
    print("Data is a 4x4 homogeneous transformation matrix, also valid.")
else:
    print("Unexpected matrix size. Please check the data format.")


if data.shape[1] == 4:  # Ensuring it has 4 columns
    rotation_part = data[:3, :3]  # Extract the top-left 3x3 part
    if np.allclose(np.dot(rotation_part, rotation_part.T), np.eye(3), atol=1e-6):
        print("Rotation matrix is valid.")
    else:
        print("Rotation matrix might not be valid.")

    translation_part = data[:3, 3]
    print("Translation vector:", translation_part)
