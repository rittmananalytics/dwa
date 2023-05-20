"""
this module queries the database to establish the information schema 

"""

import snowflake.connector

def query_snowflake_tables_and_columns(user, password, account, warehouse, database, schema):
    
    # connect to snowflake
    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema
    )

    # execute the query to retrieve table and column information
    query = f"""
    select table_name, column_name
    from information_schema.columns
    where table_schema = '{schema}'
    and table_catalog = '{database}'
    """
    cursor = conn.cursor()
    cursor.execute(query)

    # create a dictionary to store the table and column information
    tables_columns = {}

    # process the query results
    for table_name, column_name in cursor:
        # check if the table name exists in the dictionary
        if table_name not in tables_columns:
            tables_columns[table_name] = []

        # append the column name to the list of columns for the table
        tables_columns[table_name].append(column_name)

    # close the connection
    cursor.close()
    conn.close()

    return tables_columns
