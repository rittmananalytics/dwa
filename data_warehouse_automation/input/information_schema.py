"""
this module queries the database to establish the information schema.

It returns
* a list of dictionaries with table and column names as well as the column types
* the snowflake connection object 

"""

import snowflake.connector

def query_snowflake_tables_and_columns(
    account,
    database,
    password,
    role,
    schema,
    user,
    warehouse,
    ):
    
    print("Acquiring database credentials")
    
    # Connect to Snowflake
    conn = snowflake.connector.connect(
        account=account,
        database=database,
        password=password,
        role=role,
        schema=schema,
        user=user,
        warehouse=warehouse,
    )

    # Execute the query to retrieve table and column information
    query = f"""
    select
        table_name,
        column_name,
        data_type
    
    from {database}.information_schema.columns
    
    where 1=1
        and lower( table_schema ) = lower( '{schema}' )
        and lower( table_catalog ) = lower( '{database}' )

    order by 1, 2, 3
    """

    print(f"Connecting to database {database}")
    cursor = conn.cursor()

    print(f"Querying information schema of {schema}")
    cursor.execute(query)

    # Create a dictionary to store the table and column information
    tables_columns = {}

    # Process the query results
    print("Parsing query result")
    for table_name, column_name, data_type in cursor:
        # Check if the table name exists in the dictionary
        if table_name not in tables_columns:
            tables_columns[table_name] = []

        # Append a dictionary with column name and data type to the list of columns for the table
        column_info = {"column_name": column_name, "data_type": data_type}
        tables_columns[table_name].append(column_info)

    return tables_columns, conn