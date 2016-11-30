from grammar_generator import write_grammar
from tell_error import tell_missing
import launch_train
import infag_parser
import sys
import subprocess
import tempfile
import os
import re
import math

# change to read from file
def run(grammar_file, output_dir, towrite):
    # write the necessary train.dat file for PyAdaGram
    with open(os.path.join(input_dir,"train.dat"), "w") as f5:
        for j,line in enumerate(towrite):
            if line != '':
                f5.write(line)


    # Start PyAdaGram
    train_proc = subprocess.Popen(["python2 -m launch_train --input_directory={}\
        --output_directory={} --grammar_file={}".format(os.path.join(input_dir), output_dir,grammar_file)], shell = True)
    # Wait for it to finish
    train_proc.communicate()
    rc = train_proc.returncode
    # help with errors
    if rc != 0:
        print("ERROR: the adaptor grammar was unable to parse your files")
        missing_segs = tell_missing(os.path.join(input_dir,"train.dat"), grammar_file)
        if len(missing_segs) >0:
            print("This is due to missing segments in your segfile. You are missing the following:")
            print(missing_segs)
        else:
            print("This error may have been caused by missing files. Please check that the list of words you would like \
            syllabified is in a space-separated file named 'train.dat' in the directory you specified as your input\
             directory, and that your grammar file filename has a valid filename and path.")
    # find the produced inf-ag file
    filename = ""
    infag_regex = re.compile("infag.*")
    for path in os.walk(output_dir):
        for fn in path[2]:
            if infag_regex.match(fn) is not None:
                filename = os.path.join(path[0],fn)

    # parse the file
    all_words = infag_parser.parse_file(filename)
    return all_words

if __name__ == "__main__":
    # write the grammar based on the inputted file
    syllabics = write_grammar(sys.argv[1], "{}".format(sys.argv[3]))
    grammar_file = sys.argv[3]
    input_dir = os.path.split(sys.argv[2])[0]
    input_file = os.path.split(sys.argv[2])[1]
    #change this if you need to inspect infag file
    output_dir = tempfile.mkdtemp()
    
    end =0
    #clean corpus, no words without syllabic segments
    towrite = []
    with open(os.path.join(input_dir, input_file), "r") as f4:
        train_lines = f4.readlines()
        for i,line in enumerate(train_lines):
            for s in syllabics:
                if s in line:
                    towrite.append(line)
                    break
            end = i
    
    # get all the syllabified words
    all_words = run(grammar_file, output_dir, towrite)
    # write to file
    with open(os.path.join(input_dir,"syllabified"), "w") as f2:
        for k,v in all_words.items():
            w = v[0]
            f2.write(k+":"+w+"\n")

