"""
This module orchestrates all other modules.
main() is the first function that's kicked off when `dwa...` commands are run.

"""
import os.path
from data_warehouse_automation.input.parse_cli_input import parse_cli_input
from data_warehouse_automation.input.configuration_values import read_project_file, read_profile_file
from data_warehouse_automation.input.information_schema import query_snowflake_tables_and_columns
from data_warehouse_automation.inferring.extract_table_pks import extract_table_pks
from data_warehouse_automation.inferring.extract_pk_fk_pairs import extract_pk_fk_pairs
from data_warehouse_automation.inferring.infer_join_cardinality import infer_join_cardinality
from data_warehouse_automation.input.read_text_file import read_text_file
from data_warehouse_automation.input.process_markdown_file_content import extract_documentation
from data_warehouse_automation.cube.cube_base_layer import generate_cube_js_base_file


def main():
    
    # Create the path to the default configuration files
    default_profile_dir = os.path.expanduser( '~/.dwa/profiles.yml' )
    default_project_dir = os.path.join( os.getcwd(), 'dwa_project.yml' )

    # Parse the CLI input
    args = parse_cli_input( default_profile_dir, default_project_dir )

    # Read the project and profile configuration files
    project_content = read_project_file( args.project_dir )
    profile_content = read_profile_file( args.profile_dir, project_content['profile'] )

    # Query Snowflake to retrieve the information schema
    schema, snowflake_connection = query_snowflake_tables_and_columns(
        account = profile_content['account'],
        database = profile_content['database'],
        password = profile_content['password'],
        role = profile_content['role'],
        schema = profile_content['schema_name'],
        user = profile_content['user'],
        warehouse = profile_content['warehouse'],
    )

    # Extract PKs from the schema
    table_pks = extract_table_pks(schema)

    # Initialize inferred_join_cardinalities to None so there's something to pass to
    # generate_cube_js_base_file() even if infer_join_cardinality() doesn't generate any output
    inferred_join_cardinalities = None

    # Check if join inference is enabled
    if project_content.get('join_inference_enabled', False):
        print('Initiating join inference')

        # Extract PK-FK pairs
        pk_fk_pairs = extract_pk_fk_pairs(schema)

        # infer joins
        inferred_join_cardinalities = infer_join_cardinality(
            connection = snowflake_connection,
            pk_fk_pairs = pk_fk_pairs,
            table_pks = table_pks,
            join_query_time_threshold = project_content['join_query_time_threshold'])
    else:
        print('join_inference_enabled is not set to true in project .yml file. Join inference is skipped')

    # Close the Snowflake connection
    snowflake_connection.close()

    # Set the file path for the cube.js base file
    file_path = 'cube/schema/base.js'

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
            field_descriptions_dictionary,
            inferred_join_cardinalities
        )
    else:
        print( 'Invalid command' )


if __name__ == "__main__":
    main()