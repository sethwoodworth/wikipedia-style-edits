import style_edit_finding
import sentence_matching
import mytokenize
import Levenshtein as lev
t = mytokenize.TreebankSedExpecter()

import style_edit_finding 
def is_content_edit(hunk):
    ''' Start easy. '''
    return not style_edit_finding.is_hunk_style_edit(hunk)

def hunks_sans_typos(hunk):
    ''' Fix up the olds and news in the hunk with our best guess for
    typo fixes.'''
    # Tokenize the olds and news first then add special-case testing
    # that ensures that the prev and next char to the start and end of
    # a chunk of edits is not ' '

    assert(type(hunk.olds) == type([]))
    assert(type(hunk.news) == type([]))

    old = u' '.join([u' '.join(k) for k in hunk.olds])
    new = u' '.join([u' '.join(k) for k in hunk.news])

    old = sentence_matching.old_sans_typos(old, new) # take that, tyops!

    if old.lower() == new.lower(): # You, too, capitalization!
        return False

    hunk.olds = [old]
    hunk.news = [new]
    return hunk

def content_edits_sub(s):
    return style_edit_finding.format_interesting(s=s, fn=is_content_edit)

def hunks_sans_typos_sub(s):
    return style_edit_finding.format_interesting(s=s, fn=hunks_sans_typos)
