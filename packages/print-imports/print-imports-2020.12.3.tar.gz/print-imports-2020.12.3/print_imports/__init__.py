import sys

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

old_import = builtins.__import__


def my_import(name, *args, **kwargs):
    if name not in sys.modules:
        print('importing --> {}'.format(name))
    return old_import(name, *args, **kwargs)

builtins.__import__ = my_import
