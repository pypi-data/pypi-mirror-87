import sys
import traceback
from pprint import PrettyPrinter
from threading import Lock
from typing import *




__all__ = [
        'PRINT', 'Print', 'PrintLines', 'getPPrintStr', 'print_exception',
        'TITLE_TAG', 'DEFAULT_TAG', 'END_TAG', 'pp', 'check', 'GetCallStackAsString', 'GetCallStack',
        'get_func_details', 'GetFunctionName', 'GetFuncModule', 'print_signature'
        ]

class NoStringWrappingPrettyPrinter(PrettyPrinter):
    """
        https://stackoverflow.com/questions/31485402/can-i-make-pprint-in-python3-not-split-strings-like-in-python2
        https://stackoverflow.com/a/31485450/9530917
    """
    @classmethod
    def Create(cls): return cls(indent=4, sort_dicts=False)

    # noinspection PyProtectedMember, PyUnresolvedReferences
    def _format(self, o, *args):
        if isinstance(o, (str, bytes, bytearray)):
            width = self._width
            self._width = sys.maxsize
            try:
                super()._format(o, *args)
            finally:
                self._width = width
        else:
            super()._format(o, *args)

DEFAULT_TAG = '\n______________________________________________________________\n"{0}"'
TITLE_TAG = "\n ---------------- {0} ---------------- \n"
END_TAG = '\n ============================================================= \n'

pp = NoStringWrappingPrettyPrinter.Create()
debug = __debug__
_lock = Lock()

def check(DisableWhenNotDebug: bool) -> bool:
    """ internal method """
    if not debug: return True
    elif not DisableWhenNotDebug: return True

    return False

def Print(*args, sep=' ', end='\n', file=None, DisableWhenNotDebug: bool = True):
    """
    :param sep: string to put between passed args
    :type sep: str
    :param end: string to append to end of passed args
    :type end: str
    :param file: file to write to
    :type file: file
    :param DisableWhenNotDebug: if __debug__ is False and DisableWhenNotDebug is True, returns and does NOT print to console.
    :type DisableWhenNotDebug: bool
    """
    if check(DisableWhenNotDebug):
        print('__check__')
        return

    with _lock:
        return print(*args, sep=sep, end=end, file=file)
def PrintLines(*args, sep='\n', end='\n\n', file=None, DisableWhenNotDebug: bool = True):
    """
    :param sep: string to put between passed args
    :type sep: str
    :param end: string to append to end of passed args
    :type end: str
    :param file: file to write to
    :type file: file
    :param DisableWhenNotDebug: if __debug__ is False and DisableWhenNotDebug is True, returns and does NOT print to console.
    :type DisableWhenNotDebug: bool
    """
    return Print(*args, sep=sep, end=end, file=file, DisableWhenNotDebug=DisableWhenNotDebug)
def PRINT(title: str, *args, _pp: PrettyPrinter = None, use_double_quotes: bool = True, DisableWhenNotDebug: bool = True, sep='\n', end='\n\n', file=None, **kwargs):
    """
    :param title: message to start the Print, to make it easier to find it.
    :type title: str
    :param o: object to be serialized
    :type o: any
    :param _pp: any PrettyPrinter inpmentation. provide your own to customize the output.
    :type _pp: PrettyPrinter
    :param use_double_quotes: use double quotes (") instead of the default single quotes (')
    :type use_double_quotes: bool

    :param sep: string to put between passed args
    :type sep: str
    :param end: string to append to end of passed args
    :type end: str
    :param file: file to write to
    :type file: file
    :param DisableWhenNotDebug: if __debug__ is False and DisableWhenNotDebug is True, returns and does NOT print to console.
    :type DisableWhenNotDebug: bool
    """
    if check(DisableWhenNotDebug): return

    return PrintLines(TITLE_TAG.format(title),
                      getPPrintStr(dict(args=args, kwargs=kwargs), _pp=_pp, use_double_quotes=use_double_quotes),
                      sep=sep, end=end, file=file)



def getPPrintStr(o: any, *, _pp: PrettyPrinter = None, use_double_quotes: bool = True) -> str:
    """
    :param o: object to be serialized
    :type o: any
    :param _pp: any PrettyPrinter inpmentation. provide your own to customize the output.
    :type _pp: PrettyPrinter
    :param use_double_quotes: use double quotes (") instead of the default single quotes (')
    :type use_double_quotes:
    :return: formatted string of the passed object
    :rtype: str
    """
    s = (_pp or pp).pformat(o)
    if use_double_quotes: s = s.replace("'", '"')
    return s



def print_exception(e: Exception, *, DisableWhenNotDebug: bool = True):
    if check(DisableWhenNotDebug): return

    with _lock:
        traceback.print_exception(type(e), e, e.__traceback__)



def GetFuncModule(func: callable) -> str: return func.__module__
def GetFunctionName(func: callable) -> str:
    if hasattr(func, '__qualname__') and hasattr(func, '__module__'): return f"{func.__module__}.{func.__qualname__}"
    elif hasattr(func, '__qualname__'): return func.__qualname__
    else: return func.__name__



def GetCallStack(INDENT: str) -> Iterable[str]: return [INDENT + line.strip() for line in traceback.format_stack()][:-1]
def GetCallStackAsString(INDENT: str) -> str: return '\n'.join(GetCallStack(INDENT))



def get_func_details(func: callable, tag: str, result: Any, args, kwargs) -> Tuple[Any, str, str, str, str]:
    """
    :param result: result of the passed function or method
    :type result: Any
    :param func: function or method being called
    :type func: callable
    :param tag: line to print before function/method details
    :type tag: str
    :param args: args passed to function/method
    :param kwargs: keyword args passed to function/method
    :return: result, tag, name, signature, pp_result
    :rtype: Tuple[Any, str, str, str, str]
    """
    assert ('{0}' in tag)

    name = GetFunctionName(func)
    tag = tag.format(name)
    signature = getPPrintStr({ 'args': args, 'kwargs': kwargs })
    pp_result = getPPrintStr(result)

    return result, tag, name, signature, pp_result
def print_signature(func: callable, tag: str, *args, **kwargs):
    if not debug: return
    assert ('{0}' in tag)

    result = func(*args, **kwargs)
    result, _tag, name, signature, pp_result = get_func_details(func, tag, result, args, kwargs)
    PrintLines(tag, f'{name}(\n      {signature}\n   )', name, f'returned: \n{getPPrintStr(result)}')

    return result
