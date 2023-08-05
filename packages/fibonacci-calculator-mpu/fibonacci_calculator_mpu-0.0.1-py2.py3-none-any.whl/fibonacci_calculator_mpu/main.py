import timeit
from fibonacci_calculator_mpu.Calculator.FibonacciIteration import FibonacciIteration
from fibonacci_calculator_mpu.Calculator.FibonacciRecursion import FibonacciRecursion


def timer():
    """
    Times the iteration and recursive method of
    finding the n-th fibonacci number.
    """
    time_methods = [FibonacciIteration(), FibonacciRecursion()]
    time_elapsed = []
    numbers = [400, 399]
    for i in range(2):
        for m in time_methods:
            start_time = timeit.default_timer()
            m.get_fibonacci_number(numbers[i])
            run_time = timeit.default_timer() - start_time
            print(f'Finished: {m.__class__.__name__} in {run_time:.6f} secs')
            time_elapsed.append(run_time)

    print(f'Recursion is the second time {time_elapsed[1]/time_elapsed[3]:.2f} faster')


def main():

    timer()


if __name__ == '__main__':
    main()





