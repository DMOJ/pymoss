import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymoss",
    version="0.0.4",
    author="Tudor Brindus",
    author_email="me@tbrindus.ca",
    description="Library for interfacting with Stanford MOSS.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DMOJ/pymoss",
    keywords=['moss', 'plagarism-detection'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
)
