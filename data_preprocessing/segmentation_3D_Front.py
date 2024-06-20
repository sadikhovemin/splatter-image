import json
import numpy as np
from PIL import Image
from settings import TEST_SET_JSON, SAMPLE_IMAGE


def rle_to_mask(rle, shape):
    """
    Convert RLE run length encoding into a binary mask.
    :param rle: Run-length as list of numbers (starts, lengths)
    :param shape: tuple, shape (height, width) of the mask to be returned
    :return: numpy array, binary mask
    """
    if len(rle) % 2 != 0:
        print("Warning: RLE data has odd length, which might indicate an error.")
        rle.append(0)

    img = np.zeros(shape[0] * shape[1], dtype=np.uint8)
    position = 0
    for i in range(0, len(rle), 2):
        skip = rle[i]
        mark = rle[i + 1]
        position += skip
        img[position:position + mark] = 1
        position += mark

    return img.reshape(shape)


def apply_mask(image, mask):
    """
    Apply a binary mask to an image.
    :param image: PIL image
    :param mask: numpy array, binary mask
    :return: PIL image, with mask applied
    """
    image_array = np.array(image)
    masked_image = image_array * mask[:, :, None]
    return Image.fromarray(masked_image.astype(np.uint8))


def load_image(image_path):
    return Image.open(image_path)


def extract_rle_and_apply_mask(json_path, image_path, output_path, image_shape):
    with open(json_path, "r") as file:
        data = json.load(file)
        first_key = next(iter(data["annotations"]))
        rle = data["annotations"][first_key][0]["segmentation"]["counts"]

    image = load_image(image_path)
    mask = rle_to_mask(rle, image_shape)
    masked_image = apply_mask(image, mask)
    masked_image.save(output_path)


if __name__ == "__main__":
    json_path = TEST_SET_JSON
    image_path = SAMPLE_IMAGE
    output_path = 'masked_output.jpg'
    image_shape = (1200, 1200)
    extract_rle_and_apply_mask(json_path, image_path, output_path, image_shape)