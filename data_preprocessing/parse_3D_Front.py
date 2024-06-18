"""
File preprocesses the 3D-FUTURE-scene dataset by reorganizing unsorted annotations by scene based on "image_id". 
It groups object annotations into a single map for each scene to improve data organization and accessibility.
"""

import json
from settings import GT_TEST_SET, TEST_SET_JSON


def parse_json_file(file_path, output_file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

        # Parsing for first 3 images for memory reasons
        categories = data["categories"][:3]
        images = data["images"][:3]

        # Collect annotations for each image based on image_id
        annotations_map = {}
        for image in images:
            image_id = image["id"]
            annotations_map[image_id] = [
                annotation
                for annotation in data["annotations"]
                if annotation["image_id"] == image_id
            ]

        structured_data = {
            "categories": categories,
            "images": images,
            "annotations": annotations_map,
        }

        with open(output_file_path, "w") as outfile:
            json.dump(structured_data, outfile, indent=4)

        print(json.dumps(structured_data, indent=4))


if __name__ == "__main__":
    parse_json_file(
        GT_TEST_SET,
        TEST_SET_JSON,
    )
