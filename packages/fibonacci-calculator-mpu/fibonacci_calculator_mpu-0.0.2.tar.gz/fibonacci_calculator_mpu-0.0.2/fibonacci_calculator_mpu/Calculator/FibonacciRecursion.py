from typing import List
from fibonacci_calculator_mpu.Decorators.memoize import memoize


class FibonacciRecursion:

    @memoize
    def get_fibonacci_number(self, n: int) -> int:
        """ Recursion method of the n-th fibonacci number"""
        if n < 0:
            return -1
        if n == 0 or n == 1:
            return n
        else:
            next_fib = self.get_fibonacci_number(n-1) + self.get_fibonacci_number(n-2)
            return next_fib

    @memoize
    def get_fibonacci_sequence(self, n: int) -> List[int]:
        """Returns list of fibonacci numbers until the n-th fibonacci number."""
        if n < 0:
            return [-1]
        else:
            sequence = [self.get_fibonacci_number(i) for i in range(n+1)]
            return sequence

    @memoize
    def get_index_fibonacci_number(self, number: int) -> int:

        if number < 2:
            return number
        next_fib = 1
        index = 2
        while next_fib < number:
            index += 1
            next_fib = self.get_fibonacci_number(index)
        if number is not next_fib:
            index = self.get_closest_index(index, number)
        return index

    @memoize
    def get_closest_index(self, index: int, number: int) -> int:
        """Helper function. Gives back the index of the nearest fibonacci number"""
        previous = self.get_fibonacci_number(index - 1)
        current = self.get_fibonacci_number(index)
        if abs(previous - number) <= abs(current - number):
            return index - 1
        else:
            return index




