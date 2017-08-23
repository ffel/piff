#!/usr/bin/env python

'''
Clear included code.

    $ pandoc --filter clear_code.py

see http://pandoc.org/scripting.html
'''

from __future__ import print_function
import sys
import os.path
import re

# print all debug info to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

from pandocfilters import toJSONFilter, CodeBlock

def insertfile(key, value, fmt, meta):
    if key == 'CodeBlock':
        [[ident, classes, kvs], code] = value
        kv = {key: value for key, value in kvs}
        if "include" in kv and os.path.isfile(kv["include"]):
            return CodeBlock([ident, classes, kvs], "")
    return None

if __name__ == "__main__":
    toJSONFilter(insertfile)
