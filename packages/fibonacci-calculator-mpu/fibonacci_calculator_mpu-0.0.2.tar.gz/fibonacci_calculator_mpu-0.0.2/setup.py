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
    description="First PyPi package. Fibonacci Calculator. ",
    entry_points={
        'console_scripts': [
            'fibonacci_calculator_mpu=fibonacci_calculator_mpu.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='fibonacci_calculator_mpu',
    name='fibonacci_calculator_mpu',
    packages=find_packages(include=['fibonacci_calculator_mpu',
                                    'fibonacci_calculator_mpu/Calculator',
                                    'fibonacci_calculator_mpu/Decorators',
                                    'fibonacci_calculator_mpu.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/MaartenUijen/fibonacci_calculator_mpu',
    version='0.0.2',
    zip_safe=False,
)
