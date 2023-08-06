from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="ario",
    version="0.6.0",
    packages=find_packages(),
    author="Wish Team",
    description="A Flask-Based Package for Web Development. API Documentation Is Now Available",
    install_requires=required,
    url="https://github.com/wish-team/ario",
    long_description=long_description,
    long_description_content_type='text/markdown'
)
