#!/usr/bin/python
# Hacking at XML with regular expressions is great fun.

if __name__ == '__main__':
    import sys
    import csv
    titleparser = csv.parser()
    revparser = csv.parser()
    try:
        titles = open(sys.argv[1])
        revs = open(sys.argv[2])
    except:
        print "Usage: %s title-file.csv revision-file.csv" % sys.argv[0]
        raise AssertionError()

    titledata = []
    for line in titles.xreadlines():
        offset, title = titleparser.parse(line)
        titledata.append((int(offset), title))

    for line in revs.xreadlines():
        offset, length, eyedee = revparser.parse(line)
        offset, length = int(offset), int(length)
        # if the offset is less than the first titledata, then we're doomed
        if offset < titledata[0][0]:
            raise AssertionError("OMG")
        # Now we know it's >= titledata[0][0]
        # if it's > titledata[1][0], then we should pop titledata
        elif len(titledata) > 1 and  offset > titledata[1][0]:
            print 'I popped!'
            print titledata[0]
            title = titledata.pop(0)[1]
        else:
            title = titledata[0][1]
        # finally, spew that to stdout
        print revparser.join((title, offset, length, eyedee))
