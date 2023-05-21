"""
This module returns the content of a text file

"""

import os

def read_text_file(file_path, file_name):
    # Construct the full path to the file
    full_file_path = os.path.join(file_path, file_name)

    # Open the file and read its content
    with open(full_file_path, 'r') as file:
        file_content = file.read()

    return file_content
