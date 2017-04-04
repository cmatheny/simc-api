import json
import pathlib
import os

def remove_file(filename):
    try:
        os.remove(filename)
    except OSError:
        pass

def check_for_file(filename):
    return pathlib.Path(filename).is_file()

def load_json(filename):
    with open(filename) as json_file:    
        json_data = json.load(json_file)
    return json_data
    