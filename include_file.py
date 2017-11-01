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
import git
from textwrap import dedent

# print all debug info to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

from pandocfilters import toJSONFilter, CodeBlock

def insertfile(key, value, fmt, meta):
    if key == 'CodeBlock':
        [[ident, classes, kvs], code] = value
        kv = {key: value for key, value in kvs}
        if "include" in kv:
            if "git" in kv:
                repo = git.Repo(os.path.abspath(kv["include"]),
                    search_parent_directories=True)
                gitpath = repo.working_tree_dir
                filepath = os.path.abspath(kv["include"])
                relpath = os.path.relpath(filepath, gitpath)
                try:
                    contents = repo.git.show(
                        ":".join([kv["git"], relpath]))
                    lines = contents.splitlines(True)
                except git.exc.GitCommandError:
                    eprint("cannot include file:", "git tag error", kv["git"], "for file:", kv["include"])
                    return None
            elif os.path.isfile(kv["include"]):
                lines = [line for line in open(kv["include"])]
            else:
                eprint("cannot include file:", "file not found:", kv["include"])
                return None
            start = 0
            stop = len(lines)
            if "start" in kv:
                start = int(kv["start"]) - 1
            if "match" in kv:
                eprint("use of *match* is deprecated, use *start* instead")
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
                eprint("use of *pars* is deprecated, use *stop* or *lines* instead")
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
            if "stop" in kv:
                stop = int(kv["stop"])
            # now select lines
            data = "".join(lines[start:stop])
            if "dedent" in kv and kv["dedent"]=="y":
                data = dedent(data)
            return CodeBlock([ident, classes, kvs], data)
    return None

if __name__ == "__main__":
    toJSONFilter(insertfile)
