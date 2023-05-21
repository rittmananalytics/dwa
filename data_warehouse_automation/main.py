"""
This module 

"""
import os.path
from data_warehouse_automation.input.parse_cli_input import parse_cli_input
from data_warehouse_automation.input.configuration_values import read_project_file, read_profile_file
from data_warehouse_automation.input.information_schema import query_snowflake_tables_and_columns
from data_warehouse_automation.input.read_text_file import read_text_file
from data_warehouse_automation.input.process_markdown_file_content import extract_documentation
from data_warehouse_automation.cube.cube_base_layer import generate_cube_js_base_file


def main():
    
    # Create the path to the default configuration files
    default_profile_dir = os.path.expanduser( '~/.droughty/profile.yaml' )
    default_project_dir = os.path.join( os.getcwd(), 'dwa_project.yml' )

    # Parse the CLI input
    args = parse_cli_input( default_profile_dir, default_project_dir )

    # Read the project and profile configuration files
    project_content = read_project_file( args.project_dir )
    profile_content = read_profile_file( args.profile_dir, project_content['profile'] )

    # Query Snowflake to retrieve the information schema
    schema = query_snowflake_tables_and_columns(
        user = profile_content['user'],
        password = profile_content['password'],
        account = profile_content['account'],
        warehouse = profile_content['warehouse'],
        database = profile_content['database'],
        schema = profile_content['schema_name']
    )

    # Set the file path for the cube.js base file
    
    file_path = 'cube/schema/base.js' # TODO put in project config

    # Process based on the command
    if args.command == 'cube':
        field_description_file_content = read_text_file( 
            project_content['field_description_path'],
            project_content['field_description_file_name']
        )
        field_descriptions_dictionary = extract_documentation(field_description_file_content)
        generate_cube_js_base_file(
            schema,
            file_path,
            field_descriptions_dictionary
        )
    else:
        print( 'Invalid command' )

if __name__ == "__main__":
    main()