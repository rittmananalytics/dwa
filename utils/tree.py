"""
This script recursively lists all directories and files in a given directory, 
indenting them to represent their level in the directory hierarchy. 

The script takes a directory path as a command-line argument and walks through 
each subdirectory, printing the directory or file names. The indentation is 
determined by counting the number of separators in the relative path from the 
starting directory to the current directory or file.

Usage:
python tree.py /path/to/your/directory
"""

import os
import sys

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

# Use the first command line argument as the path
list_files(sys.argv[1])
