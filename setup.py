from setuptools import setup, find_packages

setup(
    name='data_warehouse_automation',
    version='0.9.0',
    packages=find_packages(),
    install_requires=[
        'langchain',
        'openai',
        'pyyaml',
        'snowflake-connector-python',
    ],
    entry_points={
        'console_scripts': [
            'dwa = data_warehouse_automation.main:main',
        ],
    },
)
