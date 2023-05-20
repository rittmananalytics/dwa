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
The `main()` function is located in `data_warehouse_automation/input/parser_setup.py`
* This is the entry point of the package
* It also that orchestrates all other function
* When a `dwa` command is run, this function kicks off initially
  * this is determined by `setup.console_scripts` in `setup.py`
* Start there if you are looking to understand the project