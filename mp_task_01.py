import threading
import time
import multiprocessing
import math
import asyncio

import requests
import aiohttp

# список url
urls = ['https://www.example.com'] * 10


def fetch_url(url):
    response = requests.get(url)
    return response.text


def sequence():
    start_time = time.perf_counter()
    for url in urls:
        fetch_url(url)
    end_time = time.perf_counter()
    print(f'sequence time: {end_time - start_time: 0.2f} \n')


def threads():
    start_time = time.perf_counter()
    threads = []
    for url in urls:
        thread = threading.Thread(target=fetch_url, args=(url, ))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.perf_counter()
    print(f'threads time: {end_time - start_time: 0.2f} \n')


def processes():
    start_time = time.perf_counter()

    processes = []
    for url in urls:
        process = multiprocessing.Process(target=fetch_url, args=(url, ))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time.perf_counter()
    print(f'processes time: {end_time - start_time: 0.2f} \n')


async def fetch_url_async(session, url):
    async with session.get(url) as response:
        return await response.text()


async def async_requests():
    start_time = time.perf_counter()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url_async(session, url) for url in urls]
        await asyncio.gather(*tasks)
    end_time = time.perf_counter()
    print(f'async time: {end_time - start_time: 0.2f} \n')


if __name__ == '__main__':
    sequence()
    threads()
    processes()
    asyncio.run(async_requests())

    """
        CPU: Ryzen 5 4600H 6 cores 12 threads 4.2ghz 
        Memory: 3200mhz
        
        sequence time:  13.19 
        
        threads time:  1.58 
        
        processes time:  1.25 
        
        async time:  0.93 
    """
