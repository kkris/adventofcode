import hashlib

def hash(key, number):
    value = key + str(number).encode('utf-8')
    return hashlib.md5(value).hexdigest()

def find_lowest_with_prefix(key, prefix):
    i = 1

    while True:
        h = hash(key, i)
        if h.startswith(prefix):
            return i, h

        i += 1

if __name__ == '__main__':
    import sys

    prefix = sys.argv[1]
    key = sys.stdin.read().strip().encode('utf-8')

    number, h = find_lowest_with_prefix(key, prefix)

    print("Found {} with hash {}".format(number, h))
