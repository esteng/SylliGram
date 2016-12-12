import csv
import os
import re
import sys


def parse_file(path):
    words = 0
    all_words = {}
    # find the number + line
    prefix_regex = re.compile(".*?(?=((?<!\()Word))")
    # find valid lines
    line_regex=re.compile("True.*Word -> .*")
    # find word without number/True
    just_word = re.compile("Word -> .*? (?=[(])")
    with open(path) as f1: 
        lines =f1.readlines()
    for i, line in enumerate(lines):
        word = ""
        # get lines starting with Word -> ...
        prefix = "<UNFOUND>"
        p = prefix_regex.search(line)
        if p is not None:
            # get the probability for the line (expansion)
            prefix = p.group(0).replace("True", "").replace("False", "").strip()
        # make sure the expansion is valid
        s = line_regex.search(line)
        if s is not None:
            words +=1
            # split it up, get the onsets and nuclei
            syl_strings = get_syls(line)
            if syl_strings is not None:
                syllabified_word = ""
                for syl in syl_strings:
                    # get rid of the Syl -> string
                    syl = re.sub("Syl -> ", "", syl)
                    # strip it, add the syllable followed by a space
                    syllabified_word += re.sub("\s","",syl) + " "
                    word +=syl
                    word = word.strip()
                    word = re.sub("\s","",word)
                if syllabified_word == "":
                    pass
                # if the new probability is greater than existing, replace the expansion with more probable one
                try:
                    first = all_words[word][1]
                    if first < prefix:
                        all_words[word] = [syllabified_word, prefix] 
                        # print("switching {} to {} because {} < {} ".format(all_words[word][0], syllabified_word, first, prefix))   
                except KeyError:
                    all_words.update({word: [syllabified_word, prefix]}) 
            else:
                pass
    return all_words

# find all Syl -> xxx strings
def get_syls(string):
    # just_syl = re.compile("Syl -> .*?(?=(, Syls ->)|$)")
    syl_regex = re.compile("(?<!\()Syl ->.*?(?=\()")
    # syl_regex = re.compile("Syl -> [\w\d ]+ ")
    return syl_regex.findall(string)
    # return [x.group(0) for x in just_syl.finditer(string)]

# deprecated (from older grammar format)
# keep in case we go back to similar format
def process_syl(string):
    onset_regex = re.compile("Onset -> .+?(?= \()")
    nucleus_regex = re.compile("Nucleus -> .+?(?= \()")
    coda_regex = re.compile("(?!<\()Coda -> .+?(?= \()")
    seg_regex = re.compile("(?<=')[^\s](?=')")
    rhyme_regex = re.compile("(?<!\()Rhyme -> .+?(?= \()")

    onset,nucleus,coda,seg=None,None,None,None
    o = onset_regex.search(string)  
    if o is not None:
        onset = o.group(0).replace("Onset -> ","").strip()
    # n = nucleus_regex.search(string)
    # c = coda_regex.search(string)
    # nucleus = n.group(0)
    # rhyme = nucleus.replace("Nucleus -> ","").strip()
    # rhyme= rhyme.strip()
    # if c:
    #     coda = c.group(0).replace("Coda -> ","")

    #     rhyme+=coda.strip()
    # else:
    #     return ""
    r = rhyme_regex.search(string)
    rhyme = r.group(0)
    rhyme = rhyme.replace("Rhyme -> ", "")
    rhyme = re.sub("\s","", rhyme)
    toret = "" 
    if onset is not None:
        toret+= onset.strip()    
    toret+= rhyme.strip()
    
    toret = re.sub("\s", "", toret)

    return toret

