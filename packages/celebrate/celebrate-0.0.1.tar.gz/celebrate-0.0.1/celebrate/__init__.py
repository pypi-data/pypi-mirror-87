__version__ = "0.0.1"

import builtins
from copy import deepcopy
import pdb
import sys
import importlib

OLDETYPE = deepcopy(builtins.type)
OLDEOBJECT = deepcopy(builtins.object)

# class Celebration(object):
#
#     def __init__(cls, name=None, arg1=None, arg2=None):
#         print(f'CONGRATULATIONS YOU HAVE DECLARED {name}')
#         sys.stdout.flush()
#         try:
#             globals()['OLDETYPE'](cls)
#         except:
#             globals()['OLDETYPE'](cls, name, arg1, arg2)
#         # except:
#         #     if all([a is None for a in (name, arg1, arg2)]):
#         #
#         #     else:
#         #         return globals()['OLDETYPE'].__new__(cls, name, arg1, arg2)

class Celebration(object):
    def __init__(self, *args, **kwargs):
        print('YOU MADE IT')
        sys.stdout.flush()
        globals()['OLDEOBJECT'].__init__(self, *args, **kwargs)

    def __new__(cls, *args, **kwargs):
        print('AND THEN SOME!!!!')
        sys.stdout.flush()
        return globals()['OLDEOBJECT'].__new__(cls, *args, **kwargs)



builtins.object = Celebration
importlib.reload(builtins)