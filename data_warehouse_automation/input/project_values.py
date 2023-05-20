"""
This module reads the project .yml file and extracts its values into dictionary

"""
import yaml

def read_project_file(project_dir):

    with open(project_dir, 'r') as file:
        profile_json = yaml.safe_load(file)

    return profile_json
