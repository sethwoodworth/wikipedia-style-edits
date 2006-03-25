#!/usr/bin/python
try:
	import psyco
except:
	pass # oh, well
from lib.sentence_matching import transform as sub
from lib.text_normalize_filter import text_normalize_filter
import sys # HACK ALERT
reload(sys)
sys.setdefaultencoding('utf-8')
# Stage 1:

# Use SAX to write a program
# That echoes what input it gets.
# Stage 2:
# Not necessary.

# Stage 3: Make it remove wiki markup.
# Stage 3a: Make it de-wiki 

# Stage 4: Make it mxterminate the de-wiki-markup'd junk.

if __name__ == "__main__":
    import sys
    from xml import sax
    from xml.sax.saxutils import XMLGenerator
    parser = sax.make_parser()
    #XMLGenerator is a special SAX handler that merely writes
    #SAX events back into an XML document
    downstream_handler = XMLGenerator(encoding='utf-8')
    #upstream, the parser, downstream, the next handler in the chain
    filter_handler = text_normalize_filter(parser, downstream_handler, sub)
    #The SAX filter base is designed so that the filter takes
    #on much of the interface of the parser itself, including the
    #"parse" method
    filter_handler.parse(sys.argv[1])
