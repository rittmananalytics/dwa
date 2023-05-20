"""
This module defines the available commands, their input parameters, and kicks off relevant
upstrem modules accordingly.

"""
import argparse
import os.path
from data_warehouse_automation.cube.cube_name_tbc import generate_cube
from data_warehouse_automation.input.project_values import read_project_file


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='A simple argparse program')
    
    # Create the path to the default configuration files
    default_profile_dir = os.path.expanduser('~/.droughty/profile.yaml')
    default_project_dir = os.path.join(os.getcwd(), 'dwa_project.yml')

    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Subparser for 'cube' command
    test_parser = subparsers.add_parser('cube', help='Generates base cube syntax')
    test_parser.add_argument('profile_dir', type=str, nargs='?', default=default_profile_dir, help='This command takes the path/to/your/profile.yml as input')
    test_parser.add_argument('project_dir', type=str, nargs='?', default=default_project_dir, help='This command takes the path/to/your/project.yml as input')

    # Parse the arguments
    args = parser.parse_args()

    # Get the project file information
    profile_json = read_project_file( args.project_dir )

    # Process based on the command
    if args.command == 'cube':
        generate_cube(args.profile_dir, args.project_dir)
    else:
        print('Invalid command')

if __name__ == "__main__":
    main()