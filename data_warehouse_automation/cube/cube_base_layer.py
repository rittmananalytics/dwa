
"""
This module generates the cube base layer

"""


# def generate_cube(profile_dir, project_dir):
#     print(f'Generating cube syntax for profile {profile_dir} and project {project_dir}')

def generate_cube_js_base_file(tables_columns, file_path):

    # Open the file for writing
    with open(file_path, 'w') as file:
        # Iterate over each table in the dictionary
        for table_name, columns in tables_columns.items():
            # Write the cube definition for the table
            file.write(f'cube(`{table_name}`) {{\n')

            # Initialize dimensions and measures
            dimensions = []
            measures = []

            # Process each column in the table
            for column_info in columns:
                column_name = column_info['column_name']
                data_type = column_info['data_type']

                # Check if the column is a primary key dimension
                if column_name.endswith('_pk') or 'text' in data_type.lower():
                    dimensions.append(f'    `{column_name}`: {{ sql: `{column_name}`, type: "string" }}')
                elif 'number' in data_type.lower():
                    measures.append(f'    `{column_name}`: {{ sql: `{column_name}`, type: "sum" }}')

            # Write dimensions
            file.write('  dimensions: {\n')
            file.write(',\n'.join(dimensions))
            file.write('\n  },\n')

            # Write measures
            file.write('  measures: {\n')
            file.write(',\n'.join(measures))
            if measures:
                file.write(',\n')
            file.write('    count: { type: "count" }\n  }\n')

            file.write('}\n\n')