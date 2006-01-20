#!/usr/bin/python
# Hacking at XML with regular expressions is great fun.

import re

DEBUG=0
def debug(o):
    if DEBUG:
        print o
# GOAL:
# print out a CSV with an index of revisions
# play dumb and don't try to know anything about the titles
# This list of events looks like [(offset, length, rev_id), ...]

try:
    import psyco
except:
    pass

ider = re.compile(r'<id>(\d*?)</id>', re.DOTALL)

def needle_position(needle, haystack, start = 0, end=-1):
    found = haystack.find(needle, start, end)
    if found != -1:
        return found + len(needle)
    return found

def revision_position(s, start = 0, end = -1):
    start = s.find('<revision>', start, end)
    return start

def id_value(s, start = 0):
    return int(ider.search(s, start).group(1))

def revision_start_end(s, start = 0):
    full_tag = needle_position('<text xml:space="preserve">', s, start)
    short_tag = needle_position('<text xml:space="preserve" />', s, start)
    # if we found the short tag,
    if short_tag > -1:
        # and, if the short tag appears *before* the long tag
        if short_tag < full_tag:
            # pick that one
            return short_tag, short_tag
    return full_tag, revision_end(s, full_tag)

def revision_end(s, start = 0):
    needle = '</text>'
    ret = s.find(needle, start)
    return ret

def fd2lists(fd):
    ''' Takes the file object called "fd" and returns
    a list of revision events'''
    ret = []

    # ASSUME that no revision is more than 64MiB long :-)
    SLURPSIZE = 65536 * 1024
    chunk = fd.read(SLURPSIZE) # a "character array", not decoded Unicode
    offset = 0
    # now we get to use multiline regexes

    while chunk:
        start, end = revision_start_end(chunk)
        if start > -1:
            id = id_value(chunk) # might even be safe...
            length = end - start
            assert(length >= 0)
            ret.append((offset + start, length, id))
            chunk = chunk[end:] # get away!
            offset += end
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
