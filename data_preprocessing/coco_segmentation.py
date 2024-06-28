from pycocotools.coco import COCO
import numpy as np
from PIL import Image
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


def get_mask(json_path, image_directory):
    coco = COCO(json_path)
    img_id = 1
    img = coco.imgs[img_id]
    ann_ids = coco.getAnnIds(imgIds=img["id"])
    anns = coco.loadAnns(ann_ids)
    mask = coco.annToMask(anns[0])

    # Construct image path
    image_path = f"{image_directory}/{img['file_name']}.jpg"

    # Apply mask to image
    masked_image = apply_segmentation_mask(image_path, mask)

    # Optionally, save the image
    masked_image.save("coco_masked_output.jpg")


if __name__ == "__main__":
    image_directory = "/storage/group/dataset_mirrors/01_incoming/3DFront/3D-FUTURE-scene/test/image"  # Update as needed
    get_mask(GT_TEST_SET, image_directory)
