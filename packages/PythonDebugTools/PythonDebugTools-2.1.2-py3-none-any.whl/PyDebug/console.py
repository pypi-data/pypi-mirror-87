import logging
import pprint
import traceback

pp = pprint.PrettyPrinter(indent=4)

__all__ = ['PRINT', 'getPPrintStr', 'print_exception']

def PRINT(title: str, Object: any, logger: logging.Logger = None):
    Print(f"\n ---------------- {title} ---------------- \n\r")
    pp.pprint(Object)
    if logger: logger.debug(f' ---------------- {title} ---------------- \n{pp.pformat(Object)}')



def getPPrintStr(Object: any) -> str:
    return f'{pp.pformat(Object)}'



def print_exception(e: Exception):
    traceback.print_exception(type(e), e, e.__traceback__)
