import sys


file1 = sys.argv[1]
file2 = sys.argv[2]

with open(file1) as f1:
    lines1 = f1.readlines()
with open(file2) as f2:
    lines2 = f2.readlines()

print(len(lines1), len(lines2))

true_words ={}
found_words = {}

unfound = 0
for line in lines1:
    splitline = line.split(":")
    true_words[splitline[0]] = splitline[1]
    if "ReORdone" in line:
        print("Mapping {} to {}".format(splitline[0], splitline[1]))

for line in lines2:
    splitline = line.split(":")
    found_words[splitline[0]] = splitline[1]
    


found = False
for k,v in true_words.items():
    try:
        if found_words[k].strip() == v.strip():
            # print("{} matches to {}".format(found_words[k].strip(), v.strip()))
            found = True

    except KeyError:
        pass
        print("{} not in found_words".format(k))
        unfound+=1
    if not found:
        unfound += 1
        print("{} has no match".format(k.strip()))


print("{} remained unmatched".format(unfound))
print("matched {} out of {}, which is {}%".format((len(lines1) - unfound), len(lines1), 100* (len(lines1) - unfound)/len(lines1)))






