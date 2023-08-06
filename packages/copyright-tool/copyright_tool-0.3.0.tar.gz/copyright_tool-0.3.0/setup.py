#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ "GitPython>=3.1.11", "gitignore-parser>=0.0.8" ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Steve Graham",
    author_email='stgraham2000@gmail.com',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Use to scan your git repo and add/update copyrights to files of various language types.",
    entry_points={
        'console_scripts': [
            'copyright_tool=copyright_tool.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description="Use to scan your git repo and add/update copyrights to files of various language types.",
    include_package_data=True,
    keywords='copyright_tool',
    name='copyright_tool',
    packages=find_packages(include=['copyright_tool', 'copyright_tool.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/stgraham2000@gmail.com/copyright_tool',
    version='0.3.0',
    zip_safe=False,
)
