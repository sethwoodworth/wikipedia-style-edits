#!/usr/bin/python
from lib.remove_wiki_markup import sub
from lib.text_normalize_filter import text_normalize_filter
# Stage 1:

# Use SAX to write a program
# That echoes what input it gets.
# Stage 2:
# Not necessary.

# Stage 3: Make it remove wiki markup.
# Stage 3a: Make it de-wiki 

# Stage 4: Make it mxterminate the de-wiki-markup'd junk.

cache = {}
def pipe_through_opennlp(s):
	global cache
	if len(cache) > 5000:
		cache = {} # dumb, I know
	from lib.rwpopen import rwpopen
	paragraphs = s.split('\n\n')
	ret = []
	for paragraph in paragraphs:
		if paragraph in cache:
			ret.append(cache[paragraph])
		else:
			result = rwpopen(paragraph, './lib/opennlp-wrap.sh')
			cache[paragraph] = result
			ret.append(cache[paragraph])
	return '\n\n'.join(ret)

if __name__ == "__main__":
    import sys
    from xml import sax
    from xml.sax.saxutils import XMLGenerator
    parser = sax.make_parser()
    #XMLGenerator is a special SAX handler that merely writes
    #SAX events back into an XML document
    downstream_handler = XMLGenerator(encoding='utf-8')
    #upstream, the parser, downstream, the next handler in the chain
    filter_handler = text_normalize_filter(parser, downstream_handler, pipe_through_opennlp)
    #The SAX filter base is designed so that the filter takes
    #on much of the interface of the parser itself, including the
    #"parse" method
    filter_handler.parse(sys.argv[1])
