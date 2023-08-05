""" __Doc__ File handle class """
from setuptools import find_packages, setup

from XOGoogle.__version__ import __version__


def dependencies(imported_file):
    """ __Doc__ Handles dependencies """
    with open(imported_file) as file:
        return file.read().splitlines()


with open("README.md") as file:
    setup(
        name="XOGoogle",
        license="GPLv3",
        description="XOGoogle is a google bot that scraps google for keywords and returns all links",
        long_description=file.read(),
        author="Akhil Reni",
        version=__version__,
        author_email="akhil@wesecureapp.com",
        url="https://strobes.co/",
        packages=find_packages(
            exclude=('tests')),
        python_requires='>=3.6',
        install_requires=[
            "requests==2.24.0",
            "bs4==0.0.1"
        ],
        package_data={
            'XOGoogle': [
                '*.txt',
                '*.json']},
        entry_points={
            'console_scripts': ['xo_google = XOGoogle.xo_google:main']},
        include_package_data=True)
