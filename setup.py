import os

import setuptools


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as fh:
    long_description = fh.read()

setuptools.setup(
    py_modules=['moss'],
    name='pymoss',
    version='0.2',
    author='Tudor Brindus',
    author_email='me@tbrindus.ca',
    description='Library for interfacting with Stanford MOSS.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DMOJ/pymoss',
    keywords=['moss', 'plagarism-detection'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
    ],
)
