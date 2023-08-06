import json
import os
import time
import sys

import tkinter as tk
from PythonDebugTools import *




if __name__ == '__main__':
    class test(object):
        @Debug()
        def pp_run(self, *args, **kwargs):
            return args, kwargs

        @Debug()
        def run(self, *args, **kwargs):
            return args, kwargs

        @DebugTkinterEvent()
        def tk_run(self, event: tk.Event):
            return None

        @CheckTime()
        def timed(self, delay: int, *args, **kwargs):
            time.sleep(delay)
            return args, kwargs

        @CheckTimeWithSignature()
        def timed_sig(self, delay: int, *args, **kwargs):
            time.sleep(delay)
            return args, kwargs

        @StackTrace()
        def stack(self, *args, **kwargs):
            return args, kwargs

        @StackTrace()
        def stack_sig(self, *args, **kwargs):
            return args, kwargs


        @chain()
        def chain_root(self, *args, **kwargs):
            return self.sub1(*args, **kwargs)

        @sub()
        def sub1(self, *args, **kwargs):
            return self.sub2(*args, **kwargs)

        @sub()
        def sub2(self, *args, **kwargs):
            return 'chain.sub.end', args, kwargs



    t = test()

    t.run()
    t.pp_run()
    t.timed(1)
    t.timed_sig(1)

    evt = tk.Event()
    evt.widget = None
    evt.x = None
    evt.y = None
    t.tk_run(evt)


    t.stack(1, 2, 3, test=True, print=False)
    t.stack_sig(1, 2, 3, test=True, print=True)

    t.chain_root()



    path = os.path.abspath(sys.argv[1])

    with open(path, 'r') as f:
        d = json.load(f)

    # Print(getPPrintStr(d))
