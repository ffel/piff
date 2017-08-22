#!/usr/bin/env python

'''
Include code from code files

    $ pandoc --filter include_file.py

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
            # https://stackoverflow.com/q/3277503
            lines = [line for line in open(kv["include"])]
            start = 0
            stop = len(lines)
            if "start" in kv:
                start = int(kv["start"]) - 1
            if "match" in kv:
                patt = re.compile(kv["match"])
                for l in range(start, stop):
                    if patt.search(lines[l]):
                        start = l
                        break
            if "lines" in kv:
                nr_lines = int(kv["lines"])
                if nr_lines >= 0 and start+nr_lines < stop:
                    stop = start+nr_lines
            if "pars" in kv:
                nr_pars = int(kv["pars"])
                between_pars = False
                for l in range(start, stop):
                    if lines[l].isspace():
                        if not between_pars:
                            between_pars = True
                            nr_pars -= 1
                            if nr_pars <= 0:
                                stop = l
                                break
                    else:
                        between_pars = False
            if "indent" in kv:
                nr_indents = int(kv["indent"])
                pre = leading(lines[start])
                for l in range(start+1, stop):
                    if not lines[l].isspace():
                        if pre == leading(lines[l]):
                            nr_indents -= 1
                            if nr_indents <= 0:
                                stop = l+1 # include that last line as well
                                break
            data = "".join(lines[start:stop])
            return CodeBlock([ident, classes, kvs], data)
    return None

# find white space leading in s
def leading(s):
    m = re.search(r"^(\s*)", s)
    return m.group(0)

if __name__ == "__main__":
    toJSONFilter(insertfile)