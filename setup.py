#!/usr/bin/env python
from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

packages = [
    'promptly'
]

requires = ['colorama']

setup(
    name='promptly',
    version='0.4',
    description='Console Prompting',
    long_description=readme,
    author='Aubrey Taylor <aubricus@gmail.com>, Adam Venturella <aventurella@gmail.com>',
    author_email='aubricus@gmail.com, aventurella@gmail.com',
    url='https://github.com/aventurella/promptly',
    license=license,
    packages=packages,
    package_data={'': ['LICENSE'],
                  'promptly': ['resources/*.*']},
    include_package_data=True,
    install_requires=requires,
    package_dir={'promptly': 'promptly'},
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
