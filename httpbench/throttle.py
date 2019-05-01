import time
from threading import Lock


class Throttle:
    def __init__(self, rate):
        self._consume_lock = Lock()
        self.rate = rate  # per second
        self.tokens = 0.0
        self.last = 0

    def consume(self, amount=1):
        if amount > self.rate:
            raise ValueError("amount must be less or equal to rate")

        with self._consume_lock:
            while True:
                now = time.time()

                if self.last == 0:
                    self.last = now

                elapsed = now - self.last
                self.tokens += elapsed * self.rate
                self.last = now

                if self.tokens > self.rate:
                    self.tokens = self.rate

                if self.tokens >= amount:
                    self.tokens -= amount
                    return amount

                time.sleep((amount - self.tokens) / self.rate)
