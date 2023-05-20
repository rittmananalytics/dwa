
"""
This module generates the cube base layer

"""

def to_camel_case(name):
    components = name.split('_')
    return components[0].lower() + ''.join(x.title() for x in components[1:])

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
            file.write(',\n\n'.join(dimensions))
            file.write('\n\n  },\n\n')

            # Write measures
            file.write('  measures: {\n\n')
            file.write(',\n\n'.join(measures))
            if measures:
                file.write(',\n\n')
            file.write(f'    count{table_name_camel_case.capitalize()}: {{ type: "count" }}\n\n  }}\n')

            # Write the end of the cube
            file.write('});\n\n')
