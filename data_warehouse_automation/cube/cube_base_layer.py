
"""
This module generates the cube base layer

"""

import os

# Convert a string to camel case
def to_camel_case(name):
    components = name.split('_')
    return components[0].lower() + ''.join(x.title() for x in components[1:])


def generate_cube_js_base_file( tables_columns, file_path, field_descriptions_dictionary, inferred_join_cardinalities ):

    # Create the necessary directories
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Create a dictionary mapping tables to their join cardinalities
    join_cardinalities_dict = {(j['left_table'], j['right_table']): j['cardinality'] for j in inferred_join_cardinalities}

    # Open the file for writing
    with open(file_path, 'w') as file:

        print(f"Attempting to generate base Cube file here: {file_path}")

        # Write the import statement at the top of the file
        file.write('import { databaseSchema, databaseName } from \'../tablePrefix\';\n\n')

        # Iterate over each table in the dictionary
        for table_name, columns in tables_columns.items():

            # Write the cube-level attributes
            table_name_camel_case = to_camel_case(table_name)
            file.write(f'cube(`{table_name_camel_case}`, {{\n\n')

            file.write(f'  sql: `select * from ${{databaseName()}}.${{databaseSchema()}}."{table_name}"`,\n\n')

            file.write('  shown: false,\n\n')

            # Write joins if they exist
            if inferred_join_cardinalities:
                file.write('  joins: {\n')
                for join in inferred_join_cardinalities:
                    if join['left_table'] == table_name or join['right_table'] == table_name:
                        join_table_name = join['right_table'] if join['left_table'] == table_name else join['left_table']
                        join_table_name_camel_case = to_camel_case(join_table_name)
                        relationship = join['cardinality'].replace('_','To').capitalize()
                        file.write(f'    {join_table_name_camel_case}: {{\n')
                        file.write(f'      relationship: "{relationship}",\n')
                        file.write(f'      sql: `${{CUBE}}."{join["left_column"]}" = {join_table_name_camel_case}."{join["right_column"]}"`\n')
                        file.write('    },\n')
                file.write('  },\n')

            # Initialize dimensions and measures
            dimensions = []
            measures = []

            # Process each column in the table
            for column_info in columns:
                column_name = column_info['column_name']
                data_type = column_info['data_type']
                column_name_camel_case = to_camel_case(column_name)
                column_description = field_descriptions_dictionary.get(column_name.lower(), 'no description') # Find field description 

                # Prep column's attributes based on rules
                if column_name.lower().endswith('_pk'): # Primary Key
                    dimensions.append(f'{column_name_camel_case}: {{\n      sql: `${{CUBE}}."{column_name}"`,\n      description: `{column_description}`, \n      type: "string",\n      primaryKey: true \n    }}')
                elif data_type.lower() in ['text', 'varchar', 'string', 'char', 'binary', 'variant']: # String types
                    dimensions.append(f'{column_name_camel_case}: {{\n      sql: `${{CUBE}}."{column_name}"`,\n      description: `{column_description}`, \n      type: "string" \n    }}')
                elif data_type.lower() in ['number', 'numeric', 'float', 'float64', 'integer', 'int', 'smallint', 'bigint']: # Numeric types
                    measures.append(f'{to_camel_case("sum_" + column_name)}: {{\n      sql: `${{CUBE}}."{column_name}"`,\n      description: `{column_description}`, \n      type: "sum" \n    }}')
                elif data_type.lower() in ['timestamp', 'timestamp_tz', 'timestamp_ltz', 'timestamp_ntz', 'date', 'time']: # Date, time and timestamp-related types
                    dimensions.append(f'{column_name_camel_case}: {{\n      sql: `${{CUBE}}."{column_name}"`,\n      description: `{column_description}`, \n      type: "time" \n    }}')
                elif data_type.lower() in ['boolean']: # Boolean types
                    dimensions.append(f'{column_name_camel_case}: {{\n      sql: `${{CUBE}}."{column_name}"`,\n      description: `{column_description}`, \n      type: "boolean" \n    }}')

            # Write dimensions
            file.write('  dimensions: {\n\n')
            file.write(',\n\n'.join('    ' + dim for dim in dimensions))
            file.write('\n\n  },\n\n')

            # Write measures
            file.write('  measures: {\n\n')
            file.write(',\n\n'.join('    ' + measure for measure in measures))
            if measures:
                file.write(',\n\n')
            file.write(f'    count{table_name_camel_case.capitalize()}: {{\n      type: "count"\n    }}\n\n  }}\n')

            # Write the end of the cube
            file.write('});\n\n')
    
    print(f"Base Cube file generated")