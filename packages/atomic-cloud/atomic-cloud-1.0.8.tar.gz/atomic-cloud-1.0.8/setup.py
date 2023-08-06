import pathlib
from setuptools import setup, find_packages
import toml

def get_install_requirements():
    try:
        # read my pipfile
        with open ('Pipfile', 'r') as fh:
            pipfile = fh.read()
        # parse the toml
        pipfile_toml = toml.loads(pipfile)
        
    except FileNotFoundError:
        return []

    try:
        required_packages = pipfile_toml['packages'].items()

        # if the package's key isn't there then just return an empty
        # list
        
        # If a version/range is specified in the Pipfile honor it
        # otherwise just list the package
        return ["{0}{1}".format(pkg,ver) 
                if ver != "*" else pkg for pkg,ver in required_packages]

    except KeyError:
        return []

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="atomic-cloud",
    version="1.0.8",
    description="Helper library to automate cloud environment management.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/python-cicd/atomic-cloud",
    author="SimonComputing, Inc.",
    author_email="simon@simoncomputing.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("test", "venv", "doc_build", "doc_source", "build", "dist")),
    include_package_data=True,
    install_requires=get_install_requirements()
)
