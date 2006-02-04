#!/usr/bin/python

import re
# "Python isn't all that slow."

# The goal is to take lots of raw wikitext input,
# and return one string where "paragraphs" (sections between which
# sentence joining is disallowed) are separated by '\n\n'.

# Time go over the MediaWiki markup list and make a list of how to
# handle them: http://meta.wikimedia.org/wiki/Help:Editing

replacers = [] # compile these all with re.DOTALL and re.MULTILINE and subn them against the input string *in order*

# '''%s''' -> %s
replacers.append((r"'''(.*?)'''", r"\1"))
# ''%s'' -> %s
replacers.append((r"''(.*?)''", r"\1"))
# newlines or whitespace: collapse into a single whitespace - this is unnecessary because the Java will do it for us
#replacers.append((r'\s+', ' '))
# ~~~, ~~~~, ~~~~~ : remove? THINKME
replacers.append((r'(~~~|~~~~|~~~~~)', ''))
# [[Page name]] -> Page name; plus [[:Page name]] - treat as equivalent to [[Page name]] - FIXME wrong for [[:::::::zomg]]
replacers.append((r'\[\[:*([^|]*?)\]\]', r'\1'))
# [[Page name|Some text]] -> Some text
replacers.append((r'\[\[([^|]*?)\|(.*?)\]\]', r'\2'))
# [something://urljunk text] -> text
replacers.append((r'\[[A-Za-z]*://[^\s]*\s(.*?)]', r'\1'))
# == section == (from 1 to 6 '=' allowed): sectionify
replacers.append((r'^======([^\n]*?)======', r'\n\n\1\n\n'))
replacers.append((r'^=====([^\n]*?)=====', r'\n\n\1\n\n'))
replacers.append((r'^====([^\n]*?)====', r'\n\n\1\n\n'))
replacers.append((r'^===([^\n]*?)===', r'\n\n\1\n\n'))
replacers.append((r'^==([^\n]*?)==', r'\n\n\1\n\n'))
replacers.append((r'^=([^\n]*?)=', r'\n\n\1\n\n'))
# ": " at the beginning of a line: New paragraph
replacers.append((r'^:', r'\n\n'))
# * (k >=1 '*' or '#' allowed): Paragraphify.  Terminated by '\n'
replacers.append((r'^[*#]+([^\n]*)', r'\n\n\1\n\n'))
# ; word : definition : Paragraphify both "word" and "definition" FIXME multiline word
replacers.append((r'^\s*;\s*([^\n]+):([^\n]*):\s*', r'\n\n\1\n\n\2\n\n'))
# : indented paragraph : Paragraphify; terminated by '\n'
replacers.append((r'^:([^\n]*?)', r'\n\n\1\n\n'))
# ---- (-> HR): end paragraph, remove markup
replacers.append((r'^----', r'\n\n'))
# [something://urljunk] -> [LINK]  THINKME: I think we could strip these entirely since they don't contribute to sentences.
replacers.append((r'\[[a-z]+://[^]]*?]', '[LINK]'))
# #REDIRECT [[Page name]] -> Page name THINKME
replacers.append((r'^#REDIRECT \[\[(.*?)]]\s*$', r'\n\n\1\n\n'))

# HTML comments
replacers.append((r'<!--(.*?)-->', ''))

## Waa - handle "Just show what I typed" - THINKME
# <math>.*</math> - keep as-is
# Templates: {{.*?}} : split contents on '|'; first: discard; rest: paragraphs


# http://meta.wikimedia.org/wiki/Help:HTML_in_wikitext lists allowed HTML

# <br> - treat as whitespace (THINKME)
replacers.append((r'<br[^>]*>', ' '))
# Tags to collapse away: <tt>, <b>, <strong>, <em>, <i>, <strike>, <s>, <span>, <u>, <big>, <center>, <font>, <hr>, <small>, <var>, <code>
for tag in 'tt', 'b', 'strong', 'em', 'i', 'strike', 's', 'span', 'u', 'big', 'center', 'font', 'hr', 'small', 'var', 'code':
    replacers.append((r'<' + tag + r'[^>]*>', ''))
    replacers.append((r'</' + tag + r'>', ''))
# Tags to keep: <sup>, <sub>
# Tables - handle each row as its own paragraph
# Tags whose contents to treat as paragraphs: <blockquote>, <caption>, <cite>, <dl>, <dt>, <dd>, <h1>, <h2>, <h3>, <h4>, <h5>, <h6>, <li>, <ol>, <p>, <ul>, <pre>, <table>, <td>, <tr>, <tdata>, <th>
for tag in 'blockquote', 'caption', 'cite', 'cite', 'dl', 'dt', 'dd', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'ol', 'p', 'ul', 'pre', 'table', 'td', 'tr', 'tdata', 'th':
    replacers.append((r'<' + tag + r'[^>]*?>', '\n\n'))
    replacers.append((r'</' + tag + r'>', r'\n\n'))
# THINKME - <ruby>, <rb>, <rp>, <rt> - see http://www.w3.org/TR/1999/WD-ruby-19990322/

compileds = [ (re.compile(regex, re.MULTILINE + re.DOTALL), replacement) for regex, replacement in replacers ]

def unformatted_cell(cell):
    ''' Input: A line from a mediawiki table, not including the leading "| "
    Output: A list of lines suitable for joining on \n '''
    if '|' not in cell:
        return ['', '', cell, '', '']
    if '||' in cell: # YOW!  Multiple cells got in here.
        ret = []
        for subthing in cell.split('||'):
            subthing = subthing.strip()
            ret.extend(unformatted_cell(subthing))
        return ret
    first, rest = cell.split('|', 1)
    first, rest = first.strip(), rest.strip()
    if re.search(r'^[a-z]*?=', first):
        return ['', '', rest, '', '']
    return ['', '', first, rest, '', '']

def remove_mediawiki_tables(intext):
    lines = intext.split('\n')
    ret = ''
    IN_TABLE = 0
    for line in lines:
        if line[:2] == '{|': # table begins
            IN_TABLE += 1
            ret += '\n\n'
        if IN_TABLE == 0:
            ret += line + '\n'
        elif line: # we're in a table

            # Remove the silly "!" instead of "|" for heading junk
            if line[0] == '!':
                line = '|' + line[1:]
            line = line.replace('!!', '||')

            # simple goals: Just turn this table into "paragraphs" separated by \n\n
            # make sure to decrement IN_TABLE as appropriate
            if line[:2] == '{|':
                pass # no text on this line, just formatting
            elif line[:2] == '|+':
                ret += line.split("|+", 1)[1] + '\n' # everything after it is text
            elif line[:2] == '|-':
                pass # no text on this line, just formatting
            elif line[:2] == '|}':
                # TABLE OVER!
                IN_TABLE -= 1
                ret += '\n\n'
            elif line[:1] == '|':
                # it's a cell!
                
                ret += '\n'.join(unformatted_cell(line[1:]))
            else:
                ret = ret + line + '\n' # I guess
        else: # line was false
            ret += '\n'
    ### And now a finite-state fixup for when people do '| align="right \n center" | zomg'
    regex = re.compile(r'^[a-zA-Z]+=[^\n]*\n\n\s*[^\n]* \|\n', re.MULTILINE + re.DOTALL)
    ret = regex.sub('\n\n', ret)
    return ret

import htmlentitydefs
def de_htmlify(uns):
    ''' Turn &quot; (etc.), &#51648; (etc.), and &#033; from the input
    Unicode string into actual Unicode text in the output.'''
    # Named entities
    for entity in htmlentitydefs.name2codepoint:
        uns = uns.replace('&' + entity + ';', unichr(htmlentitydefs.name2codepoint[entity]))
    # Numbered Unicode entities
    finder = re.compile(r'&#(\d*?);')
    for match in finder.findall(uns):
        uns = uns.replace('&#' + match + ';', unichr(int(match)))
    return uns

def remove_template_references(s):
    ret = ''
    splitted = re.split('{{(.*?)}}', s)
    for k in xrange(len(splitted)):
        element = splitted[k]
        if k % 2 == 0: # if it's even, replace it verbatim
            ret += element + '\n\n'
        else: # if it's odd, ignore
            ret += '\n\n'.join(element.split('|')[1:]) + '\n\n'
    return ret

def sub(s):
    unicodetext = unicode(s, 'utf-8')
    # Remove HTML junk
    unicodetext = de_htmlify(unicodetext)
    # Clean out MW tables
    unicodetext = remove_mediawiki_tables(unicodetext)
    unicodetext = remove_template_references(unicodetext)
    # Now do my magic markup model
    for regex, replacement in compileds:
        unicodetext = regex.sub(replacement, unicodetext)
    return unicodetext.encode('utf-8')


# Each bullet point should be its own paragraph.
# Each '\n\n' should stop a paragraph.
