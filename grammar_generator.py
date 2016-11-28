#!/usr/bin/python
# -*- coding: utf8 -*-

import sys 

def write_grammar(seg_file, grammar_file):
    with open(seg_file) as f0:
        seglines = f0.readlines()
    try:
        assert(len(seglines)<=3 and len(seglines)>=2)
    except AssertionError:
        print "ERROR: segment file must have less than 3 and more than 2 lines"

    syllabics = seglines[0].split(",")
    nonsyllabics = seglines[1].split(",")
    try:
        liquids = seglines[2].split(",")
    except IndexError:
        liquids = None

    header = "% non-terminals\n\
Word ->  Syls\n\
Syls ->  Syl\n\
Syls ->  Syl Syls\n\
\n\
% adapted non-terminals\n\
@ Word 1500 100 0\n\
Syl ->  Rhyme\n\
Syl ->  Onset Rhyme\n\
Rhyme -> Nucleus\n\
Rhyme -> Nucleus Coda\n\
Onset -> Consonant\n\
Onset -> Consonant Consonants\n\
Coda -> Consonant\n\
Coda -> Consonant Consonants\n\
Consonants -> Consonant\n\
Consonants -> Consonant Consonants\n\
Nucleus -> Vowel\n\
Nucleus -> Consonant\n\
\n\
%terminals\n"

    
    with open(grammar_file, "w") as f1:
        f1.write(header)

        for vowel in syllabics:
            f1.write('Vowel -> "{}"'.format(vowel.strip()) + "\n")
        if liquids:
            for seg in liquids:
                f1.write('Vowel -> "{}"'.format(seg.strip())+ "\n")
        for c in nonsyllabics:
            f1.write('Consonant -> "{}"'.format(c.strip())+ "\n")

        

# try:
#     write_grammar(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
# except IndexError:
#      write_grammar(sys.argv[1], sys.argv[2], sys.argv[3])
