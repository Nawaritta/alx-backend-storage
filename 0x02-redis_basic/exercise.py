#!/usr/bin/env python3
"""This module contains redis Cache class """


import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper function """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs
    for a function in Redis"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper function"""
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        self._redis.rpush(input_key, str(args))

        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))

        return result

    return wrapper


def replay(self, method: Callable):
    """display the history of calls of a particular function"""
    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"

    inputs = self._redis.lrange(input_key, 0, -1)
    outputs = self._redis.lrange(output_key, 0, -1)

    for i, (input_args, output) in enumerate(zip(inputs,
                                                 outputs), start=1):
        print("{}(*{}) -> {}"
              .format(i, input_args.decode('utf-8',
                                           output.decode('utf-8'))))


class Cache:
    """ store an instance of the Redis client as a private variable
    named _redis"""
    def __init__(self):
        """Initialize the Redis client and Flush the Redis database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Generate a random key using uuid
        Store the input data in Redis with the random key
        Return the generated key"""
        rand_key = str(uuid.uuid4())
        self._redis.set(rand_key, data)
        return rand_key

    def get(self, key: str,
            fn: Optional[Callable]
            = None) -> Union[str, bytes, int, float]:
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
