#!/usr/bin/env python

"""Tests for `fibonacci_calculator` package."""

import time
import pytest

from click.testing import CliRunner

from fibonacci_calculator import fibonacci_calculator
from fibonacci_calculator import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'fibonacci_calculator.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_increase_sequence_length() -> None:
    """"
    Good test case
    - Test if get_sequence function returns a list.
    - Test if every item in list is a sum of two previous numbers.
    - Test if elements of sequence are integers.
    - Test if the list holds more than one element and no duplicates.
    - Test if the length of the list is the same as the given input.
    """
    fibnum = fibonacci_calculator.FibonacciSequenceService()
    fibnum.increase_sequence_length(13)
    sequence = fibnum.get_sequence()
    assert type(sequence) == type([])
    sequence.reverse()
    for count in range(len(sequence)-2):
        assert sequence[count] == sequence[count + 1] + sequence[count + 2]
        assert type(sequence[count]) == type(0)
    assert len(set(sequence[2:])) > 1
    assert len(sequence) == 13


def test_get_sequence_bad() -> None:
    """"
    Bad test case
    - Test how function handles TypeErrors.
    - Test if output of function is not a string.
    - Test if output of function is not an integer.
    - Test if output of function is not an dictionary.
    """
    fibnum = fibonacci_calculator.FibonacciSequenceService()
    fibnum.increase_sequence_length('hello')
    sequence = fibnum.get_sequence()

    assert type(sequence) != type('string')
    assert type(sequence) != type(203)
    assert type(sequence) != type(dict())


def test_get_nth() -> None:
    """"
    Good test case
    - Test if get_nth function returns an integer.
    """
    fibnum = fibonacci_calculator.FibonacciSequenceService()
    fibnum.increase_sequence_length(16)
    number = fibnum.get_nth(16)
    assert type(number) == type(0)


def test_get_nth_bad() -> None:
    """
    Bad test case
    - Test if get_nth function returns an integer.
    """
    fibnum = fibonacci_calculator.FibonacciSequenceService()
    assert type(fibnum.get_nth(None)) != type(0)


def test_get_sequence_index() -> None:
    """"
    Good test case
    - Test if the get_sequence_index function returns an integer.
    - Test if the input value returns the proper index.
    - Test if the input value returns the closest index.
    """
    fibnum = fibonacci_calculator.FibonacciSequenceService()
    assert type(fibnum.get_sequence_index(233)) == type(0)
    assert fibnum.get_sequence_index(8) == 6
    assert fibnum.get_sequence_index(5) == 5
    assert fibnum.get_sequence_index(6) == 5
    assert fibnum.get_sequence_index(7) == 6


def test_get_sequence_index_bad() -> None:
    """"
    Bad test case
    - Test if the get_sequence_index function does not return a string.
    - Test if the get_sequence_index function does not return a list.
    - Test if the get_sequence_index function does not return a dictionary.
    - Test if the get_sequence_index function does not return the wrong closest index.
    """
    fibnum = fibonacci_calculator.FibonacciSequenceService()
    output = fibnum.get_sequence_index(233)
    assert type(fibnum.get_sequence_index(None)) != type(0)
    assert type(output) != type('string')
    assert type(output) != type(list())
    assert type(output) != type(dict())
    assert fibnum.get_sequence_index(8) != 5
    assert fibnum.get_sequence_index(5) != 6


def test_time_get_sequence() -> None:
    """
    Test the passed time using the get_sequence().
    """
    fibnum = fibonacci_calculator.FibonacciSequenceService()
    start = time.time()
    fibnum.increase_sequence_length(233)
    print('\n\nFunction:\t get_sequence()\nTime passed:\t', time.time() - start)


def test_time_get_nth() -> None:
    """
    Test the passed time using the get_nth().
    """
    fibnum = fibonacci_calculator.FibonacciSequenceService()
    start = time.time()
    fibnum.get_nth(233)
    print('\n\nFunction:\t get_nth()\nTime passed:\t', time.time() - start)


def test_time_get_sequence_index() -> None:
    """
    Test the passed time using the get_sequence_index().
    """
    fibnum = fibonacci_calculator.FibonacciSequenceService()
    start = time.time()
    fibnum.get_sequence_index(233)
    print('\n\nFunction:\t get_sequence_index()\nTime passed:\t', time.time() - start)


