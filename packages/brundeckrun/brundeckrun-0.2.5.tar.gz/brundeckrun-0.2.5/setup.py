__docformat__ = "restructuredtext en"
"""
:summary: Setup script for arundeckrun

:license: Apache License, Version 2.0
:author: Mark LaPerriere
:contact: otupman@antillion.com
:copyright: Mark LaPerriere 2015
"""
import os
from setuptools import setup, find_packages
from rundeck import VERSION

project = 'brundeckrun'
install_requires = ['requests>=2.23.0']

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'README.md'), 'r') as fp:
    long_description = fp.read()

setup(
    name=project,
    license='http://creativecommons.org/licenses/by-sa/3.0/',
    version=VERSION,
    packages=find_packages(exclude=["tests", "tests.*"]),
    
    description='A Rundeck API Python client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/antillion/{0}'.format(project),
    author='rundeckrun@mindmind.com',
    author_email='rundeckrun@mindmind.com',

    maintainer='Lambda Vector',
    maintainer_email='pablo@ceruleanhq.com',

    install_requires=install_requires,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
)
