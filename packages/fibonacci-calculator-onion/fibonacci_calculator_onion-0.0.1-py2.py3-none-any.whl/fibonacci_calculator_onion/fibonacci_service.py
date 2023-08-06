from typing import List
from fibonacci_table import FibonacciTable


class FibonacciService:

    def __init__(self):
        """ Instance of Fibonacci Data. With two tables. Forward and Backward tables."""
        self.data = FibonacciTable()

    def get_fibonacci_number(self, n: int) -> int:
        """Returns a fibonacci number of a given index

        """
        if n < 0:
            return -1
        if self.data.forward_look_up_table.get(n) is not None:
            return self.data.forward_look_up_table[n]
        return self.data.search_fibonacci_number(n)

    def get_fibonacci_index(self, fibonacci_number: int) -> int:
        """
        :param fibonacci_number: An arbitrary number.
        :return: The index corresponding to the fibonacci_number. If it is not a fibonacci
        number it returns an index corresponding to the closest fibonacci number.
        """
        if fibonacci_number < 0:
            return -1
        if self.data.backward_look_up_table.get(fibonacci_number) is not None:
            return self.data.backward_look_up_table.get(fibonacci_number)
        return self.data.search_index_fibonacci_number(fibonacci_number)

    def get_fibonacci_sequence(self, n: int) -> List[int]:
        """
        :param n: An index.
        :return: A list with fibonacci sequence until the given index.
        """
        if n < 0:
            return [-1]
        return [self.get_fibonacci_number(i) for i in range(n + 1)]





