from setuptools import setup, find_packages
import os
import codecs

def load_requirements(req_file):
    with open(req_file, 'r') as f:
        requirements = f.read().splitlines()

    # filter commented reqs
    requirements = [r for r in requirements if not r.startswith('#')]

    # filter empty reqs
    requirements = [r for r in requirements if r]

    return requirements

def get_version(rel_path):
    """
    https://packaging.python.org/guides/single-sourcing-package-version/
    """
    def read(rel_path):
        """
        https://packaging.python.org/guides/single-sourcing-package-version/
        """
        here = os.path.abspath(os.path.dirname(__file__))
        with codecs.open(os.path.join(here, rel_path), 'r') as fp:
            return fp.read()

    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name="celebrate",
    version=get_version('celebrate/__init__.py'),
    packages=find_packages(),
    install_requires=load_requirements('requirements.txt'),
    author="Jonny Saunders",
    author_email="j@nny.fyi",
    license="MPL-2.0"
)