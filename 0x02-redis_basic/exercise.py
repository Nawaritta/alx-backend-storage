#!/usr/bin/env python3
"""This module contains redis Cache class """


import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """ store an instance of the Redis client as a private variable
    named _redis"""
    def __init__(self):
        """Initialize the Redis client and Flush the Redis database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Generate a random key using uuid
        Store the input data in Redis with the random key
        Return the generated key"""
        rand_key = str(uuid.uuid4())
        self._redis.set(rand_key, data)
        return rand_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Retrieve the data from Redis using the key
        and if data is None, return None"""
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str):
        """getting data as UTF-8 decoded string"""
        return self._redis.get(key).decode("utf-8")

    def get_int(self, key: str):
        """getting data as an integer"""
        return self.get(key, fn=int)
