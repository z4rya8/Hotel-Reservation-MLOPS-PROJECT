from setuptools import setup, find_packages
# setuptools (extends distutils library) library helps in distributing and and packaging
# setup func provides meta data config file (name, version, packages,(directories containing __init__.py files)  )
# find_packages func is a helper utility by setuptools automatically discovers Python packages within a project's directory structure. Instead of manually listing each package in the packages argument of setup(), find_packages() can be used to automatically identify all directories containing an __init__.py file (which signifies a Python package).

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="MLOPS-PRoject-1",
    version ="0.1",
    author="Zaryab Khan",
    packages=find_packages(),
    install_requires= requirements,
)


