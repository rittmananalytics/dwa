"""
This module processes a dictionary representing a database schema and removes specified prefixes 
from the table names. The input includes a list of potential prefixes, and the function iteratively 
checks and removes these from each table name. The output is a new dictionary mapping the original 
table names to the adjusted names, facilitating easier reference and more readable code within the 
broader application.

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