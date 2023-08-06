#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Maarten Uijen",
    author_email='maarten.uijen@ordina.nl',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="This calculator gives the n-th fibonacci number, sequence of fibonacci numbers or an index.",
    entry_points={
        'console_scripts': [
            'fibonacci_calculator_onion=fibonacci_calculator_onion.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='fibonacci_calculator_onion',
    name='fibonacci_calculator_onion',
    packages=find_packages(include=['fibonacci_calculator_onion', 'fibonacci_calculator_onion.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/MaartenUijen/fibonacci_calculator_onion',
    version='0.0.3',
    zip_safe=False,
)
