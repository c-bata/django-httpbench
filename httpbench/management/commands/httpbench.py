import requests
import time

from concurrent.futures.thread import ThreadPoolExecutor
from django.core.management.base import BaseCommand
from httpbench.header import get_username_header_key
from httpbench.throttle import Throttle
from typing import Iterator, Tuple

HEADER_KEY = get_username_header_key()
DEFAULT_TIMEOUT = 30


def fetch(url: str,
          username: str = None,
          timeout: int = None,
          throttle: Throttle = None) -> (int, bool, float):
    """Send a http GET request.

    :return: (status_code, fail, elapsed)
    """
    if throttle:
        throttle.consume()
    start = time.time()
    if not timeout:
        timeout = DEFAULT_TIMEOUT
    try:
        if username:
            res = requests.get(url, timeout=timeout, allow_redirects=False,
                               headers={HEADER_KEY: username})
        else:
            res = requests.get(url, timeout=timeout, allow_redirects=False)
    except requests.exceptions.Timeout:
        return 0, True, 0.0
    except requests.exceptions.ConnectionError:
        return 0, True, 0.0
    return res.status_code, False, time.time() - start


def print_result(results: Iterator[Tuple[int, str]],
                 initial_min: int = None):
    cnt_req, cnt2xx, cnt3xx, cnt4xx, cnt5xx, cnt_fail = 0, 0, 0, 0, 0, 0
    if not initial_min:
        initial_min = DEFAULT_TIMEOUT
    min_2xx = initial_min
    max_2xx = 0
    total_response_time = 0

    for r in results:
        status_code = r[0]
        fail = r[1]
        response_time = r[2]

        cnt_req += 1
        if fail:
            cnt_fail += 1
        elif 200 <= status_code < 300:
            cnt2xx += 1
            total_response_time += response_time
            if response_time < min_2xx:
                min_2xx = response_time
            if response_time > max_2xx:
                max_2xx = response_time
        elif 300 <= status_code < 400:
            cnt3xx += 1
        elif 400 <= status_code < 500:
            cnt4xx += 1
        elif 500 <= status_code:
            cnt5xx += 1

    print(f"Response time:")
    print(f"  mean: {total_response_time / cnt2xx:.3f} secs")
    print(f"  min: {min_2xx:.3f} secs")
    print(f"  max: {max_2xx:.3f} secs")
    print(f"Status:")
    print(f"  2xx: {cnt2xx}")
    print(f"  3xx: {cnt3xx}")
    print(f"  4xx: {cnt4xx}")
    print(f"  5xx: {cnt5xx}")
    print(f"  fail: {cnt_fail}")


class Command(BaseCommand):
    help = 'Benchmarking your Django App like Apache Bench'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs=1, help='Django server url')
        parser.add_argument('--throttle', type=int, default=0,
                            help='Throttling rate. Not throttling if given 0')
        parser.add_argument('-s', '--timeout', type=int, default=30,
                            help='Seconds to max. wait for each response.')
        parser.add_argument('-c', '--concurrency', type=int, default=10,
                            help='Number of multiple requests to make at a time')
        parser.add_argument('-n', '--requests', type=int, default=100,
                            help='Number of requests to perform')
        parser.add_argument('-u', '--username', help='Login username')

    def handle(self, *args, **options):
        throttle_rate: int = options.get('throttle')
        concurrency: int = options.get('concurrency')
        number_of_requests: int = options.get('requests')
        username: str = options.get('username')
        timeout: int = options.get('timeout')
        url: str = options.get('url')

        with ThreadPoolExecutor(concurrency) as pool:
            if throttle_rate > 0:
                throttle = Throttle(throttle_rate)
                tasks = [(throttle, url, username, timeout)
                         for _ in range(number_of_requests)]
            else:
                tasks = [(url, username, timeout)
                         for _ in range(number_of_requests)]
            results = pool.map(lambda a: fetch(*a), tasks)
        print_result(results, initial_min=timeout)
