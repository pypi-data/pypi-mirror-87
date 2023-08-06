====================
Fibonacci Calculator
====================


.. image:: https://img.shields.io/pypi/v/fibonacci_calculator.svg
        :target: https://pypi.python.org/pypi/fibonacci_calculator

.. image:: https://img.shields.io/travis/richardscholtens/fibonacci_calculator.svg
        :target: https://travis-ci.org/richardscholtens/Fibonacci_Calculator

.. image:: https://readthedocs.org/projects/fibonacci-calculator/badge/?version=latest
        :target: https://fibonacci-calculator.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/richardscholtens/Fibonacci_Calculator/shield.svg
     :target: https://pyup.io/repos/github/richardscholtens/Fibonacci_Calculator/
     :alt: Updates


A calculator that calculates Fibonacci numbers from 0 to n, indexes n-number and returns n-number.


* Free software: MIT license
* Documentation: https://fibonacci-calculator.readthedocs.io.


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


Cython modules
-------

If one wants to use the Cython modules one has to make use of the Cython library:

https://cython.readthedocs.io/en/latest/
https://cython.readthedocs.io/en/latest/src/tutorial/cython_tutorial.html

EXAMPLE:

import pyximport
pyximport.install()


from fibonacci_calculator.fibonacci_calculator_cython import FibonacciSequence

print(FibonacciSequence())

