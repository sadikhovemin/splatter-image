from pycocotools.coco import COCO
import numpy as np
import os
from settings import GT_TRAIN_SET


def save_camera_parameters(json_path, output_directory):
    coco = COCO(json_path)
    annotation_ids = coco.getAnnIds()[
        :50
    ]  # Limit to the first 50 annotations for consistency

    for ann_id in annotation_ids:
        ann = coco.loadAnns(ann_id)[0]
        model_id = ann["model_id"]

        # Directory for storing the camera parameters
        model_dir = os.path.join(output_directory, str(model_id))
        os.makedirs(model_dir, exist_ok=True)

        # Determine the next file number based on existing .npy files
        existing_files = [f for f in os.listdir(model_dir) if f.endswith(".npy")]
        if existing_files:
            last_file = max(existing_files)
            next_file_num = int(last_file.split(".")[0]) + 1
        else:
            next_file_num = 0

        output_path = os.path.join(model_dir, f"{next_file_num:03d}.npy")

        # Extract camera parameters
        rotation = np.array(ann["pose"]["rotation"])
        translation = np.array(ann["pose"]["translation"])

        # Create a 4x4 transformation matrix
        transformation_matrix = np.eye(4)
        transformation_matrix[:3, :3] = rotation
        transformation_matrix[:3, 3] = translation

        # Save the transformation matrix
        np.save(output_path, transformation_matrix)


if __name__ == "__main__":
    output_directory = "/usr/prakt/s0091/github/splatter-image/processed_front3D"
    json_path = GT_TRAIN_SET
    save_camera_parameters(json_path, output_directory)
