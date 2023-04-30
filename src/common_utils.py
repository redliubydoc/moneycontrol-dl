import json

def save_json(json_obj, output_file_path):

    with open(output_file_path, "w") as file:
        json.dump(json_obj, file)


def read_json(input_file_path):

    with open(input_file_path, "r") as file:
        json_obj = json.load(file)

    return json_obj


def create_directory_structure(directories):

    for directory in directories:
        not directory.exists() and directory.mkdir(parents=True)
