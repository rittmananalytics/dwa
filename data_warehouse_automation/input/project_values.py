"""
This module reads the project .yml file and extracts its values into a dictionary

"""
import yaml

def read_project_file(project_dir):

    # Read the content of the project configuration file
    with open(project_dir, 'r') as file:
        profile_content = yaml.safe_load(file)

    return profile_content
