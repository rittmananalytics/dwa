"""
This module returns the content of a text file

"""

import os

def read_text_file(
    file_path,
    file_name,
    ):
    
    # Construct the full path to the file
    full_file_path = os.path.join(file_path, file_name)

    try:
        # Try to open the file and read its content
        with open(full_file_path, 'r') as file:
            file_content = file.read()
    except FileNotFoundError:
        # If the file does not exist, return an empty string
        return {}

    return file_content
