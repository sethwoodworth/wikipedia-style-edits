## Yeah, to be fair, this doesn't include the

import style_edit_finding 
def is_content_edit(hunk):
    return not style_edit_finding.is_hunk_style_edit(hunk)

