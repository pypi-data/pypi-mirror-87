from .console import getPPrintStr




DEFAULT_TAG = '\n______________________________________________________________\n"{0}"'
END_TAG = '\n=============================================================\n'



def GetFuncModule(func: callable) -> str:
    return func.__module__



def GetFunctionName(func: callable) -> str:
    if hasattr(func, '__qualname__'):
        return func.__qualname__
    elif hasattr(func, '__module__'):
        return f"{func.__module__}.{func.__qualname__}"
    else:
        return func.__name__



def print_signature(func: callable, tag: str, *args, **kwargs):
    assert ('{0}' in tag)
    name = GetFunctionName(func)
    Print(tag.format(f'{name}'))

    if args or kwargs:
        # try: args_repr = [repr(a) for a in args]  # 1
        # except: args_repr = [str(a) for a in args]  # 1
        #
        # kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        #
        # signature = ", ".join(args_repr + kwargs_repr)  # 3
        #
        # Print(f"{name}(\n{signature}\n)")
        signature = getPPrintStr({'kwargs': kwargs, 'args': args, })
        Print(f"{name}(\n      {signature}\n   )")
        result = func(*args, **kwargs)
        Print(f"{name}  returned: \n{getPPrintStr(result)}\n")
