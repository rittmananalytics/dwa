"""
This function simplifies table naming within a database schema
dictionary by removing certain specified prefixes from the table
names. The function takes a dictionary representation of a schema
as input and returns a new dictionary with original table names
mapped to their simplified counterparts.

The dictionary output has the following format:
{
    'original_table_name': 'simplified_table_name',
    ...
}

"""

def remove_prefixes_from_table_names( schema_dict ):

    prefixes = [
        'dim_',
        'fact_',
        'fct_',
        'xa_',
        'obt_',
        ]

    result = {}
    for table_name in schema_dict.keys():
        extracted_table_name = table_name.lower()
        for prefix in prefixes:
            if extracted_table_name.startswith(prefix):
                extracted_table_name = extracted_table_name[len(prefix):]
                break
        result[table_name] = extracted_table_name.upper()
    return result