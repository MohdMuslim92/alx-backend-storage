#!/usr/bin/env python3
"""
Cache class utilizing Redis for storing data
"""
import redis
import uuid
from typing import Union


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
