class FibonacciTable:

    def __init__(self):
        self.forward_look_up_table = {0: 0, 1: 1}
        self.backward_look_up_table = {0: 0, 1: 1}

    def _build_lookup_table(self, fib_index: int) -> None:
        if fib_index in self.forward_look_up_table.keys():
            return

        current_highest_index = max(self.forward_look_up_table.keys())
        next_value = self.forward_look_up_table[current_highest_index - 1] + self.forward_look_up_table[
            current_highest_index]

        self.forward_look_up_table[current_highest_index + 1] = next_value
        self.backward_look_up_table[next_value] = current_highest_index + 1

        self._build_lookup_table(fib_index)

    def _build_non_fibonacci_lookup_table(self, fib_number: int) -> None:
        current_index = self.backward_look_up_table[max(self.backward_look_up_table.keys())]
        previous_index = current_index - 1
        if abs(fib_number - self.forward_look_up_table[previous_index]) <= abs(
                fib_number - self.forward_look_up_table[current_index]):
            self.backward_look_up_table[fib_number] = previous_index
        else:
            self.backward_look_up_table[fib_number] = current_index

    def _update_look_up_table_number(self, fib_index: int) -> None:
        while fib_index > max(self.forward_look_up_table.keys()):
            self._build_lookup_table(fib_index)

    def _update_look_up_table_index(self, fib_number) -> None:
        while fib_number >= max(self.backward_look_up_table.keys()):
            current_index = self.backward_look_up_table[max(self.backward_look_up_table.keys())]
            self._build_lookup_table(current_index + 1)  # hier is het een fibonacci getal
        if fib_number is not max(self.backward_look_up_table.keys()):
            self._build_non_fibonacci_lookup_table(fib_number)  # hier is het geen fibonacci getal

    def new_fibonacci_number(self, fib_index: int) -> int:
        self._update_look_up_table_number(fib_index)
        return self.forward_look_up_table[fib_index]

    def new_index_fibonacci_number(self, number: int) -> int:
        """Returns an index corresponding to the given fibonacci number."""
        self._update_look_up_table_index(number)
        return self.backward_look_up_table[number]
