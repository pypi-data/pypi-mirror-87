import sys
import traceback
from pprint import PrettyPrinter
from threading import Lock
from typing import *




__all__ = [
        # 'PRINT', 'Print', 'getPPrintStr', 'print_exception', 'check', 'get_func_details', 'print_signature'
        # 'TITLE_TAG', 'DEFAULT_TAG', 'END_TAG',
        'Printer', 'pp', 'CallStack',
        'GetFunctionName', 'GetFuncModule',
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
                return super()._format(o, *args)
            finally:
                self._width = width

        elif isinstance(o, CallStack):
            print('__CallStack__', o, *args)
            # super()._format(o.Lines, *args)
            return super()._format(str(o), *args)

        else:
            return super()._format(o, *args)

class CallStack(object):
    _lines: Iterable[str] = None
    def __init__(self, indent: str = 4 * ' ', *, once: bool = True):
        self._indent = indent
        self._once = once
        self.Update()

    def Update(self):
        if self._once and self._lines is not None: raise RuntimeError()

        self._lines = [self._indent + line.strip() for line in traceback.format_stack()][:-1]

    @property
    def Lines(self) -> Iterable[str]:
        if self._lines is None: self.Update()
        return self._lines
    def __str__(self) -> str: return '\n'.join(self.Lines)
    # def __repr__(self) -> str: return '\n'.join(self.Lines)



class Printer(object):
    DEFAULT_TAG = '\n______________________________________________________________\n"{0}"'
    TITLE_TAG = "\n ---------------- {0} ---------------- \n"
    END_TAG = '\n ============================================================= \n'
    _lock = Lock()
    def __init__(self, _pp: PrettyPrinter = None, *, use_double_quotes: bool, end: str, file=None):
        """
        :param end: string to append to end of passed args
        :type end: str
        :param file: file to write to
        :type file: file
        :param _pp: any PrettyPrinter inpmentation. provide your own to customize the output.
        :type _pp: PrettyPrinter
        :param use_double_quotes: use double quotes (") instead of the default single quotes (')
        :type use_double_quotes: bool
        """
        self._file = file
        self._end = end
        self._use_double_quotes = use_double_quotes
        self._pp = _pp or NoStringWrappingPrettyPrinter.Create()
        self.pprint = self._pp.pprint

    @property
    def debug(self) -> bool: return __debug__
    def check(self) -> bool: return not self.debug

    def Print(self, *args):
        if self.check(): return

        with self._lock:
            # self._pp.pprint(args)
            return print(*args, sep='\n', end=self._end, file=self._file)

    def PRINT(self, title: str, *args, **kwargs):
        """
        :param title: message to start the Print, to make it easier to find it.
        :type title: str
        """
        if self.check(): return

        return self.Print(title, dict(args=args, kwargs=kwargs))

    def getPPrintStr(self, o: any) -> str:
        """
        :param o: object to be serialized
        :type o: any
        :return: formatted string of the passed object
        :rtype: str
        """
        s = self._pp.pformat(o)
        if self._use_double_quotes: s = s.replace("'", '"')
        return s


    def print_exception(self, e: Exception):
        if self.check(): return

        with self._lock:
            traceback.print_exception(type(e), e, e.__traceback__)

    def get_func_details(self, func: callable, tag: str, result: Any, args, kwargs) -> Tuple[Any, str, str, str, str]:
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
        signature = self.getPPrintStr({ 'args': args, 'kwargs': kwargs })
        pp_result = self.getPPrintStr(result)

        return result, tag, name, signature, pp_result

    def print_signature(self, func: callable, tag: str, *args, **kwargs):
        if not self.debug: return
        assert ('{0}' in tag)

        result = func(*args, **kwargs)
        result, _tag, name, signature, pp_result = self.get_func_details(func, tag, result, args, kwargs)
        self.Print(tag, f'{name}(\n      {signature}\n   )', name, f'returned: \n{self.getPPrintStr(result)}')

        return result

    @classmethod
    def Default(cls): return cls(use_double_quotes=True, end='\n\n')

    @staticmethod
    def Set(_pp):
        """
        :param _pp: Printer class instance to be used for all printing.
        :type _pp: Printer
        """
        assert (isinstance(_pp, Printer))
        global pp
        pp = _pp

pp: Printer = Printer.Default()


def GetFuncModule(func: callable) -> str: return func.__module__
def GetFunctionName(func: callable) -> str:
    if hasattr(func, '__qualname__') and hasattr(func, '__module__'): return f"{func.__module__}.{func.__qualname__}"
    elif hasattr(func, '__qualname__'): return func.__qualname__
    else: return func.__name__
