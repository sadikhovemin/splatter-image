import os
import json


def get_folder_names(directory):
    # Get all entries in the directory
    entries = os.listdir(directory)
    # Filter out only directories
    folders = [
        entry for entry in entries if os.path.isdir(os.path.join(directory, entry))
    ]
    return folders


def save_list_to_json(data, json_file):
    # Save the list as a JSON file
    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    directory_path = "/usr/prakt/s0091/views_release"
    json_file_path = "/usr/prakt/s0091/annotations_filtered.json"

    folder_names = get_folder_names(directory_path)
    save_list_to_json(folder_names, json_file_path)

    print(f"Folder names in '{directory_path}' have been saved to '{json_file_path}'")
