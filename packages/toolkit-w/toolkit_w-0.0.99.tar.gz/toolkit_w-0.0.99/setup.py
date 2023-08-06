
#!/usr/bin/env python

import os
import sys

if sys.version_info < (3, 4):
    raise ImportError("Please use python 3.4 or higher")

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
version_contents = {}

with open(os.path.join(here, "toolkit_w", "version.py"), encoding="utf-8") as f:
    exec(f.read(), version_contents)

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='toolkit_w',
    version=version_contents["__version__"],
    description='Python client for Whathif API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Whatify',
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    package_data={'': ['data_source/*.csv']},

    platforms='any',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    tests_require=[
        'pytest==5.4.2'
    ],
    install_requires=[
        "requests==2.20.0",
        "boto3==1.10.39"
    ],
)
