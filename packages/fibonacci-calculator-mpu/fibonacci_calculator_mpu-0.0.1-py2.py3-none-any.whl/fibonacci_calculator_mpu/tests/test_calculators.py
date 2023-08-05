import pytest

from fibonacci_calculator_mpu.Calculator.FibonacciRecursion import FibonacciRecursion
from fibonacci_calculator_mpu.Calculator.FibonacciIteration import FibonacciIteration


@pytest.mark.parametrize('fibonacci_class', [FibonacciIteration, FibonacciRecursion])
@pytest.mark.parametrize('test_input, expected', [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3),
                                                  (5, 5), (6, 8), (7, 13), (8, 21), (9, 34)])
def test_good_cases_get_fibonacci_number(test_input, expected, fibonacci_class):
    f = fibonacci_class()
    assert f.get_fibonacci_number(test_input) == expected


@pytest.mark.parametrize('fibonacci_class', [FibonacciIteration, FibonacciRecursion])
@pytest.mark.parametrize('test_input, expected', [(0, [0]),
                                                  (1, [0, 1]),
                                                  (3, [0, 1, 1, 2]),
                                                  (4, [0, 1, 1, 2, 3]),
                                                  (5, [0, 1, 1, 2, 3, 5]),
                                                  (6, [0, 1, 1, 2, 3, 5, 8]),
                                                  ])
def test_good_cases_get_fibonacci_sequence(test_input, expected, fibonacci_class):
    f = fibonacci_class()
    assert f.get_fibonacci_sequence(test_input) == expected


@pytest.mark.parametrize('fibonacci_class', [FibonacciIteration, FibonacciRecursion])
@pytest.mark.parametrize('test_input, expected', [(0, 0), (1, 1), (2, 3), (3, 4), (5, 5),
                                                  (8, 6), (13, 7), (21, 8), (34, 9), (6, 5),
                                                  (7, 6), (9, 6), (10, 6), (11, 7), (12, 7),
                                                  (14, 7), (15, 7), (16, 7), (17, 7), (18, 8),
                                                  (19, 8), (20, 8)
                                                  ])
def test_good_cases_get_index_fibonacci(test_input, expected, fibonacci_class):
    f = fibonacci_class()
    assert f.get_index_fibonacci_number(test_input) == expected


@pytest.mark.parametrize('fibonacci_class', [FibonacciIteration, FibonacciRecursion])
@pytest.mark.parametrize('test_input, expected', [(-1, -1), (-100, -1)])
def test_bad_cases_get_fibonacci_number(test_input, expected, fibonacci_class):
    f = fibonacci_class()
    assert f.get_fibonacci_number(test_input) == expected


@pytest.mark.parametrize('fibonacci_class', [FibonacciIteration, FibonacciRecursion])
@pytest.mark.parametrize('test_input, expected', [(-1, [-1]), (-100, [-1])])
def test_bad_cases_get_fibonacci_sequence(test_input, expected, fibonacci_class):
    f = fibonacci_class()
    assert f.get_fibonacci_sequence(test_input) == expected
