import requests
import time

from concurrent.futures.thread import ThreadPoolExecutor
from django.core.management.base import BaseCommand
from httpbench.header import get_username_header_key
from httpbench.throttle import Throttle
from typing import Iterator, Tuple

HEADER_KEY = get_username_header_key()


def fetch(url: str, username: str = None) -> (int, bool):
    try:
        if username:
            res = requests.get(url, timeout=5, allow_redirects=False,
                               headers={HEADER_KEY: username})
        else:
            res = requests.get(url, timeout=5, allow_redirects=False)
    except requests.exceptions.Timeout:
        return 0, True
    except requests.exceptions.ConnectionError:
        # Sometimes this exception was happened with following message:
        # ('Connection aborted.', BrokenPipeError(32, 'Broken pipe'))
        return fetch(url, username=username)
    return res.status_code, False


def throttling_fetch(throttle: Throttle, url: str,
                     username: str = None) -> (int, bool):
    throttle.consume()
    return fetch(url, username)


def print_result(results: Iterator[Tuple[int, str]], elapsed: float):
    cnt_req, cnt2xx, cnt3xx, cnt4xx, cnt5xx, cnt_timeout = 0, 0, 0, 0, 0, 0

    for r in results:
        status_code = r[0]
        timeout = r[1]
        cnt_req += 1
        if timeout:
            cnt_timeout += 1
        elif 200 <= status_code < 300:
            cnt2xx += 1
        elif 300 <= status_code < 400:
            cnt3xx += 1
        elif 400 <= status_code < 500:
            cnt4xx += 1
        elif 500 <= status_code:
            cnt5xx += 1

    print(f"{elapsed:.3f} secs / {cnt_req} req, "
          f"2xx={cnt2xx} 3xx={cnt3xx} 4xx={cnt4xx} 5xx={cnt5xx} timeout={cnt_timeout}")


class Command(BaseCommand):
    help = 'Insert dummy users and dummy snippets'

    def add_arguments(self, parser):
        parser.add_argument('--throttle', type=int, default=0,
                            help='Throttling rate. Not throttling if given 0')
        parser.add_argument('--threads', type=int, default=10,
                            help='Number of threads')
        parser.add_argument('--interval', type=int, default=20,
                            help='interval requests count')
        parser.add_argument('--username', help='Login username')
        parser.add_argument('--url', help='Request url',
                            default='http://127.0.0.1:8000/')

    def handle(self, *args, **options):
        throttle_rate: int = options.get('throttle')
        number_of_threads: int = options.get('threads')
        interval: int = options.get('interval')
        username: str = options.get('username')
        url: str = options.get('url')

        throttle: Throttle = None
        if throttle_rate > 0:
            throttle = Throttle(throttle_rate)

        try:
            while True:
                start = time.time()
                with ThreadPoolExecutor(number_of_threads) as pool:
                    if throttle_rate > 0:
                        results = pool.map(lambda a: throttling_fetch(*a),
                                           [(throttle, url, username) for _ in range(interval)])
                    else:
                        results = pool.map(lambda a: fetch(*a),
                                           [(url, username) for _ in range(interval)])
                end = time.time()
                elapsed = end - start
                print_result(results, elapsed)
        except KeyboardInterrupt:
            print("exit")
