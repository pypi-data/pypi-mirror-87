import functools
import time
from tkinter import Event

from .console import *
from .misc import RoundFloat




__all__ = ['Debug', 'CheckTime', 'CheckTimeWithSignature', 'DebugTkinterEvent', 'SimpleDebug', 'StackTrace', 'StackTraceWithSignature']


# def ClassMethodDebug(cls: str or type, tag: str = DEFAULT_TAG):
#     """
#         Print the function signature and return value
#
#     :param cls: class string or type to describe the method's parent or caller.
#     :param tag: a unique string to identify the output in the console window.
#     :return:
#     """
#     if isinstance(cls, type):
#         cls = cls.__name__
#
#     def debug_inner(func: callable = None):
#         """
#             Print the function signature and return value
#
#         :param func: callable function to be debugged.
#         :return:
#         """
#         name = f"{cls}.{func.__name__}"
#
#         @functools.wraps(func)
#         def wrapper_debug(*args, **kwargs):
#             if debug:
#                 Print(tag.format(name))
#                 if args or kwargs:
#                     try: args_repr = [repr(a) for a in args]  # 1
#                     except: args_repr = [str(a) for a in args]  # 1
#
#                     kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
#
#                     signature = ", ".join(args_repr + kwargs_repr)  # 3
#
#                     Print(f"{name}(\n      {signature}\n   )")
#             result = func(*args, **kwargs)
#             if debug: Print(f"{name}  returned  {result!r}\n")  # 4
#
#             return result
#         return wrapper_debug
#     return debug_inner


def Debug(*, tag: str = DEFAULT_TAG, DisableWhenNotDebug: bool = True, sep='\n', end='\n\n', file=None):
    """
        Print the function signature and return value

    :param sep: string to put between passed args
    :type sep: str
    :param end: string to append to end of passed args
    :type end: str
    :param file: file to write to
    :type file: file
    :param DisableWhenNotDebug: if __debug__ is False and DisableWhenNotDebug is True, returns and does NOT print to console.
    :type DisableWhenNotDebug: bool
    :param tag: a unique string to identify the output in the console window.
    """

    def wrapper(func: callable):
        @functools.wraps(func)
        def wrapper_debug(*args, **kwargs):
            result = func(*args, **kwargs)
            if check(DisableWhenNotDebug): return result
            result, _tag, name, signature, pp_result = get_func_details(func, tag, result, args, kwargs)
            PrintLines(f"{name}  returned  {result!r}\n", sep=sep, end=end, file=file, DisableWhenNotDebug=DisableWhenNotDebug)

            return result
        return wrapper_debug
    return wrapper
def SimpleDebug(*, DisableWhenNotDebug: bool = True, sep='\n', end='\n\n', file=None):
    """
        Print the function signature and return value

    :param sep: string to put between passed args
    :type sep: str
    :param end: string to append to end of passed args
    :type end: str
    :param file: file to write to
    :type file: file
    :param DisableWhenNotDebug: if __debug__ is False and DisableWhenNotDebug is True, returns and does NOT print to console.
    :type DisableWhenNotDebug: bool
    """

    def wrapper(func: callable):
        @functools.wraps(func)
        def wrapper_debug(*args, **kwargs):
            result = func(*args, **kwargs)
            if check(DisableWhenNotDebug): return result
            name = GetFunctionName(func)
            start = f"--------- CALLED: {name}\n"
            _end = f"--------- ENDED: {name}\n"
            PrintLines(start, _end, sep=sep, end=end, file=file, DisableWhenNotDebug=DisableWhenNotDebug)
            return result
        return wrapper_debug
    return wrapper


# def CheckClsTime(*, cls: str or type = None, printSignature: bool = True, tag: str = DEFAULT_TAG, DisableWhenNotDebug: bool = True):
#     """
#         Print the function signature and return value
#
#     :param printSignature:
#     :param cls: class string or type to describe the method's parent or caller.
#     :param tag: a unique string to identify the output in the console window.
#     """
#     if isinstance(cls, type): cls = cls.__name__
#
#     def timeit(func: callable):
#         name = GetFunctionName(func)
#
#         @functools.wraps(func)
#         def timed(*args, **kwargs):
#             if debug:
#                 tag = tag.format(name)
#                 if printSignature:
#                     try: args_repr = [repr(a) for a in args]  # 1
#                     except: args_repr = [str(a) for a in args]  # 1
#
#                     kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
#
#                     signature = ", ".join(args_repr + kwargs_repr)  # 3
#
#                     if cls is not None:
#                         Print(f"\n{cls}.{func.__name__}\n{signature}")
#                     else:
#                         Print(f"\n{func.__name__}\n{signature}")
#
#             start_time = time.time()
#             result = func(*args, **kwargs)
#             if debug:
#                 Print(f'{name}  took  {time.time() - start_time}')
#                 Print(f"{name}  returned  {result!r}\n")  # 4
#             return result
#
#         return timed
#     return timeit


def CheckTime(*, DisableWhenNotDebug: bool = True, Precision: int = 5, tag: str = TITLE_TAG, sep='\n', end='\n\n', file=None):
    """

    :param sep: string to put between passed args
    :type sep: str
    :param end: string to append to end of passed args
    :type end: str
    :param file: file to write to
    :type file: file
    :param DisableWhenNotDebug: if __debug__ is False and DisableWhenNotDebug is True, returns and does NOT print to console.
    :type DisableWhenNotDebug: bool
    :param Precision:
    :type Precision:
    :param tag: a unique string to identify the output in the console window.
    :type tag: str
    :return:
    :rtype:
    """
    def wrapper(func: callable):
        @functools.wraps(func)
        def timed(*args, **kwargs):
            if check(DisableWhenNotDebug): return func(*args, **kwargs)
            start_time = time.time()
            result = func(*args, **kwargs)
            _time = RoundFloat(time.time() - start_time, Precision=Precision)
            result, _tag, name, signature, pp_result = get_func_details(func, tag, result, args, kwargs)
            PrintLines(_tag, f'{name}  took:  {_time}', sep=sep, end=end, file=file, DisableWhenNotDebug=DisableWhenNotDebug)
            return result

        return timed
    return wrapper
def CheckTimeWithSignature(*, DisableWhenNotDebug: bool = True, Precision: int = 5, tag: str = TITLE_TAG, sep='\n', end='\n\n', file=None):
    """

    :param sep: string to put between passed args
    :type sep: str
    :param end: string to append to end of passed args
    :type end: str
    :param file: file to write to
    :type file: file
    :param DisableWhenNotDebug: if __debug__ is False and DisableWhenNotDebug is True, returns and does NOT print to console.
    :type DisableWhenNotDebug: bool
    :param Precision:
    :type Precision:
    :param tag: a unique string to identify the output in the console window.
    :type tag: str
    :return:
    :rtype:
    """
    def wrapper(func: callable):
        @functools.wraps(func)
        def timed(*args, **kwargs):
            if check(DisableWhenNotDebug): return func(*args, **kwargs)
            start_time = time.time()
            result = func(*args, **kwargs)
            _time = RoundFloat(time.time() - start_time, Precision=Precision)
            result, _tag, name, signature, pp_result = get_func_details(func, tag, result, args, kwargs)
            _start = f'{name}  took:  {_time}'
            _end = f'{name} returned {pp_result}'
            PrintLines(_start, _end, sep=sep, end=end, file=file, DisableWhenNotDebug=DisableWhenNotDebug)
            return result

        return timed
    return wrapper



def DebugTkinterEvent(*, DisableWhenNotDebug: bool = True, tag: str = TITLE_TAG, sep='\n', end='\n\n', file=None):
    """

    :param sep: string to put between passed args
    :type sep: str
    :param end: string to append to end of passed args
    :type end: str
    :param file: file to write to
    :type file: file
    :param DisableWhenNotDebug:
    :type DisableWhenNotDebug:
    :param tag: a unique string to identify the output in the console window.
    :type tag: str
    :return:
    :rtype:
    """
    def wrapper(func: callable):
        @functools.wraps(func)
        def wrapper_debug(self, event: Event, *args, **kwargs):
            result = func(self, event, *args, **kwargs)
            if check(DisableWhenNotDebug): return result
            name = GetFunctionName(func)
            _tag = tag.format(f'{name}')
            start = f'{name}.{event.__class__}'
            data = event.__dict__
            _end = f"{name}  returned  {getPPrintStr(result)}"
            PrintLines(_tag, start, data, _end, sep=sep, end=end, file=file, DisableWhenNotDebug=DisableWhenNotDebug)

            return result

        return wrapper_debug
    return wrapper




def StackTrace(*, DisableWhenNotDebug: bool = True, INDENT=4 * ' ', tag: str = TITLE_TAG, sep='\n', end='\n\n', file=None):
    """
        Get all but last line returned by traceback.format_stack() which is the line below.

    :param sep: string to put between passed args
    :type sep: str
    :param end: string to append to end of passed args
    :type end: str
    :param file: file to write to
    :type file: file
    :param DisableWhenNotDebug: if __debug__ is False and DisableWhenNotDebug is True, returns and does NOT print to console.
    :type DisableWhenNotDebug: bool
    :param INDENT:
    :type INDENT:
    :param tag: a unique string to identify the output in the console window.
    :type tag: str
    :return:
    :rtype:
    """
    def wrapper(func: callable):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            result = func(*args, **kwargs)
            if check(DisableWhenNotDebug): return result
            result, _tag, name, signature, pp_result = get_func_details(func, tag, result, args, kwargs)
            callstack = GetCallStackAsString(INDENT)
            call = f'{name}() called:'
            _end = f"{name}  returned  {getPPrintStr(result)}"
            PrintLines(_tag, call, callstack, _end, sep=sep, end=end, file=file, DisableWhenNotDebug=DisableWhenNotDebug)
            return result

        return wrapped
    return wrapper
def StackTraceWithSignature(*, DisableWhenNotDebug: bool = True, INDENT=4 * ' ', tag: str = TITLE_TAG, sep='\n', end='\n\n', file=None):
    """
        Get all but last line returned by traceback.format_stack() which is the line below.

    :param sep: string to put between passed args
    :type sep: str
    :param end: string to append to end of passed args
    :type end: str
    :param file: file to write to
    :type file: file
    :param DisableWhenNotDebug: if __debug__ is False and DisableWhenNotDebug is True, returns and does NOT print to console.
    :type DisableWhenNotDebug: bool
    :param tag: a unique string to identify the output in the console window.
    :type tag: str
    :param INDENT:
    :type INDENT:
    :return:
    :rtype:
    """
    def wrapper(func: callable):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            result = func(*args, **kwargs)
            if check(DisableWhenNotDebug): return result
            result, _tag, name, signature, pp_result = get_func_details(func, tag, result, args, kwargs)
            callstack = GetCallStackAsString(INDENT)
            call = f'{name}() called: '
            _end = f"{name}  returned  {pp_result}"
            PrintLines(_tag, call, signature, callstack, _end, sep=sep, end=end, file=file, DisableWhenNotDebug=DisableWhenNotDebug)
            return result

        return wrapped
    return wrapper
