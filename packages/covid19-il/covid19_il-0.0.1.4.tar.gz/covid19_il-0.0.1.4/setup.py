import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="covid19_il",
    version="0.0.1.4",
    description='python package which brings a "Facade" interface for using official covid19 israeli data gov data.',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/natylaza89/covid19-il",
    author="Naty Laza",
    author_email="natylaza89@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(include=['covid19_il.*']),
    include_package_data=True,
    install_requires=[
        "numpy>=1.19.2,<2",
        "pandas>=1.1.2,<2",
        "requests>=2.24.0,<3"
    ])
