"""
This function accepts a string representation of a database schema and, for each
table and column, uses OpenAI API to extract useful metadata. It determines if
a column is likely a key column, what dimension type it should create, and up to
two potential measures from the column. The result is a nested dictionary providing
insights for each table and column for facilitating semantic layer development in a
data warehouse. The OpenAI API call uses structured conversational templates and
parsing logic to extract the required data.


The ouput dictionary has the following structure:
{
    "Table1": {
        "Column1": {
            "is_key_column": "boolean_value",
            "dimension_type": "dimension_type_value",
            "measure_1_type": "measure_type_value_1",
            "measure_2_type": "measure_type_value_2"
        },
        ...
    },
    ...
}

"""

import os
import json
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import (
    ResponseSchema,
    StructuredOutputParser,
    )
from langchain.prompts import ChatPromptTemplate

def infer_semantics_with_a_large_language_model( schema ):
    
    # Initialize the OpenAI Chat model
    print('Initializing OpenAI Chat model')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    chat = ChatOpenAI(
        temperature=0.0,
        model_name='gpt-3.5-turbo'
    )
    
    print('Setting things up for the OpenAI API call')

    # Prepare the Response Schemas
    is_key_column_schema = ResponseSchema(
        name='is_key_column',
        description="""is the column likely to be a primary, foreign, natural, or surrogate key column? \
        Value should be "true" or "false" (enclosed in double quotes). \
        Look for substrings like 'id', 'pk', 'fk', 'key', 'primary', 'foreign', etc."""
    )
    dimension_type_schema = ResponseSchema(
        name='dimension_type',
        description="""the type of the dimension. \
        The dimension type should be determined by considering: 
            1. the data_type of the column.
            2. the column_name."""
    )
    measure_1_type_schema = ResponseSchema(
        name='measure_1_type',
        description="""the type of the first measure. \
        This should be created if end users (analysts) might create useful \
        analyses through aggregating the values in this column by a certain \
        aggregation (measure type). \
        If a measure made from this column is not appropriate then this field \
        should be "null" (enclosed in double quotes)."""
    )
    measure_2_type_schema = ResponseSchema(
        name='measure_2_type',
        description="""the type of the second measure. \
        Use the same logic as for measure_1_type, but, only if an additional \
        measure would be useful. \
        If a second measure made from this column is not appropriate then this \
        field should be "null" (enclosed in double quotes)."""
    )
    response_schemas = [
        is_key_column_schema,
        dimension_type_schema,
        measure_1_type_schema,
        measure_2_type_schema
    ]
    
    # Initialize the Output Parser
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    
    # Prepare the Cube.js prompt template
    cube_objects_from_schema_template = """\
        The dictionary below details a snowflake schema for a list of tables and their columns. \
        Act as a developer creating a semantic layer in cube.js on top of a data warehouse. \
        I want you to, for the colum_name '{column_name}' of table '{table_name}' (the key of \
        the dictionary) decide:
            1. whether this column is likely to be a primary, foreign, natural, or surrogate key column
            2. which dimension type this column should create
            3. whether it would be useful to create up to two measures from this column and, if \
                so, which measure types to create.

        Follow these rules:
            1. you have choose a dimension type for every column
            2. you can choose between 0 and 2 measure types for every column
            3. the dimension type should be one of the following:
                * string
                * number
                * time
                * boolean
            4. the measure type should be one of the following (listed in order of preference):
                * sum
                * avg
                * count_distinct
                * max
                * min
            5. you should aim to make measures whenever appropriate and preferrably 2. The exception: next rule.
            6. only assign the count_distinct measure type on columns which are likely to be primary, foreign, \
                natural, or surrogate key columns.

        schema: {schema}

        {format_instructions}
        """
    prompt = ChatPromptTemplate.from_template(template=cube_objects_from_schema_template)
    
    # Prepare the result dictionary and load from existing file if it exists
    result = {}
    filepath = "dwa_target/semantics_from_large_language_model.json"
    if os.path.isfile(filepath):
        with open(filepath, 'r') as f:
            if os.stat(filepath).st_size != 0:
                result = json.load(f)

    # Analyze each table and column in the schema
    print(f'Calling the OpenAI API. Whenever possible, using saved result at {filepath}')
    for table_name, columns in schema.items():
        for column in columns:
            column_name = column['column_name']

            # Skip API call if result already exists
            if table_name in result and column_name in result[table_name]:
                continue

            # Prepare the chat messages
            format_instructions = output_parser.get_format_instructions()
            messages = prompt.format_messages(
                table_name=table_name,
                column_name=column_name,
                schema=schema, 
                format_instructions=format_instructions,
            )

            # Get the response from the OpenAI API
            print(f'Calling the OpenAI API for table: {table_name}, column: {column_name}, type: {column["data_type"]}')
            response = chat(messages)

            # Parse the response into a dictionary
            output_dict = output_parser.parse(response.content)
            print(f'OpenAI API response: {output_dict}')

            # Add the output to the result
            if table_name not in result:
                result[table_name] = {}
            result[table_name][column_name] = output_dict

            # Write the result to file after each API call
            with open(filepath, 'w') as f:
                json.dump(result, f, indent=4)

    print('Finished calling the OpenAI API')
    
    return result