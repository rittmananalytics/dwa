# dwa - Data Warehouse Automation

This project automates work that is based on values in your cloud data warehouse (dwh). Currently, it supports:
* dwh
  * Snowflake
* output
  * cube (formely cube.js) semantic files

This is a work in progress. If you'd like to make changes to make this suitable for your workflow, see `contribute`.

## Demo: generate `Cube` code based on an `information_schema`

![dwa_cube_demo](media/dwa_cube_demo.gif)


## Usage
1. Configure your project and connections (see `configuration`)
2. Install `dwa` (see `how to develop`)
3. Navigate to your analytics repo
4. Run one of the available cli commands. For more detail on how these commands work, see `project architecture`. But, at a high level:
    * `dwa --help` and `dwa -h` show the available sub-commands
    * `dwa cube` generates `Cube` (previously `cube.js`) code based on an `information_schema`

## Configuration
Before running the program you need at least two files
### project.yml
This should by default be stored at the top of your repo
* but can be overwritten by the optional `project_dir` argument at runtime
```yml
profile: profile_name # this should match the name in `profiles.yml'
cube_path: cube/schema # this is where your cube output file will be

field_description_path: warehouse_docs # if you have dbt-compatible field descriptions in doc blocs, this is the folder within your repo in which the file is
field_description_file_name: field_descriptions.md # and this is the file name
```

### profiles.yml
This should by default be stored in a `.dwa/` folder in the user's home directory
* but can be overwritten by the optional `profile_dir` argument at runtime
```yml
profile_name:
  account: va83945.eu-west-1.aws
  password: hunter2
  schema_name: your_schema
  user: amir
  warehouse: your_warehouse
  database: your_database_name
  warehouse_name: snowflake
```

## Assumptions About Your Data Warehouse

The `dwa cube` tool works best when your data warehouse follows certain conventions. These conventions allow `dwa cube` to infer table relationships and generate accurate Cube.js schema files:

1. **Primary Key (PK) Suffixes**: `dwa cube` assumes that the primary keys in your tables are suffixed with `_pk`. For example, the primary key for a table named `orders` should be named `order_pk`.

2. **Foreign Key (FK) Suffixes**: Similarly, `dwa cube` assumes that foreign keys are suffixed with `_fk`. For example, a foreign key linking to the `orders` table should be named `order_fk`.

3. **Table Name Prefixes and Suffixes**: `dwa cube` assumes that your table names may have various prefixes (like `fact_`, `dim_`, `xa_`) and are suffixed with the plural form of the primary key prefix. For example, a fact table linked to the `orders` table may be named `fact_orders`.

4. **Foreign Key Naming**: `dwa cube` assumes that a foreign key will have the exact same name as the primary key it refers to, except for the suffix. For example, the foreign key referring to `order_pk` would be named `order_fk`.

These conventions are not strictly required for `dwa cube` to function, but adhering to them can greatly improve the accuracy of the generated Cube.js schema. If your database does not follow these conventions, `dwa cube` may not infer the correct relationships between your tables, and you may need to manually adjust the generated schema.

Note that if `dwa cube` isn't getting the configurations right, you can easily modify them with Cube.js's `extend` functionality for more granular control. 

For larger databases, the process of inferring joins might take a considerable amount of time. For this reason, you have the option to enable or disable the join inference feature. This can be done by specifying it in the `project.yml` configuration file. 

Additionally, you can specify a warning threshold for the maximum allowed time for a single join inference query. If a query takes longer than this threshold, a warning will be printed to the terminal and the table pair will be skipped for join inference. The names of such tables are saved in a configuration file and are skipped in subsequent runs to avoid repeating long-running queries. This configuration can also be set in the `project.yml` configuration file. 

Please refer to the `Configuration` section for more details on how to adjust these settings.

## Contribute
Anyone is welcome to contribute to this project. The sections below detail some information you might need to help you get started. If anything is unclear, please reach out by creating an issue or suggestion in github.

###  How to develop
1. clone this repo
2. create a branch
3. make changes and save your files. Some dev tips:
    *  To add a new non-native python package, add it to `setup.install_requires` in `setup.py`
4. test your changes by installing your local files as a package
    * `pip3 install -e /path/to/dwa`
    * note: the `-e` flag means that you don't need to re-install on subsequent changes
        * unless you change the `version` in `setup.py`
5. raise a PR into `main`
    * get approval, then I'll merge


### Project architecture


#### `main.py`
This project starts with the `main()` function in `data_warehouse_automation/main.py`. This function is the entry point of the package and orchestrates the interaction between all other functions. When a `dwa` command is run, the `main()` function is triggered first, serving as the initiation point for the rest of the program. If you are new to the project and trying to understand how everything fits together, starting with `main()` is your best bet.

The below line of code in `main.py` makes it executable as a standalone script and also usable as a module.

```python
if __name__ == "__main__":
    main()
```


#### `dwa cube`

The `cube` module is responsible for connecting with your Snowflake database, gathering schema information, and using this data to generate a `base.js` file. This file follows the Cube.js syntax and contains predefined `dimensions` and `measures` for your data.

This feature enables you to have a dynamically updated schema file for Cube.js that reflects your current Snowflake schema, minimizing manual intervention and reducing error. If the module doesn't get the configurations right, you can easily modify them with cube's `extend` functionality.

Under the hood, the `generate_cube_js_base_file()` function orchestrates this process. This function takes in table and column information from the database and a target file path for the output file. It then processes each table and its respective columns, applying specific rules based on the data types of the columns to create dimensions and measures for the Cube.js schema:

- If the column name ends with `'_pk'` (indicating it's likely a `primary key`) or if its data type is `string`-like (such as `'text'`, `'varchar'`, `'string'`, etc.), it's defined as a `string` dimension in Cube.js.
- Numeric columns (like `'number'`, `'numeric'`, `'float'`, etc.) are defined as `sum` measures.
- `Date`, `time`, and `timestamp` type columns are defined as `time` dimensions.
- `Boolean` type columns are created as `boolean` dimensions.

The function auto-generates these configurations, but you can easily override them using Cube.js's `extend` functionality for more granular control.

This module is initiated by running the `dwa cube` command. The aim of this module is to automate the creation of a Cube.js schema file. If the module doesn't get the configurations right, you can easily modify them with cube's `extend` functionality.

For more details and to view optional arguments, use the `dwa cube -h` command.