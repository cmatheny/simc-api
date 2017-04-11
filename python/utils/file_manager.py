import json
import pathlib
import os
import sys

from utils.misc import singleton


def remove_file(filename):
    try:
        os.remove(filename)
    except OSError:
        return False


def check_for_file(filename):
    return pathlib.Path(filename).is_file()


def load_json(filename):
    with open(filename) as json_file:
        json_data = json.load(json_file)
    return json_data


@singleton
class FileManager:

    def __init__(self):
        self.null = open(os.devnull, "w")
        self.stdout = sys.stdout
        self.stderr = sys.stderr
