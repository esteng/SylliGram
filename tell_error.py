

def tell_missing(trainfile, segfile):
    orig_phones = set()
    with open(trainfile) as f1:
        lines1 = f1.readlines()
    for line in lines1:
        splitline = line.strip().split(" ")
        [orig_phones.update(x) for x in splitline]



    with open(segfile) as f2:
        lines2 = f2.readlines()
    new_phones = set()
    for line in lines2:
        splitline = line.strip().split(",")
        [new_phones.update(x) for x in splitline]

    missing_set = orig_phones-new_phones
    return list(missing_set)