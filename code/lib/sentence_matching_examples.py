#!/usr/bin/python

import sentence_matching

for from_s, to_s in (
    ("the other day", "the other day"),
    ("the other day", "the other days"),
    ("With regard to the 9 members of the Nepalese royal family, that the killing was purpotrated by one of their relatives has no bearing on whether their killings were 'assassinations' per se; it is assumed that the killing was indeed political, however, so we keep it.", "With regard to the 9 members of the Nepalese royal family, that the killing was perpetrated by one of their relatives has no bearing on whether their killings were 'assassinations' per se; it is assumed that the killing was indeed political, however, so we keep it."),
    ('Towns and muncipalities','Towns and municipalities'),
    ('Air Canada A330', 'Airbus A330-300 of Air Canada (C-GHLM) on the approach to London (Heathrow) Airport.'),
    ('Martin Luther defended his teachings and calls for reform from April 16 - April 18, 1521, and refused to recant.','Luther was called upon to recant his teachings, yet he defended them and called for reform from April 16 - April 18, 1521.')):
    print jaccard_two_sentences(from_s, to_s), "Via: {%s} {%s}" % (from_s, to_s)
