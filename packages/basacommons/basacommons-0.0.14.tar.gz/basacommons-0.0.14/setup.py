from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'Readme.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='basacommons',
    version='0.0.14',
    packages=find_packages(),
    python_requires='>=3.7',
    author='Enrique Basañez Mercader',
    author_email='enrique.basanez@gmail.com',
    url='https://github.com/ebasanez/python-commons',
    description='Basic project utilities',
    long_description=long_description,
    long_description_content_type='text/markdown'
    )