#!/usr/bin/env python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    # basic
    name='tool-registry-client',
    version='0.1.0',
    # packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    # py_modules=['hello'],
    # scripts=['bin/nlp-evaluate'],

    packages=setuptools.find_packages(),
    entry_points={
        # 'console_scripts': ['rocc-cli=roccclient.cli.__main__:main']
    },

    # requirements
    python_requires='>=3.6.*',
    install_requires=[
        'click>=7.1.2',
        'jsonschema>=3.2.0',
        'synapseclient>=2.2.0'
    ],

    # metadata to display on PyPI
    description='Tool Registry Library for Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Sage-Bionetworks/tool-registry-client',
    author='The Tool Registry Team',
    author_email='thomas.schaffter@sagebionetworks.org',
    license='Apache',
    project_urls={
        "Source Code": "https://github.com/Sage-Bionetworks/tool-registry-client",  # noqa: E501
        "Bug Tracker": "https://github.com/Sage-Bionetworks/tool-registry-client/issues",  # noqa: E501
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ]
)
