#!/usr/bin/python
# Hacking at XML with regular expressions is great fun.

import re
try:
    import psyco
except:
    pass

titler = re.compile(r'<title>(.*?)</title>', re.DOTALL)
ider = re.compile(r'<id>(\d*?)</id>', re.DOTALL)

def needle_position(needle, haystack, start = 0, end=-1):
    found = haystack.find(needle, start, end)
    if found != -1:
        return found + len(needle)
    return found

def title_position(s, start = 0, end = -1):
    return needle_position('<title>', s, start, end)

def title_string(s):
    return titler.search(s).group(1)

def revision_position(s, start = 0):
    start = s.find('<revision>')
    #end = s.find('</revision>', start)
    #if end != -1:
    #    return start
    return start

def id_value(s, start = 0):
    return int(ider.search(s, start).group(1))

def revision_start_end(s, start = 0):
    full_tag = needle_position('<text xml:space="preserve">', s, start)
    short_tag = needle_position('<text xml:space="preserve" />', s, start)
    if (full_tag < 0) or (short_tag < full_tag): # then we return info about the empty tag
        return short_tag, short_tag
    elif full_tag > -1:
        return full_tag, revision_end(s, full_tag)
    return -1

def revision_end(s, start = 0):
    needle = '</text>'
    ret = s.find(needle, start)
    return ret

def fd2csv(fd):
    # variables controlling state
    ret = [] # to store (title, revision_id, start_offset, length)
    title = ''

    # ASSUME that no revision is more than 4MiB long :-)
    SLURPSIZE = 65536 * 1024
    chunk = fd.read(SLURPSIZE) # a "character array", not decoded Unicode
    offset = 0
    # now we get to use multiline regexes

    while chunk:
        start = 0
        length = 0
        # we've got a chunk in hand.
        revision_pos = revision_position(chunk)
        #print revision_pos
        title_pos = title_position(chunk, end=revision_pos)
        #print title_pos
        # if there's a title before a revision, use that and slurp
        if title_pos != -1 and \
           title_pos < revision_pos:
            #print 'looking for title',offset
            title = title_string(chunk)
            start = title_pos
            length = 0 # who cares?, so long as we don't match it next time
            chunk = chunk[start + length:]
            offset += start + length
            chunk += fd.read(SLURPSIZE - len(chunk))
        elif revision_pos != -1: # if title_match was None, or if it was after a revision
            #print 'looking for rev',offset
            revision_id = id_value(chunk, revision_pos)
            start, end = revision_start_end(chunk, revision_pos)
            length = end - start
            #print 'length',length
            tup = (title, revision_id, start + offset, length)
            ret.append(tup)
            chunk = chunk[start + length:]
            offset += start + length
            chunk += fd.read(SLURPSIZE - len(chunk))
        else: # if there was no match of any kind found
            #print len(chunk)
            #print 'offset ended at',offset
            return ret


if __name__ == '__main__':
    import sys
    import csv
    writer = csv.writer(sys.stdout)
    writer.writerows(fd2csv(sys.stdin))
