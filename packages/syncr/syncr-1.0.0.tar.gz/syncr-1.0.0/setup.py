from os.path import dirname, abspath, join
from setuptools import setup

NAME: str = "syncr"
AUTHOR: str = "Saadman Rafat"
DESCRIPTION: str = "Site Backup Tool"
URL: str = "https://github.com/saadmanrafat/syncr"
REQUIRES_PYTHON: str = ">=3.6.0"
VERSION = "1.0.0"
REQUIRED = ["boto3"]
EMAIL = "saadmanhere@gmail.com"

with open(join(abspath(dirname(__file__)), "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=NAME,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    license="MIT",
    install_requires=REQUIRED,
    include_package_data=True,
    py_modules=["syncr"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)