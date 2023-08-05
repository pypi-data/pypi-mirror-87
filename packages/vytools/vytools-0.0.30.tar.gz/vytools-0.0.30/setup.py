#!/usr/bin/env python
import setuptools, re

try:
    with open('README.md','r') as f:
        readme = f.read()
except Exception as exc:
    readme = ''

setuptools.setup(name='vytools',
    description='Tools for working with vy',
    long_description=readme,
    license='MIT',
    author='Nate Bunderson',
    author_email='nbunderson@gmail.com',
    url='https://github.com/NateBu/vyengine',
    keywords = ["meteor", "ddp", "vy", "vytools"],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Other/Nonlisted Topic"
    ],
    python_requires='>=3.5',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'pyyaml',
        'termcolor',
        'cerberus',
        'python-ddp',
        'argcomplete'
    ],
    entry_points={
        'console_scripts':[
            'vytools=vytools._commandline:main'
        ]
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)

