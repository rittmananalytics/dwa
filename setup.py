from setuptools import setup, find_packages

setup(
    name='data_warehouse_automation',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyyaml',
        'snowflake-connector-python',
    ],
    entry_points={
        'console_scripts': [
            'dwa = data_warehouse_automation.input.parser_setup:main',
        ],
    },
)
