def pred_1(s):
    return sum(map(lambda c: s.count(c), "aeiou")) >= 3

def pred_2(s):
    for i, c in enumerate(s[:-1]):
        if c == s[i + 1]:
            return True

    return False

def pred_3(s):
    return all(map(lambda x: x not in s, ["ab", "cd", "pq", "xy"]))

def pred_4(s):
    pairs = map(lambda a: a[0] + a[1], (zip(s[:-1], s[1:])))

    for pair in pairs:
        i = s.find(pair)
        j = s.rfind(pair)

        if j - i > 1:
            return True

    return False

def pred_5(s):
    for i, c in enumerate(s[:-2]):
        if c == s[i + 2]:
            return True

    return False

def nice1(s):
    s = s.strip()
    return pred_1(s) and pred_2(s) and pred_3(s)

def nice2(s):
    s = s.strip()
    return pred_4(s) and pred_5(s)


if __name__ == '__main__':
    import sys

    if sys.argv[1] == 'one':
        nice_strs = list(filter(nice1, sys.stdin.readlines()))
    else:
        nice_strs = list(filter(nice2, sys.stdin.readlines()))

    print("Found {} nice strings".format(len(nice_strs)))

