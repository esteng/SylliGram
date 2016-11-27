import csv
import os
import re
import sys


def parse_file(path):
    all_words = {}
    prefix_regex = re.compile(".*?(?=((?<!\()Word))")
    line_regex=re.compile("Word -> .*")
    just_word = re.compile("Word -> .*? (?=[(])")
    with open(path) as f1: 
        lines =f1.readlines()
    for i, line in enumerate(lines):
        word = ""
        # get lines starting with word -> ...
        prefix = "<UNFOUND>"
        p = prefix_regex.search(line)
        if p is not None:
            prefix = p.group(0).replace("True", "").replace("False", "").strip()
        s = line_regex.search(line)
        if s is not None:
            # split it up, get the onsets and nuclei

            syl_strings = get_syls(s.group(0))

            if syl_strings is not None:
                syllabified_word = ""
                for s in syl_strings:
                    syl = process_syl(s)
                    syllabified_word += syl + " "
                    word +=syl
                if syllabified_word == "":
                    pass
                    # print(line)  

                try:
                    first = all_words[word][1]
                    if first < prefix:
                        all_words[word] = [syllabified_word, prefix] 
                        # print("replacing {}".format(syllabified_word))   
                except KeyError:
                    if "taRabystER" in word:
                        print(line)
                    all_words.update({word: [syllabified_word, prefix]}) 
            else:
                pass
                # print(s.group(0))
    return all_words

def get_syls(string):
    just_syl = re.compile("Syl -> .*?(?=(, Syls ->)|\))")
    return [x.group(0) for x in just_syl.finditer(string)]


def process_syl(string):
    onset_regex = re.compile("Onset -> .*?(?=(Rhyme))")
    rhyme_regex = re.compile("Rhyme -> .*")
    nucleus_regex = re.compile("Nucleus -> .*")
    coda_regex = re.compile("Coda -> .*")
    seg_regex = re.compile("(?<=')[^\s](?=')")

    onset,nucleus,coda,seg=None,None,None,None
    o = onset_regex.search(string)  
    if o is not None:
        onset = "".join(seg_regex.findall(o.group(0)))   
    r = rhyme_regex.search(string)
    if r is not None:
        rhyme = "".join(seg_regex.findall(r.group(0)))
    else:
        return ""
    toret = "" 
    if onset is not None:
        toret+= onset.strip()    
    toret+= rhyme.strip()
    return toret


# if __name__ == '__main__':
#     f2 = open("syllabified", "w")
#     path = sys.argv[1]
#     all_words = parse_file(path)
#     for k,v in all_words.items():
#         w = v[0]
#         f2.write(k+":"+w+"\n")


    # directory = sys.argv[1]    
    # for dir in os.walk(directory):
    #     for file in dir[2]:
    #         if file_regex.match(file):
    #             path = os.path.join(dir[0],file)
    #             all_words = parse_file(path)
    #             for w in all_words:
    #                 f2.write(w + "\n")
    f2.close()
