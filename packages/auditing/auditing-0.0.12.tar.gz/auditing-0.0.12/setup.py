import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="auditing",
    version="0.0.12",
    description="A simple auditing library intended for use with Flask-based applications",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    author="Emil Haldrup Eriksen",
    author_email="emil.h.eriksen@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=["auditing"],
    include_package_data=True,
    install_requires=["flask", "numpy", "psycopg2-binary", "elasticsearch"],
)
