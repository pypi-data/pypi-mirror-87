import json
import os

from pathlib import Path


def write_json(data, filename):
    """Write data to a json file, and add a line break at the end"""
    with open(filename, "w+") as outfile:
        json.dump(data, outfile, indent=4, separators=(",", ": "))
        outfile.write("\n")


def read_json(filename, folder):
    """Reads a json file. Can leave .json out of filename"""
    if filename[-5:] != ".json":
        filename = filename + ".json"

    with open(Path(folder) / filename, "r") as json_data:
        return json.load(json_data)


def make_folder_if_new(folder):
    """Check if a path already exists, and make the necessary folders if it doesn't"""
    destination = Path.cwd() / folder
    if not os.path.exists(destination):
        os.makedirs(destination)
