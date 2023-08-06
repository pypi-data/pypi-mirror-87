import sys
from itertools import count
from typing import Iterator




__all__ = [
        'get_size', 'RoundFloat', 'AutoCounter',
        ]


def RoundFloat(Float: float, Precision: int) -> str:
    """ Rounds the Float to the given Precision and returns It as string. """
    return f"{Float:.{Precision}f}"



def get_size(obj, seen: set = set()):
    """ Recursively finds size of objects """
    size = sys.getsizeof(obj)
    if seen is None: seen = set()

    obj_id = id(obj)
    if obj_id in seen: return 0

    # Important mark as seen *before* entering recursion to gracefully handle self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])

    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)

    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])

    return size



class AutoCounter(object):
    _counter: Iterator[int]
    _next: callable
    def __init__(self, *, start: int = 0, step: int = 1):
        self._value = start
        self.reset(start=start, step=step)
    def __call__(self, *args, **kwargs) -> int:
        self._value = self._next()
        return self._value
    @property
    def value(self) -> int: return self._value
    def reset(self, *, start: int = 0, step: int = 1):
        self._counter = count(start=start, step=step)
        self._next = self._counter.__next__

    def __str__(self): return str(self._value)
    def __repr__(self): return f'<{self.__class__.__name__}, value: {self._value}>'
