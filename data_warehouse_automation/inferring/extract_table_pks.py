def extract_table_pks(schema):
    table_pks = {}

    # Iterate over each table in the schema
    for table_name, columns in schema.items():
        # Extract primary keys
        primary_keys = [col['column_name'] for col in columns if col['column_name'].lower().endswith('_pk')]
        # If there are primary keys, add them to the dictionary
        if primary_keys:
            table_pks[table_name] = primary_keys

    return table_pks
