import functools
from itertools import count

from .base import GetFunctionName, DEFAULT_TAG, END_TAG

from .console import getPPrintStr

__all__ = ['chain', 'sub']


class _AutoCounter(object):
    _counter: count
    def __init__(self, *, start: int = 0, step: int = 1):
        self._value = start
        self.reset(start=start, step=step)
    def __call__(self, *args, **kwargs) -> int:
        self._value = self._next()
        return self._value
    @property
    def value(self) -> int:
        return self._value
    def reset(self, *, start: int = 0, step: int = 1):
        self._counter = count(start=start, step=step)
        self._next = self._counter.__next__


_counter = _AutoCounter()


def _print_chain_signature(func: callable, tag: str, level: int or str, signature: bool, *args, **kwargs):
    assert ('{0}' in tag)
    name = GetFunctionName(func)
    Print(tag.format(f'{level} --> {name}'))

    if signature and (args or kwargs):
        signature = getPPrintStr({ 'kwargs': kwargs, 'args': args, })
        Print(f"{name}(\n      {signature}\n   )")
        result = func(*args, **kwargs)
        Print(f"{name}  returned: \n{getPPrintStr(result)}\n")



def chain(start_tag: str = DEFAULT_TAG, end_tag: str = END_TAG, start: int = 1):
    """
        Print the function signature and return value

    :param end_tag: a unique string to identify the ENDING of the chain in the console window.
    :param start_tag: a unique string to identify the START of the chain in the console window.
    :return:
    """
    _counter.reset(start=start)
    def top(func: callable):
        """
        :param func: callable function to be debugged.
        :return:
        """
        name = GetFunctionName(func)

        @functools.wraps(func)
        def wrapper_debug(*args, **kwargs):
            Print(start_tag.format(name))
            signature = getPPrintStr({ 'kwargs': kwargs, 'args': args, })
            Print(f"{name}(\n      {signature}\n   )")
            result = func(*args, **kwargs)
            Print(f"{name}  returned: \n{getPPrintStr(result)}\n")
            Print(end_tag)

            return result
        return wrapper_debug
    return top

# class callback(object):
#     def __init__(self, func: callable, name: str, tag: str, signature: bool ):
#         self._signature = signature
#         self._tag = tag
#         self._name = name
#         self._func = func
#     def __call__(self, *args, **kwargs):
#         _print_chain_signature(self._func, self._tag, _counter(), self._signature, *args, **kwargs)
#         result = self._func(*args, **kwargs)
#         Print(f"{self._name}  returned  {result!r}\n")
#         return result

def sub(*, tag: str = '-------------- level: {0}', signature: bool = False):
    """
        Print the function signature [Optional] and return value.

    :param signature: for sub-level method chains, prints it's signature. defaults to False.
    :param level: the call stack level. f() -> g() -> h() -> etc.
    :param tag: a unique string to identify the output in the console window. must have one '{0}' for str.format() support.
    :return:
    """

    def wrapped(func: callable):
        """
        :param func: callable function to be debugged.
        :return:
        """
        name = GetFunctionName(func)

        @functools.wraps(func)
        def wrapper_debug(*args, **kwargs):
            # return callback(func, name, tag, signature)
            _print_chain_signature(func, tag, _counter(), signature, *args, **kwargs)
            result = func(*args, **kwargs)
            Print(f"{name}  returned  {result!r}\n")
            return result
        return wrapper_debug
    return wrapped
