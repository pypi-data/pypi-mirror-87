#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    'numpy>=1.18',
    'scipy>=1.4.0',
    'smart_open',
    'requests',
    'bs4'
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Software Engineering Laboratory of Fudan University",
    author_email='lmwtclmwtc@outlook.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="provide a wrapper to access Stack Overflow tag data.",
    entry_points={
        'console_scripts': [
            'sotag=sotag.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='sotag',
    name='sotag',
    packages=find_packages(include=['sotag', 'sotag.*']),
    package_data={
        # If any package contains *.json files, include them:
        'sotag': ["download/*.zip"],
    },
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/FudanSELab/sotag',
    version='0.1.1',
    zip_safe=False,
)
