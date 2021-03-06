#!/usr/bin/python
# Hacking at XML with regular expressions is great fun.

import re
from lib.remove_wiki_markup import de_htmlify

DEBUG=1
def debug(o):
    if DEBUG:
        print o

# Method: Make two lists
# One of all the title events:
# title_events = [(35, "Alchemy"), (2003, "Banana")]

try:
    import psyco # always give it a shot...

except:
    pass

titler = re.compile(r'<title>(.*?)</title>', re.DOTALL)

def needle_position(needle, haystack, start = 0, end=-1):
    found = haystack.find(needle, start, end)
    if found != -1:
        return found + len(needle)
    return found

def title_position(s, start = 0, end = -1):
    return needle_position('<title>', s, start, end)

def title_string(s):
    s = titler.search(s).group(1)
    u = s.decode('utf-8')
    s = de_htmlify(u).encode('utf-8')
    return s

def fd2lists(fd):
    ''' Takes the file object called "fd" and returns
    a list of title events, e.g. [(35, "Alchemy"), (2003, "Banana")]'''
    ret = []

    # ASSUME that no revision is more than 64MiB long :-)
    SLURPSIZE = 65536 * 1024
    chunk = fd.read(SLURPSIZE) # a "character array", not decoded Unicode
    offset = 0
    # now we get to use multiline regexes

    while chunk:
        title_pos = title_position(chunk)
        if title_pos > -1:
            title = title_string(chunk) # FIXME: call can be optimized to include title_pos
            start = title_pos
            length = 0 # who cares?, so long as we don't match it next time
            ret.append((offset + title_pos, title))
            chunk = chunk[title_pos:]
            offset += title_pos
            chunk += fd.read(SLURPSIZE - len(chunk))
        else:
            return ret # we're done

if __name__ == '__main__':
    import sys
    import csv
    p = csv.parser()
    values = fd2lists(sys.stdin)
    for vals in values:
        print p.join(vals)
