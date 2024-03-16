
from setuptools import setup, find_packages

setup(
    name='hammock',
    version='1.0',
    author='Hammad Saeed',
    packages=find_packages(),
    install_requires=[
      'pandas',
      'fastparquet',
      'dask',
      'uuid',
      'colorama',
      'pathlib',
      'numpy',  
        
        ],
)