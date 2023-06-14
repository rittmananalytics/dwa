"""
This module extracts and pairs primary keys (PKs) and foreign keys (FKs) within a schema based
on pre-established naming conventions.

The central function accepts a schema as a dictionary where keys are table names, and the
values are lists of dictionaries. Each dictionary in the list represents a column and contains
the 'column_name' and 'data_type' keys.

The function returns a list of tuples in the following structure:

(pk_table_name, pk_column_name, fk_table_name, fk_column_name)

The function works by iterating over each table and its columns in the schema. It identifies
columns which are primary keys foreign keys. For each primary key, it seeks matching foreign
keys in other tables.

Refer to the project's README 'Assumptions About Your Data Warehouse' section for more information
on the naming conventions and assumptions this module relies on.

"""

def extract_pk_fk_pairs( schema ):
    pk_fk_pairs = []

    # Iterate over each table in the schema
    for table_name, columns in schema.items():
        # Extract primary and foreign keys
        primary_keys = [col['column_name'] for col in columns if col['column_name'].lower().endswith('_pk')]
        foreign_keys = [col['column_name'] for col in columns if col['column_name'].lower().endswith('_fk')]

        # For each PK, find the matching FK in other tables
        for pk in primary_keys:
            pk_prefix = pk.lower().replace('_pk', '')
            for other_table_name, other_table_columns in schema.items():
                if other_table_name != table_name:
                    matching_fks = [col['column_name'] for col in other_table_columns if col['column_name'].lower() == f'{pk_prefix}_fk']
                    for fk in matching_fks:
                        pk_fk_pairs.append({
                            'left_table': table_name,
                            'left_column': pk,
                            'right_table': other_table_name,
                            'right_column': fk
                        })

    print('primary-foreign key pairs identified')

    return pk_fk_pairs

