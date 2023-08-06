from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="ario",
    version="0.6.3",

    packages=find_packages(),
    package_data={
        # If any package contains *.html or *.css files, include them:
        "document": ["*.html", "*.css"],
        # And include any *.msg files found in the "hello" package, too:
    },
    author="Wish Team",
    description="A PYTHON Micro-Framework For Web Development. API Documentation Is Now Available.",
    install_requires=required,
    url="https://github.com/wish-team/ario",
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True
)
