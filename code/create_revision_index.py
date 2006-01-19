#!/usr/bin/python
# Hacking at XML with regular expressions is great fun.

import re
try:
    import psyco
except:
    pass

titler = re.compile(r'<title>(.*?)</title>', re.DOTALL)
id_and_content = re.compile(r'<revision>\n *<id>(\d*)</id>.*?<text xml:space="preserve">(.*?)</text>', re.DOTALL)

def fd2csv(fd):
    # variables controlling state
    ret = [] # to store (title, revision_id, start_offset, length)
    title = ''

    # ASSUME that no revision is more than 64MiB long :-)
    SLURPSIZE = 65536 * 1024
    chunk = fd.read(SLURPSIZE) # a "character array", not decoded Unicode
    offset = 0
    # now we get to use multiline regexes

    while chunk:
        start = 0
        length = 0
        # we've got a chunk in hand.
        title_match = titler.search(chunk)
        id_and_content_match = id_and_content.search(chunk)
        # if the title_match is before the id_and_content match, then take the new title and adance
        if title_match is not None and \
           (id_and_content_match is None or \
            title_match.start() < id_and_content_match.start()):
            title = title_match.group(1)
            start = title_match.start()
            length = title_match.end() - title_match.start()
            chunk = chunk[start + length:]
            offset += start + length
            chunk += fd.read(SLURPSIZE - len(chunk))
        elif id_and_content_match is not None: # if title_match was None, or if it was after a revision
            revision_id = int(id_and_content_match.group(1))
            start = id_and_content_match.start(2)
            length = id_and_content_match.end(2) - id_and_content_match.start(2)
            tup = (title, revision_id, start + offset, length)
            ret.append(tup)
            chunk = chunk[start + length:]
            offset += start + length
            chunk += fd.read(SLURPSIZE - len(chunk))
        else: # if there was no match of any kind found
            return ret


if __name__ == '__main__':
    import sys
    import csv
    writer = csv.writer(sys.stdout)
    writer.writerows(fd2csv(sys.stdin))
