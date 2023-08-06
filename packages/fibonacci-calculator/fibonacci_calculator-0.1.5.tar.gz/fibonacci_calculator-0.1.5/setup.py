#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

from Cython.Build import cythonize
# import numpy as np
from distutils.extension import Extension

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

exts = [Extension("fibonacci_calculator.fibonacci_calculator", ["fibonacci_calculator/fibonacci_calculator_cython.pyx"])]
ext_options = {"compiler_directives": {"profile": True}, "annotate": True}

setup(
    author="Richard Scholtens",
    author_email='richardscholtens2@gmail.com',
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
    description="Fibonacci Calculator including normal Python code and Cython wrapper.",
    entry_points={
        'console_scripts': [
            'fibonacci_calculator=fibonacci_calculator.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='fibonacci_calculator',
    name='fibonacci_calculator',
    packages=find_packages(include=['fibonacci_calculator', 'fibonacci_calculator.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/richardscholtens/Fibonacci_Calculator',
    version='0.1.5',
    zip_safe=False,
    # ext_modules=cythonize(["fibonacci_calculator/__init__.pyx"]),
    ext_modules=cythonize(exts, **ext_options),
    # include_dirs=np.get_include(),
)
