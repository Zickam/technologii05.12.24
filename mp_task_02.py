import threading
import time
import multiprocessing
import math
import asyncio

# Функции для АТ-03

# запускать с n = 700003
def fibonacci(n):  # содержимое функции не менять
    """Возвращает последнюю цифру n-е числа Фибоначчи."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    print(f'fibonacci = {b % 10}')


# запускать с f, a, b, n равными соответственно math.sin, 0, math.pi, 20000000
def trapezoidal_rule(f, a, b, n):  # содержимое функции не менять
    """Вычисляет определенный интеграл функции f от a до b методом трапеций с n шагами."""
    h = (b - a) / n
    integral = (f(a) + f(b)) / 2.0
    for i in range(1, n):
        integral += f(a + i * h)
    print(f'trapezoidal_rule = {integral * h}')

n = 700003
trapezoidal_rule_args = (math.sin, 0, math.pi, 20000000)

def sequence():
    start_time = time.perf_counter()

    fibonacci(n)
    trapezoidal_rule(*trapezoidal_rule_args)

    end_time = time.perf_counter()

    print(f'sequence time: {end_time - start_time: 0.2f} \n')


def threads():
    start_time = time.perf_counter()

    threads = []

    fib_thread = threading.Thread(target=fibonacci, args=(n, ))
    fib_thread.start()
    threads.append(fib_thread)

    trapezoidal_rule_thread = threading.Thread(target=trapezoidal_rule, args=(*trapezoidal_rule_args, ))
    trapezoidal_rule_thread.start()
    threads.append(trapezoidal_rule_thread)

    for thread in threads:
        thread.join()

    end_time = time.perf_counter()

    print(f'threads time: {end_time - start_time: 0.2f} \n')


def processes():
    start_time = time.perf_counter()

    processes = []

    fib_process = multiprocessing.Process(target=fibonacci, args=(n, ))
    fib_process.start()
    processes.append(fib_process)

    trapezoidal_rule_process = multiprocessing.Process(target=trapezoidal_rule, args=(*trapezoidal_rule_args, ))
    trapezoidal_rule_process.start()
    processes.append(trapezoidal_rule_process)

    for process in processes:
        process.join()

    end_time = time.perf_counter()

    print(f'processes time: {end_time - start_time: 0.2f} \n')


async def async_fibonacci(n):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, fibonacci, n)


async def async_trapezoidal_rule(*args):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, trapezoidal_rule, *args)


async def async_run():
    start_time = time.perf_counter()

    await asyncio.gather(
        async_fibonacci(n),
        async_trapezoidal_rule(*trapezoidal_rule_args)
    )

    end_time = time.perf_counter()
    print(f'async time: {end_time - start_time: 0.2f} \n')


if __name__ == '__main__':
    sequence()
    threads()
    processes()
    asyncio.run(async_run())

    """
        CPU: Ryzen 5 4600H 6 cores 12 threads 4.2ghz 
        Memory: 3200mhz
        
        fibonacci = 7
        trapezoidal_rule = 2.000000000000087
        sequence time:  5.80 
        
        trapezoidal_rule = 2.000000000000087
        fibonacci = 7
        threads time:  7.74 
        
        trapezoidal_rule = 2.000000000000087
        fibonacci = 7
        processes time:  3.85 
        
        trapezoidal_rule = 2.000000000000087
        fibonacci = 7
        async time:  8.49 
    """
