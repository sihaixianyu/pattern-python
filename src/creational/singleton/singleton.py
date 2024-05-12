import unittest
from typing import Any, List
from threading import Lock, Thread
from unittest import TestCase


class SingletonMeta(type):
    """
    This is a thread-safe impl of singleton pattern in python.
    """

    _instances = {}
    _lock: Lock = Lock()

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        with self._lock:
            if self not in self._instances:
                ins = super().__call__(*args, **kwargs)
                self._instances[self] = ins

        return self._instances[self]


class Singleton(metaclass=SingletonMeta):
    value: str = ""

    def __init__(self, value: str) -> None:
        self.value = value

    def do_something(self):
        print("The value of class is {}".format(self.value))


class SingletonTest(TestCase):
    def test_create_singleton_concurrently(self):
        def create_single(value):
            singleton = Singleton(value)
            print(singleton.value)

        pool: List[Thread] = []
        for i in range(10):
            t = Thread(target=create_single, args=("value_{}".format(i),))
            pool.append(t)

        for t in pool:
            t.start()


if __name__ == "__main__":
    unittest.main()
