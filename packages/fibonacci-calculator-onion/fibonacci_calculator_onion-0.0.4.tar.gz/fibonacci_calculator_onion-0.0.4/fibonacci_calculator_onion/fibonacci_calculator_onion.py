from fibonacci_service import FibonacciService


def main():
    f = FibonacciService()
    print(f.get_fibonacci_number(10))
    print(f.get_fibonacci_sequence(10))
    print(f.get_fibonacci_index(34))


if __name__=='__main__':
    main()
