from infag_parser import parse_file

all_words = parse_file("16Nov29-191756-D150-P10-S10-B150-O1-t64-k0.75-Gfrench.grammar/infag-2")
with open('french_test',"w") as f1:
    for k,v in all_words.items():
        f1.write("{}:{}\n".format(k,v[0]))