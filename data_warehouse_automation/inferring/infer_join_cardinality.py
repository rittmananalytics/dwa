import os
import json
import snowflake.connector
import time

def infer_join_cardinality(connection, pk_fk_pairs, table_pks, join_query_time_threshold):
    # Specify the output directory and file path
    output_dir = "dwa_target"
    output_file_path = os.path.join(output_dir, "inferred_join_cardinalities.json")

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the existing results if the output file exists
    existing_results = []
    if os.path.exists(output_file_path):
        with open(output_file_path, "r") as f:
            existing_results = json.load(f)

    # Create a dictionary to store the existing results for quick lookup
    existing_results_dict = {(r['left_table'], r['left_column'], r['right_table'], r['right_column']): r for r in existing_results}

    cardinalities = []

    print(f'Inferring relationships. Whenever possible, using saved ones at {output_file_path}')

    for pair in pk_fk_pairs:
        left_table = pair['left_table']
        left_column = pair['left_column']
        left_table_pk = table_pks[left_table][0]
        right_table = pair['right_table']
        right_column = pair['right_column']
        right_table_pk = table_pks[right_table][0]

        # Check if the pair already exists in the existing results
        if (left_table, left_column, right_table, right_column) in existing_results_dict:
            # If so, skip the current loop
            print(f'Inferred relationship already saved for: {pair}')
            continue

        print(f'Attempting to infer join by querying: {pair}')

        # Construct the SQL query to infer the join cardinality
        query = f"""
        with
        join_and_count_partitioned as (
            select
                count(*) over (partition by t1.{left_table_pk}) as count_by_t1_key,
                count(*) over (partition by t2.{right_table_pk}) as count_by_t2_key
            from {left_table} as t1
            join {right_table} as t2
            on t1.{left_column} = t2.{right_column}
        ),
        check_for_fan_out as (
            select
                max(count_by_t1_key) > 1 as is_many_t2,
                max(count_by_t2_key) > 1 as is_many_t1
            from join_and_count_partitioned
        ),
        derive_cardinality as (
            select
                case
                    when is_many_t1 = true and is_many_t2 = true then 'many_to_many'
                    when is_many_t1 = true and is_many_t2 = false then 'many_to_one'
                    when is_many_t1 = false and is_many_t2 = true then 'one_to_many'
                    else 'one_to_one'
                end as table1_to_table2_cardinality
            from check_for_fan_out
        )
        select * from derive_cardinality
        """

        print(f"query: {query}")

        # Execute the query and measure the elapsed time
        start_time = time.time()
        cur = connection.cursor()
        cur.execute(query)
        elapsed_time = time.time() - start_time

        if elapsed_time > join_query_time_threshold:
            print(f"Warning: Query for ({left_table}, {left_column}) and ({right_table}, {right_column}) took longer than the threshold.")
            cardinalities.append({
                'left_table': left_table,
                'left_column': left_column,
                'right_table': right_table,
                'right_column': right_column,
                'exceeded_threshold': True
            })
            continue

        # Fetch the cardinality result and append it to the cardinalities list
        cardinality = cur.fetchone()
        cardinalities.append({
            'left_table': left_table,
            'left_column': left_column,
            'right_table': right_table,
            'right_column': right_column,
            'cardinality': cardinality,
            'exceeded_threshold': False
        })

    # Update the existing results with the new cardinalities
    existing_results.extend(cardinalities)

    # Remove any pairs that are no longer present in pk_fk_pairs
    # but without the 'cardinality' and 'exceeded_threshold' keys since they do not exist in pk_fk_pairs
    pk_fk_pairs_dict_format = [{'left_table': pair['left_table'], 
                                'left_column': pair['left_column'], 
                                'right_table': pair['right_table'], 
                                'right_column': pair['right_column']} for pair in pk_fk_pairs]

    # Filter existing_results, keeping only those entries which are also present in pk_fk_pairs_dict_format
    existing_results = [r for r in existing_results if {k: r[k] for k in ['left_table', 'left_column', 'right_table', 'right_column']} in pk_fk_pairs_dict_format]

    # Save the updated results to the output file
    with open(output_file_path, "w") as f:
        json.dump(existing_results, f, indent=4)

    return cardinalities
