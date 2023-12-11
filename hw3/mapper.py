import sys

for line in sys.stdin:
    line = line.strip()
    words = line.split(',')
    if words[0] == "Event":
        continue
    print(words[0], 1, sep=',')