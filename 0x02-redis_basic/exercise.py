#!/usr/bin/env python3
"""This module contains redis Cache class """


import redis
import uuid
from typing import Union


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
