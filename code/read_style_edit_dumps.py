#!/usr/bin/python
import pdb
# The idea is:
# For each diffedsentences pair in the input file,
# make a corresponding .html file that has deletions deletions in <strike>
# and additions in <strong>.

# Interpret "replace" as a deletion followed by an insertion.

def usage():
    print "./read_style_edit_dumps.py filename1 filename2 etc..."
    print ""
    print "That will make filename1.html and filename2.html etc."
    print "The HTML will have deletions in <strike> and additions in <strong>."
    print "Replacements will be interpreted as a deletion then an insertion."

from lib.text_normalize_filter import text_normalize_filter
from lib.style_edit_finding import plus_and_minus2hunks
import Levenshtein as lev

class AccumulatingHtml:
    def __init__(self):
        self.edits = []

    def accumulate(self, s):
        ''' Listens for a series of diff hunks expressed as strings.
        Intern them.'''
        for edit in plus_and_minus2hunks(s):
            self.edits.append(edit)
        return '' # who cares?
        
    def render(self):
        ret = ''
        for edit in self.edits:
            # We're going to work with growing_html
            growing_html = u''
            
            # First, create something we can Leven
            old = ' '.join(edit.olds)
            new = ' '.join(edit.news)

            # Now, leven them
            editops = lev.editops(old, new)

            last_saw = 0

            for op in editops:
                etype, old_index, new_index = op
                if last_saw < old_index:
                    growing_html += old[last_saw:old_index]
#                    print growing_html
#                    print old[last_saw]
#                    print etype
#                    print old_index
#                    print new_index
#                    print old[last_saw:old_index]
#                    print 'huh'

#                    pdb.set_trace()
                last_saw = old_index
                if etype == 'replace':
                    growing_html += '<strike>' + old[old_index] + '</strike>'
                    growing_html += '<strong>' + new[new_index] + '</strong>'
                    last_saw += 1 
                elif etype == 'insert':
                    growing_html += '<strong>' + new[new_index] + '</strong>'
                elif etype == 'delete':
                    growing_html += '<strike>' + old[old_index] + '</strike>'
                    last_saw += 1 # I think
            # finally, get any remaining junk
            if last_saw < len(old) - 1:
                growing_html += old[last_saw:]

            # Finally, put that in a <p></p>
            ret += "<p>" + growing_html.encode('utf-8') + "</p>"

        return '<html><body>' + ret + '</body></html>'
    
def htmlify(in_name, htmlname = None):
    if htmlname is None:
        htmlname = in_name + ".html"
    accumulated = AccumulatingHtml()

    from xml import sax
    from xml.sax.saxutils import XMLGenerator
    parser = sax.make_parser()
    #XMLGenerator is a special SAX handler that merely writes
    #SAX events back into an XML document
    downstream_handler = XMLGenerator(encoding='utf-8', out = open("/dev/null", 'w'))
    #upstream, the parser, downstream, the next handler in the chain
    filter_handler = text_normalize_filter(parser, downstream_handler, accumulated.accumulate)
    #The SAX filter base is designed so that the filter takes
    #on much of the interface of the parser itself, including the
    #"parse" method
    filter_handler.parse(open(in_name))
    s = accumulated.render()
    fd = open(htmlname, 'w')
    fd.write(s)
    fd.close()

def main():
    import sys
    if len(sys.argv) <= 1:
        print >> sys.stderr, "Going to act as a pipe filter."
        htmlify('/dev/stdin', '/dev/stdout')
    else:
        filenames = sys.argv[1:] # That's right, multiple filenames
        for f in filenames:
            htmlify(f)
    
if __name__ == '__main__':
    main()
