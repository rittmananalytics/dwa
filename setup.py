from setuptools import setup, find_packages

setup(
    name='dwa (Data Warehouse Automation)',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dwa = mymodule.myscript:main',
        ],
    },
)
