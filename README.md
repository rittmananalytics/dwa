# dwa
Data Warehouse Automation


## How to develop
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


## Project architecture

### Overall
The `main()` function is located in `data_warehouse_automation/main.py`
* This is the entry point of the package
* It also that orchestrates all other function
* When a `dwa` command is run, this function kicks off initially
  * this is determined by `setup.console_scripts` in `setup.py`
* Start there if you are looking to understand the project


## Usage
The `dwa --help` or `dwa -h` commands show the available sub-commands.


### `dwa cube`
The `cube` module queries your Snowflake database and generates a `base.js` file with syntax for`Cubes` compatible with the program previously named cube.js
* the command to do this is `dwa cube`
* the idea is that you automate the generation of most `dimensions` and `measures`. If the automatic configuration gets something wrong you can overwrite it with `extend`s.
* use `dwa cube -h` to see optional arguments


## Configuration
Before running the program you need at least two files
### project.yml
This should be stored at the top of your repo
```yml
profile: profile_name # this should match the name in `profile.yml'
cube_path: cube/schema # this is where your cube output file will be

field_description_path: warehouse_docs # if you have dbt-compatible field descriptions in doc blocs, this is the folder within your repo in which the file is
field_description_file_name: field_descriptions.md # and this is the file name
```

### profile.yml
This should be stored in a `.droughty/`folder at the top of your repo
```yml
profile_name:
  account: va83945.eu-west-1.aws
  password: hunter2
  schema_name: YOURS_SCHEMA
  user: amir
  warehouse: your_warehouse
  database: YOUR_DATABASE_NAME
  warehouse_name: snowflake
```