import functools
import sys
import time
from datetime import timedelta
from typing import Callable, Union

from .config import settings
from .exceptions import RateLimitExceeded
from .redis_client import redis_client


class RateLimiter:
    def __init__(
        self,
        limit: int = sys.maxsize,
        period: Union[int, timedelta] = timedelta(minutes=1),
    ):
        """RateLimiter

        :param limit: Rate limit for each period, defaults to sys.maxsize
        :type limit: int, optional
        :param period: Size of the period, accept int(seconds) and timedelta, defaults to timedelta(minutes=1)
        :type period: Union[int, timedelta], optional
        """
        self.limit = limit
        self.period = period.seconds if isinstance(period, timedelta) else period

    def check(self, func: Callable):
        """Check if func could be called.

        :param func: the func to be limited
        :type func: Callable
        :raises RateLimitExceeded: Raised when the func has been called `self.limit` times during last `self.period`
        """
        key = f"{settings.key_prefix}:{func.__name__}:{int(time.time())//self.period}"
        if int(redis_client.incr(key)) > self.limit:
            raise RateLimitExceeded()
        if redis_client.ttl(key) == -1:
            redis_client.expire(key, self.period)

    def __call__(self, func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.check(func)
            return func(*args, **kwargs)

        return wrapper
