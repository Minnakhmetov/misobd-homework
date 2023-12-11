import sys

word2count = {}

for line in sys.stdin:
    word, _ = line.split(',')

    try:
        word2count[word] = word2count[word] + 1
    except:
        word2count[word] = 1

for word in sorted(word2count.keys()):
    print(word, word2count[word])