#!/usr/bin/python
import pdb
import psyco
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

import xml.dom.pulldom as pulldom

def doTag(saxxer, tag, characters, attrs = {}):
    saxxer.startElement(tag, attrs)
    saxxer.characters(characters)
    saxxer.endElement(tag)

def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

import lib.Levenshtein as lev # !??!!
from lib.style_edit_finding import plus_and_minus2hunks
from xml.sax.saxutils import XMLGenerator

class StyleEditAggregator:
    def __init__(self, fd):
        ''' Takes an fd as an input.
        Creates a lot of internal state as a result. '''
        self.current_page = ''
        self.result = []
        self.parse(fd)

    def parse(self, fd):
        events = pulldom.parse(fd)
        for (event, node) in events:
            if event == 'START_ELEMENT':
                if node.tagName == 'title':
                    events.expandNode(node)
                    self.current_page = getText(node.childNodes)
                elif node.tagName == 'revision':
                    events.expandNode(node)
                    eyedee = getText(node.getElementsByTagName('id')[0].childNodes)
                    text = getText(node.getElementsByTagName('text')[0].childNodes)
                    if text:
                        self.result.append( (self.current_page, eyedee, plus_and_minus2hunks(text)) )

    def to_html(self, outfd=None):
        exgen = XMLGenerator(out=outfd, encoding='utf-8')
        exgen.startElement('html', {})
        exgen.startElement('head', {})
        doTag(exgen, 'meta', '', {'http-equiv': "Content-Type", 'content': "text/html;charset=utf-8"})
        exgen.endElement('head')
        exgen.startElement('body', {})
        exgen.startElement('ul', {})

        for page, eyedee, editer in self.result:
            for edit in editer:
                exgen.startElement('li', {})
                
                exgen.characters(page + ' - ')
                exgen.characters('id=' + eyedee + ' ')

                # First, create something we can Leven
                old = u' '.join(edit.olds)
                new = u' '.join(edit.news)

                # Now, leven them
                editops = lev.editops(old, new)

                last_saw = 0


                growing_replaces_olds = ''
                growing_replaces_news = ''

                for k in range(len(editops)):
                    op = editops[k]
                    etype, old_index, new_index = op
                    if last_saw < old_index:
                        exgen.characters(old[last_saw:old_index])
                    last_saw = old_index
                    if etype == 'replace':
                        # keep growing the replace until it's done
                        growing_replaces_olds += old[old_index]
                        growing_replaces_news += new[new_index]
                        if k+1 < len(editops) and editops[k+1][0] == 'replace':
                            # then don't do anything
                            pass
                        else:
                            doTag(exgen, 'strike', growing_replaces_olds)
                            doTag(exgen, 'u', growing_replaces_news)
                            growing_replaces_olds = ''
                            growing_replaces_news = ''
                        last_saw += 1 
                    elif etype == 'insert':
                        doTag(exgen, 'u', new[new_index])
                    elif etype == 'delete':
                        doTag(exgen, 'strike', old[old_index])
                        last_saw += 1 # I think
                # finally, get any remaining junk
                if last_saw < len(old) - 1:
                    exgen.characters(old[last_saw:])

                exgen.endElement('li')
    
        exgen.endElement('ul')
        exgen.endElement('body')
        exgen.endElement('html')
            
