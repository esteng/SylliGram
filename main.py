from grammar_generator import write_grammar
from tell_error import tell_missing
import launch_train
import infag_parser
import sys
import subprocess
import tempfile
import os
import re

# change to read from file
def main():
    write_grammar(sys.argv[1], "{}".format(sys.argv[3]))

    grammar_file = sys.argv[3]
    input_dir = sys.argv[2]
    output_dir = tempfile.mkdtemp()
    print(output_dir)

    train_proc = subprocess.Popen(["python2 -m launch_train --input_directory={}\
        --output_directory={} --grammar_file={}".format(input_dir, output_dir,grammar_file)], shell = True)
    train_proc.communicate()
    rc = train_proc.returncode
    if rc != 0:
        print "ERROR: the adaptor grammar was unable to parse your files"
        missing_segs = tell_missing(os.path.join(input_dir, "train.dat"), grammar_file)
        if len(missing_segs >0):
            print "This is due to missing segments in your segfile. You are missing the following:"
            print missing_segs
        else:
            "This error may have been caused by missing files. Please check that the list of words you would like \
            syllabified is in a space-separated file named 'train.dat' in the directory you specified as your input\
             directory, and that your grammar file filename has a valid filename and path."

    filename = ""
    infag_regex = re.compile("infag.*")
    for path in os.walk(output_dir):
        for fn in path[2]:
            if infag_regex.match(fn) is not None:
                filename = os.path.join(path[0],fn)


    all_words = infag_parser.parse_file(filename)
    with open("syllabified", "w") as f2:
        for k,v in all_words.items():
            w = v[0]
            f2.write(k+":"+w+"\n")

if __name__ == "__main__":
    main()