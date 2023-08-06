from __future__ import absolute_import, print_function, division
try:
    from future_builtins import zip, map # Use Python 3 "lazy" zip, map
except ImportError:
    pass

has_pylogix			= False
try:
    import pylogix
    has_pylogix			= True
except Exception:
    pass

