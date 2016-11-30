#!/usr/bin/python3

import sys
import collections

wordDict = {}
for line in sys.stdin:
    word = line.split("\t")[0]
    if word in wordDict:
        wordDict[word] += 1
    else:
        wordDict[word] = 1

sortedDict = collections.OrderedDict(sorted(wordDict.items()))
for key in sortedDict:
    print (key, sortedDict[key])
