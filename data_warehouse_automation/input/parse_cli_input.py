"""
This module defines the available commands, their input parameters, and kicks off relevant
upstrem modules accordingly.

"""
import argparse


def parse_cli_input( default_profile_dir, default_project_dir ):
    
    # Create the parser
    parser = argparse.ArgumentParser(description='A simple argparse program' )

    # Add subparsers for different commands
    subparsers = parser.add_subparsers( dest='command', help='Available commands' )

    # Subparser for 'cube' command
    test_parser = subparsers.add_parser( 'cube', help='Generates base cube syntax' )
    test_parser.add_argument( 'profile_dir', type=str, nargs='?', default=default_profile_dir, help='This command takes the path/to/your/profile.yml as input' )
    test_parser.add_argument( 'project_dir', type=str, nargs='?', default=default_project_dir, help='This command takes the path/to/your/project.yml as input' )

    # Parse the arguments
    args = parser.parse_args()

    return args