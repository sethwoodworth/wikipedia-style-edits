import sentence_matching
import mytokenize
import Levenshtein as lev
t = mytokenize.TreebankSedExpecter()

import style_edit_finding 
def is_content_edit(hunk):
    ''' Start easy. '''
    return not style_edit_finding.is_hunk_style_edit(hunk)

def sans_typos(hunk):
    ''' Fix up the olds and news in the hunk with our best guess for
    typo fixes.'''
    # Tokenize the olds and news first then add special-case testing
    # that ensures that the prev and next char to the start and end of
    # a chunk of edits is not ' '
    old = u' '.join([' '.join(t.tokenize(k)) for k in hunk.olds])
    new = u' '.join([' '.join(t.tokenize(k)) for k in hunk.news])

    eo = lev.editops(old, new)

    typo_fixes = sentence_matching.only_typo_editops(eo)
    print typo_fixes
    wanted = sentence_matching.only_not_full_token_changing_edit_ops(typo_fixes, old, new)
    print wanted
    old = lev.apply_edit(wanted, old, new)

    hunk.olds = [old]
    hunk.news = [new]
    return hunk

