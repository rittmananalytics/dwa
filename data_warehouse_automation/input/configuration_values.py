"""
This module reads the project and profile .yml configuration files and extracts their values into object

"""
import yaml

def read_project_file( project_dir ):

    # Read the content of the project configuration file
    with open(project_dir, 'r') as file:
        profile_content = yaml.safe_load(file)

    return profile_content

def read_profile_file( profile_dir, profile_name ):

    # Read the content of the profile configuration file
    with open( profile_dir, 'r' ) as file:
        profile_content = yaml.safe_load( file )[ profile_name ]
        print(profile_content)

    return profile_content
