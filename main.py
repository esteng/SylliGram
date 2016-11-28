from grammar_generator import write_grammar
import launch_train
import infag_parser
import sys
import subprocess
import tempfile
import os
import re

write_grammar("5IYE/A{aQO}VU@iye&aouUA0O3E:", "pbtdkgNmnlRrfvTDszSZjxGhw*", "{}".format(sys.argv[2]))

grammar_file = sys.argv[2]
input_dir = sys.argv[1]
output_dir = tempfile.mkdtemp()
print(output_dir)

train_proc = subprocess.Popen(["python2 -m launch_train --input_directory={}\
    --output_directory={} --grammar_file={}".format(input_dir, output_dir,grammar_file)], shell = True)
train_proc.communicate()

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
