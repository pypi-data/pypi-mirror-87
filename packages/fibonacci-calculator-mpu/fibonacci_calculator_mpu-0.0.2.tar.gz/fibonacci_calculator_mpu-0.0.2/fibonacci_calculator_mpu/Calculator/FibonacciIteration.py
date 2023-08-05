from typing import List


class FibonacciIteration:

    def __init__(self):
        self.lookup_table = {0: 0, 1: 1}
        self.reverse_lookup_table = {0: 0, 1: 1}

    def get_fibonacci_number(self, n: int) -> int:
        """
        Iteration method of the n-th fibonacci number.
        0(n) time, 0(1) space
        """
        next_fib = -1
        latest_two = [0, 1]

        if n == 0 or n == 1:
            return latest_two[n]
        i = 2
        while i <= n and n > 1:
            next_fib = latest_two[0] + latest_two[1]
            self.lookup_table[i] = next_fib  # this is for the sequence
            latest_two[0], latest_two[1] = latest_two[1], next_fib
            i += 1
        return next_fib

    def get_fibonacci_sequence(self, n: int) -> List[int]:
        """
        Returns list of fibonacci numbers until the n-th fibonacci number.
        Makes use of iteration method.
        """

        if n == 0:
            return [0]
        self.get_fibonacci_number(n)
        return list(self.lookup_table.values()) if n > 0 else [-1]

    def get_index_fibonacci_number(self, number: int) -> int:
        """
        Returns an index of the given fibonacci number. If the given number is not a fibonacci
        number the closest fibonacci number will be used.
        """
        if number <= 1:
            return number  # base case -> problem with (1, 1) (1, 2) two different indices same fib number
        latest_idx = [0, 1]
        next_fib = 1
        i = 2
        while next_fib < number:
            next_fib = latest_idx[0] + latest_idx[1]
            self.reverse_lookup_table[next_fib] = i
            latest_idx[0], latest_idx[1] = latest_idx[1], next_fib
            i += 1
        if number is not next_fib:
            next_fib = get_closest_fibonacci_number(next_fib, latest_idx[0], number)
        return self.reverse_lookup_table[next_fib]


def get_closest_fibonacci_number(current_fib: int, previous_fib: int, fibonacci_number: int) -> int:
    """
    Returns the fibonacci number with the shortest distance of two consecutive fibonacci numbers.
    """
    if abs(previous_fib - fibonacci_number) <= abs(current_fib - fibonacci_number):
        return previous_fib
    else:
        return current_fib
