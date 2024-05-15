#!/usr/bin/env python3
"""
String Redis
"""
from uuid import uuid4
from typing import Union, Callable
from functools import wraps
import redis


def count_calls(method: Callable = None) -> Callable:
    """ Decorator count calls """
    name = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper method """
        self._redis.incr(name)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """ Decorator call history """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function """
        input_str: str = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input_str)

        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)

        return output

    return wrapper


def replay(func: Callable):
    """ Replay function """
    r = redis.Redis()
    func_name = func.__qualname__
    number_calls = r.get(func_name)

    try:
        number_calls = number_calls.decode('utf-8')
    except Exception:
        number_calls = 0

    print(f'{func_name} was called {number_calls} times:')

    ins = r.lrange(func_name + ":inputs", 0, -1)
    outs = r.lrange(func_name + ":outputs", 0, -1)

    for cin, cout in zip(ins, outs):
        cin = cin.decode('utf-8')
        cout = cout.decode('utf-8')

        print(f'{func_name}(*{cin}) -> {cout}')


class Cache:
    """ Functionality Redis """

    def __init__(self):
        """ Constructor """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
            Store the cache

            Args:
                data: bring the information to store

            Return:
                Key or number uuid
        """
        key = str(uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Callable = None)\
            -> Union[str, bytes, int, float]:
        """
            Store the cache

            Args:
                data: bring the information to store

            Return:
                Key or number uuid
        """
        value = self._redis.get(key)

        if fn:
            return fn(value)

        return value

    def get_str(self, key: str) -> str:
        """ Parametrized get str """
        value = self.get(key)
        return value.decode("utf-8") if isinstance(value, bytes) else value

    def get_int(self, key: str) -> int:
        """ Parametrized get int """
        value = self.get(key)
        return int(value) if isinstance(value, (str, bytes)) else value

cache = Cache()

# store
s1 = cache.store("first")
print(s1)
s2 = cache.store("second")
print(s2)
s3 = cache.store("third")
print(s3)

# stored data
inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

print("inputs:", [inp.decode("utf-8") for inp in inputs])
print("outputs:", [out.decode("utf-8") for out in outputs])

replay(cache.store)

