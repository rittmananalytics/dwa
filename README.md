# dwa
Data Warehouse Automation

## How to develop
1. clone this repo
1. create a branch
1. make changes and save your files
1. test your changes by installing your local files as a package
    * `pip3 install -e /path/to/dwa`
    * note: the `-e` flag means that you don't need to re-install on subsequent changes
        * unless you change the `version` in `setup.py`
5. raise a PR into `main`
    * get approval, then I'll merge

## Project architecture
The `main()` function is located in `data_warehouse_automation/parser/parser_setup.py`
* This is the entry point of the package
* When you run a `dwa` command, this function is run
* Start there if you are looking to understand the project