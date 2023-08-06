import functools
import time
from tkinter import Event
from .base import *
from .console import getPPrintStr, pp



__all__ = ['debug', 'class_method_debug', 'check_time', 'debugTkinterEvent', 'pprint_debug']


def class_method_debug(cls: str or type, tag: str = DEFAULT_TAG):
    """
        Print the function signature and return value

    :param cls: class string or type to describe the method's parent or caller.
    :param tag: a unique string to identify the output in the console window.
    :return:
    """
    if isinstance(cls, type):
        cls = cls.__name__

    def debug_inner(func: callable = None):
        """
            Print the function signature and return value

        :param func: callable function to be debugged.
        :return:
        """
        name = f"{cls}.{func.__name__}"

        @functools.wraps(func)
        def wrapper_debug(*args, **kwargs):
            Print(tag.format(name))
            if args or kwargs:
                try: args_repr = [repr(a) for a in args]  # 1
                except: args_repr = [str(a) for a in args]  # 1

                kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2

                signature = ", ".join(args_repr + kwargs_repr)  # 3

                Print(f"{name}(\n      {signature}\n   )")
            result = func(*args, **kwargs)
            Print(f"{name}  returned  {result!r}\n")  # 4

            return result
        return wrapper_debug
    return debug_inner



def debug(func: callable, tag: str = DEFAULT_TAG):
    """
        Print the function signature and return value

    :param func: callable function to be debugged.
    :param tag: a unique string to identify the output in the console window.
    :return:
    """
    name = GetFunctionName(func)

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        print_signature(func, tag, *args, **kwargs)
        result = func(*args, **kwargs)
        Print(f"{name}  returned  {result!r}\n")  # 4

        return result
    return wrapper_debug



def pprint_debug(func: callable, tag: str = DEFAULT_TAG):
    """
        Print the function signature and return value

    :param func: callable function to be debugged.
    :param tag: a unique string to identify the output in the console window.
    :return:
    """
    name = GetFunctionName(func)

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        Print(tag.format(name))
        signature = getPPrintStr({'kwargs': kwargs, 'args': args, })
        Print(f"{name}(\n      {signature}\n   )")
        result = func(*args, **kwargs)
        Print(f"{name}  returned: \n{getPPrintStr(result)}\n")

        return result
    return wrapper_debug



def check_cls_time(*, cls: str or type = None, print_signature: bool = True, tag: str = DEFAULT_TAG):
    """
        Print the function signature and return value

    :param print_signature:
    :param cls: class string or type to describe the method's parent or caller.
    :param tag: a unique string to identify the output in the console window.
    :return:
    """
    if isinstance(cls, type):
        cls = cls.__name__

    def timeit(func: callable):
        name = GetFunctionName(func)

        @functools.wraps(func)
        def timed(*args, **kwargs):
            Print(tag.format(name))
            if print_signature:
                try: args_repr = [repr(a) for a in args]  # 1
                except: args_repr = [str(a) for a in args]  # 1

                kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2

                signature = ", ".join(args_repr + kwargs_repr)  # 3

                if cls is not None:
                    Print(f"\n{cls}.{func.__name__}\n{signature}")
                else:
                    Print(f"\n{func.__name__}\n{signature}")

            start_time = time.time()
            result = func(*args, **kwargs)
            Print(f'{name}  took  {time.time() - start_time}')
            Print(f"{name}  returned  {result!r}\n")  # 4
            return result

        return timed
    return timeit



def check_time(func: callable, tag: str = DEFAULT_TAG):
    name = GetFunctionName(func)

    @functools.wraps(func)
    def timed(*args, **kwargs):
        print_signature(func, tag, *args, **kwargs)

        start_time = time.time()
        result = func(*args, **kwargs)
        Print(f'{name}  took  {time.time() - start_time}')
        Print(f"{name}  returned  {result!r}\n")
        return result

    return timed



def debugTkinterEvent(func: callable, tag: str = DEFAULT_TAG):
    name = GetFunctionName(func)

    @functools.wraps(func)
    def wrapper_debug(self, event: Event, *args, **kwargs):
        Print(tag.format(f'{name}'))
        Print(f'{name}.{event.__class__}')
        pp.pprint(event.__dict__)

        result = func(self, event, *args, **kwargs)
        Print(f"{name}  returned  {result!r}\n")

        return result

    return wrapper_debug

