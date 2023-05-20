
"""
This module generates the cube base layer

"""

# Convert a string to camel case
def to_camel_case(name):
    components = name.split('_')
    return components[0].lower() + ''.join(x.title() for x in components[1:])

# Function to add new lines and indentation to a dictionary string
def format_dict_string(dict_string):
    parts = dict_string.split('{ ', 1)  # Split at the first squiggkly bracket after a dimension or measure name
    parts[1] = parts[1].rstrip('}') # remove closing squiggly bracket of each dimension or measure
    parts[1] = parts[1].replace(', ', ',\n      ')  # Replace every comma in a dimension or measure with a comma followed by a newline
    formatted_parts = [parts[0] + '{\n      ' + parts[1] + '\n    }']
    return ''.join(formatted_parts)

def generate_cube_js_base_file(tables_columns, file_path):

    # Open the file for writing
    with open(file_path, 'w') as file:
        # Write the import statement at the top of the file
        file.write('import { databaseSchema, databaseName } from \'../tablePrefix\';\n\n')

        # Iterate over each table in the dictionary
        for table_name, columns in tables_columns.items():
            # Write the cube definition for the table
            table_name_camel_case = to_camel_case(table_name)
            file.write(f'cube(`{table_name_camel_case}`, {{\n\n')

            file.write(f'  sql: `SELECT * FROM ${{databaseName()}}.${{databaseSchema()}}."{table_name}"`,\n\n')

            file.write('  shown: false,\n\n')

            # Initialize dimensions and measures
            dimensions = []
            measures = []

            # Process each column in the table
            for column_info in columns:
                column_name = column_info['column_name']
                data_type = column_info['data_type']
                column_name_camel_case = to_camel_case(column_name)

                # Check if the column is a primary key dimension
                if column_name.lower().endswith('_pk'):
                    dimensions.append(f'{column_name_camel_case}: {{ sql: `${{CUBE}}."{column_name}"`, type: "string", primaryKey: true }}')
                elif 'text' in data_type.lower():
                    dimensions.append(f'{column_name_camel_case}: {{ sql: `${{CUBE}}."{column_name}"`, type: "string" }}')
                elif 'number' in data_type.lower():
                    measures.append(f'sum{column_name_camel_case.capitalize()}: {{ sql: `${{CUBE}}."{column_name}"`, type: "sum" }}')

            # Write dimensions
            file.write('  dimensions: {\n\n')
            print(dimensions)
            formatted_dimensions = [format_dict_string(dim) for dim in dimensions]
            file.write(',\n\n'.join('    ' + dim for dim in formatted_dimensions))
            # for dim in formatted_dimensions:
            #     print(format_dict_string(dim))
            #     print(dim)
            file.write('\n\n  },\n\n')

            # Write measures
            file.write('  measures: {\n\n')
            formatted_measures = [format_dict_string(measure) for measure in measures]
            file.write(',\n\n'.join('    ' + measure for measure in formatted_measures))
            if measures:
                file.write(',\n\n')
            file.write(f'    count{table_name_camel_case.capitalize()}: {{\n      type: "count"\n    }}\n\n  }}\n')

            # Write the end of the cube
            file.write('});\n\n')