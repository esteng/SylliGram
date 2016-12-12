import sys

from nltk.metrics import edit_distance




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

for line in lines2:
    splitline = line.split(":")
    found_words[splitline[0]] = splitline[1]
    

words = 0
found = False
distances = {}


# compare each word found to the corresponding word in the corpus, if it doesn't match, increment unfound
for k,v in true_words.items():
    try:
        if found_words[k].strip() == v.strip():
            # print("{} matches to {}".format(found_words[k].strip(), v.strip()))
            try:
                distances[0] +=1
            except KeyError:
                distances[0] =1
            found = True
        else:
            # print("{} doesnt match {}".format(found_words[k].strip(), v.strip()))
            distance = edit_distance(found_words[k].strip(), v.strip())
            try:
                distances[distance] +=1
            except KeyError:
                distances[distance] = 1 
            unfound += 1
        words +=1

    except KeyError:
        pass



print("{} remained unmatched".format(unfound))
print("matched {} out of {}, which is {}%".format((words - unfound), words, float(100* (words - unfound)/words)))

for k in sorted(distances.keys()):
    print("distance: {}, frequency: {}".format(k, distances[k]))

# with open("/Users/Elias/550FinalProject/distances","w") as f2:
#     for k in sorted(distances.keys()):
#         f2.write(str(k) + ",")
#     for k in sorted(distances.keys()):
#         f2.write(str(distances[k])+",")



lengthlist = [len(x) for x in found_words.keys()]
print("average word length was {}".format(sum(lengthlist)/len(lengthlist)))

print("there were {} words".format(words))




