# coding: utf-8

import os
import sys
import re

from setuptools import setup, find_packages

def version():
    """retrieve version from tag name"""
    ci_tag = os.getenv('CIRCLE_TAG')

    # Try to parse tag from CI variable, if set write version.txt file with current version
    if ci_tag is not None:
        if re.match('\d+(\.\d+)*', ci_tag):
            with open('version.txt', 'w+') as f:
                f.write(ci_tag)
            return ci_tag
        # Variable is set but format is incorrect, error
        info = "Git tag: `{0}` is not set or does not match the version pattern of this app".format(
            ci_tag
        )
        sys.exit(info)

    # Read version from file
    with open('version.txt') as f:
        return f.read()

def readme():
    """print long description"""
    with open('README.md') as f:
        return f.read()

setup(
    name='coover_thumbor_plugins',
    version=version(),
    description='Thumbor Coover plugins',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='ViZeke & Alvarollmenezes',
    author_email='vizeke@gmail.com',  # Original author email is: willtrking@gmail.com
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='thumbor aws',
    install_requires=[
        'python-dateutil',
        'thumbor>=6.0.0,<7',
        'tornado-botocore',
    ],
    extras_require={
        'tests': [
            'coverage',
            'boto',
            'moto[server]',
            'mock',
            'nose',
        ],
    },
)
