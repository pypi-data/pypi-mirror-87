# author: Min Latt
# website: http://minlaxz.me

# import necessary packages
from __future__ import print_function
import logxs
import re

def find_method(name, pretty_print=True, module=None):
    if not module:
        module = logxs

    p = ".*{}.*".format(name)
    filtered = filter(lambda x: re.search(p, x, re.IGNORECASE), dir(module))
        
    if not pretty_print:
        return filtered

    for (i, func_name) in enumerate(filtered):
        print("{}. {}".format(i + 1, func_name))
