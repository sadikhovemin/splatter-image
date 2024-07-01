from pycocotools.coco import COCO
import numpy as np
from PIL import Image
import os
from settings import GT_TEST_SET


def apply_segmentation_mask(image_path, mask):
    """
    Apply the segmentation mask to the image.
    :param image_path: Path to the image file.
    :param mask: A numpy array containing the binary mask.
    :return: PIL Image object with the mask applied.
    """
    image = Image.open(image_path).convert("RGB")
    image_array = np.array(image)

    # Apply the mask: Multiply the mask with each color channel of the image
    masked_image_array = np.zeros_like(image_array)
    for i in range(3):  # Assuming RGB
        masked_image_array[:, :, i] = image_array[:, :, i] * mask

    # Convert the masked image array back to a PIL Image
    masked_image = Image.fromarray(masked_image_array)
    return masked_image


def process_first_50_annotations(json_path, image_directory, output_directory):
    coco = COCO(json_path)
    annotation_ids = coco.getAnnIds()[:50]  # Get IDs of the first 50 annotations

    for ann_id in annotation_ids:
        ann = coco.loadAnns(ann_id)[0]  # Assuming each ID returns a single annotation
        img_id = ann["image_id"]
        img_info = coco.loadImgs(img_id)[0]
        mask = coco.annToMask(ann)
        model_id = ann["model_id"]  # Adjust this if model_id is stored differently

        # Construct image path
        image_path = f"{image_directory}/{img_info['file_name']}.jpg"

        # Define model directory and create it if doesn't exist
        model_dir = os.path.join(output_directory, str(model_id))
        os.makedirs(model_dir, exist_ok=True)

        # Determine the next file number
        existing_files = [f for f in os.listdir(model_dir) if f.endswith(".png")]
        if existing_files:
            last_file = max(existing_files)
            next_file_num = int(last_file.split(".")[0]) + 1
        else:
            next_file_num = 0

        output_path = os.path.join(model_dir, f"{next_file_num:03d}.png")

        # Apply mask to image and save
        masked_image = apply_segmentation_mask(image_path, mask)
        masked_image.save(output_path)


if __name__ == "__main__":
    image_directory = (
        "/storage/group/dataset_mirrors/01_incoming/3DFront/3D-FUTURE-scene/test/image"
    )
    output_directory = "/usr/prakt/s0091/github/splatter-image/processed_front3D"
    json_path = GT_TEST_SET
    process_first_50_annotations(json_path, image_directory, output_directory)
