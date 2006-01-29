#!/usr/bin/python

# "Python isn't all that slow."

# The goal is to take lots of raw wikitext input,
# and return a list of "paragraphs".

# Time go over the MediaWiki markup list and make a list of how to
# handle them: http://meta.wikimedia.org/wiki/Help:Editing

# ''%s'' -> %s
# '''%s''' -> %s
# newlines or whitespace: collapse into a single whitespace
# ": " at the beginning of a line: New paragraph
# ~~~, ~~~~, ~~~~~ : remove? THINKME
# == section == (from 2 to 4 '=' allowed): sectionify
# * (k >=1 '*' or '#' allowed): Paragraphify.  Terminated by '\n'
# ; word : definition : Paragraphify both "word" and "definition"
# : indented paragraph : Paragraphify; terminated by '\n'
# ---- (-> HR): end paragraph, remove markup
# [[Page name]] -> Page name
# [[Page name|Some text]] -> Some text
# [something://urljunk text] -> text
# [something://urljunk] -> renders as [1], [2], etc.  THINKME: I think we should strip these entirely since they don't contribute to sentences.  Maybe [LINK] or something?
# #REDIRECT [[Page name]] -> Page name THINKME
# [[:Page name]] - treat as equivalent to [[Page name]]

## Waa - handle "Just show what I typed" - THINKME
# Tables - handle each row as its own paragraph :-(
# <math>.*</math> - keep as-is
# Templates: {{.*?}} : split contents on '|'; first: discard; rest: paragraphs


# http://meta.wikimedia.org/wiki/Help:HTML_in_wikitext lists allowed HTML

# <br> - treat as whitespace (THINKME)
# Tags to collapse away: <tt>, <b>, <strong>, <em>, <i>, <strike>, <s>, <span>, <u>, <big>, <center>, <font>, <hr>, <small>
# Tags to keep: <sup>, <sub>
# Tags to FIXME: HTML comments, <var>, <code>, 
# Tags whose contents to treat as paragraphs: <blockquote>, <caption>, <cite>, <dl>, <dt>, <dd>, <h1>, <h2>, <h3>, <h4>, <h5>, <h6>, <li>, <ol>, <p>, <ul>, <pre>, <table>, <td>, <tr>, <td>, <th>

# THINKME - <ruby>, <rb>, <rp>, <rt> - see http://www.w3.org/TR/1999/WD-ruby-19990322/


# Each bullet point should be its own paragraph.
# Each '\n\n' should stop a paragraph.
