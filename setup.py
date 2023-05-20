from setuptools import setup, find_packages

setup(
    name='data_warehouse_automation',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dwa = data_warehouse_automation.parser.parser_setup:main',
        ],
    },
)
