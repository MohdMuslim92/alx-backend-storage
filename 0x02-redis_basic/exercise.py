#!/usr/bin/env python3
"""
Cache class utilizing Redis for storing data
"""
from functools import wraps
import redis
from typing import Union, Callable
import uuid


class Cache:
    """
    A class to handle caching using Redis.

    Attributes:
     _redis: Instance of Redis client.
    """
    def __init__(self):
        """
        Initializes Redis client and flushes the instance using flushdb
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores input data in Redis using a random key and returns the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, None]:
        """
        Retrieves data from Redis using the provided key and applies optional
        conversion function.

        Args:
        - key: The key to retrieve data from Redis.
        - fn: Optional callable function to convert the retrieved data.

        Returns:
        - Retrieved data with optional conversion applied, or None if key
        doesn't exist.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieves and converts data from Redis to a string.

        Args:
        - key: The key to retrieve data from Redis.

        Returns:
        - Retrieved data as a string, or None if key doesn't exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieves and converts data from Redis to an integer.

        Args:
        - key: The key to retrieve data from Redis.

        Returns:
        - Retrieved data as an integer, or None if key doesn't exist or data
        cannot be converted.
        """
        return self.get(key, fn=lambda d: int(d))

    def count_calls(method: Callable) -> Callable:
        """
        Decorator to count the number of times a method is called.

        Args:
        - method: The method to be decorated.

        Returns:
        - Wrapped function that increments the count for the method key in
        Redis and returns the value returned by the original method.
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Decorated method to store input data in Redis using a random key and
        returns the key.

        Args:
        - data: The data to be stored. It can be a string, bytes, int, or
        float.

        Returns:
        - key: The generated key used for storing the data in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
