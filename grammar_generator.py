#!/usr/bin/python
# -*- coding: utf8 -*-

import sys 

def write_grammar(seg_file, grammar_file):
    with open(seg_file) as f0:
        seglines = f0.readlines()
    try:
        assert(len(seglines)<=3 and len(seglines)>=2)
    except AssertionError:
        print("ERROR: segment file must have less than 3 and more than 2 lines")

    syllabics = seglines[0].split(",")
    nonsyllabics = seglines[1].split(",")
    try:
        liquids = seglines[2].split(",")
    except IndexError:
        liquids = None
    # this is the header, potentially what needs to be changed
    header = "% non-terminals\n\
Word ->  Syls\n\
\n\
% adapted non-terminals\n\
@ Word 100 500 0\n\
@ Syl 1000 10 10\n\
@ Rhyme 2500 10 10\n\
\n\
Syls ->  Syl\n\
Syls ->  Syl Syls\n\
Syl -> Rhyme\n\
Syl -> Rhyme2\n\
Syl -> Onset Rhyme\n\
Syl -> Onsets Rhyme\n\
Syl -> Onset Rhyme2\n\
Syl -> Onsets Rhyme2\n\
Rhyme -> Nucleus\n\
Rhyme2 -> Nucleus Coda\n\
Onset -> Consonant\n\
Onsets -> Consonants\n\
Nucleus -> Vowels\n\
Coda -> Consonants\n\
Consonants -> Consonant\n\
Consonants -> Consonant Consonants\n\
Vowels -> Vowel\n\
Vowels -> Vowel Vowels\n\
\n\
%terminals\n"

    # write the terminals
    with open(grammar_file, "w") as f1:
        f1.write(header)

        for vowel in syllabics:
            f1.write('Vowel -> "{}"'.format(vowel.strip()) + "\n")
        if liquids:
            for seg in liquids:
                f1.write('Vowel -> "{}"'.format(seg.strip())+ "\n")
        for c in nonsyllabics:
            f1.write('Consonant -> "{}"'.format(c.strip())+ "\n")
    return syllabics
        
