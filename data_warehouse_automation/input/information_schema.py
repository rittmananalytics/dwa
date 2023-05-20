"""
this module queries the database to establish the information schema 

"""

import snowflake.connector

def query_snowflake_tables_and_columns(user, password, account, warehouse, database, schema):
    
    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema
    )

    # Execute the query to retrieve table and column information
    query = f"""
    select table_name, column_name, data_type
    from information_schema.columns
    where table_schema = '{schema}'
    and table_catalog = '{database}'
    """
    cursor = conn.cursor()
    cursor.execute(query)

    # Create a dictionary to store the table and column information
    tables_columns = {}

    # Process the query results
    for table_name, column_name, data_type in cursor:
        # Check if the table name exists in the dictionary
        if table_name not in tables_columns:
            tables_columns[table_name] = []

        # Append a dictionary with column name and data type to the list of columns for the table
        column_info = {"column_name": column_name, "data_type": data_type}
        tables_columns[table_name].append(column_info)

    # Close the connection
    cursor.close()
    conn.close()

    return tables_columns
