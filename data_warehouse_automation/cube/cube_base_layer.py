
"""
This module generates the cube base layer

"""

# Convert a string to camel case
def to_camel_case(name):
    components = name.split('_')
    return components[0].lower() + ''.join(x.title() for x in components[1:])

def generate_cube_js_base_file(tables_columns, file_path):

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

            # Initialize dimensions and measures
            dimensions = []
            measures = []

            # Process each column in the table
            for column_info in columns:
                column_name = column_info['column_name']
                data_type = column_info['data_type']
                column_name_camel_case = to_camel_case(column_name)

                # Prep column's attributes based on rules
                if column_name.lower().endswith('_pk'): # Primary Key
                    dimensions.append(f'{column_name_camel_case}: {{\n      sql: `${{CUBE}}."{column_name}"`,\n      type: "string",\n      primaryKey: true \n    }}')
                elif 'text' in data_type.lower(): # Other string
                    dimensions.append(f'{column_name_camel_case}: {{\n      sql: `${{CUBE}}."{column_name}"`,\n      type: "string" \n    }}')
                elif 'number' in data_type.lower(): # Numbers
                    measures.append(f'sum{column_name_camel_case.capitalize()}: {{\n      sql: `${{CUBE}}."{column_name}"`,\n type: "sum" \n    }}')
            
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