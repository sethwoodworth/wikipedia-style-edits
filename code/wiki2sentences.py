#!/usr/bin/python
from xml.dom import pulldom
from xml.dom.ext import Print
# Stage 1:

# Use pullparser to write a program
# That echoes what input it gets.

# Stage 2:

# Make it encode the <text> segments as CDATAs.

# Stage 3: Make it remove wiki markup.

# Stage 4: Make it mxterminate the de-wiki-markup'd junk.

def translate(inputfd, outputfd):
    ''' '''
    events = pulldom.parse(inputfd)
    act_counter = 0
    for (event, node) in events:
        Print(node, outputfd)

import sys
translate(sys.stdin, sys.stdout)

