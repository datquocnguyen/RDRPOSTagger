# -*- coding: utf-8 -*-

import os
import sys
# os.chdir("../")
# sys.setrecursionlimit(100000)
# sys.path.append(os.path.abspath(""))
# os.chdir("./Utility")

import re
from Utility.Utils import getWordTag

def add2WordTagFreqDict(word, tag, inDict):
    if word not in inDict:
        inDict[word] = {}
        inDict[word][tag] = 1
    else:
        if tag not in inDict[word]:
            inDict[word][tag] = 1
        else:
            inDict[word][tag] += 1

def createLexicon(corpusFilePath, fullLexicon):
    if fullLexicon not in ['full', 'short']:
        print("The second parameter gets 'full' or 'short' string-value!")
        print("No lexicon is generated!!!")
        return
    #elif fullLexicon == 'full':
    #    print "Creating a full .DICT lexicon from the gold standard training corpus", corpusFilePath
    #else:
    #    print "Creating a short .sDict lexicon which excludes word types appearing 1 time in the gold standard training corpus"
    
    lines = open(corpusFilePath, "r").readlines()
    wordTagCounter = {}
    for i in range(len(lines)):
        # print i
        pairs = lines[i].strip().replace("“", "''").replace("”", "''").replace("\"", "''").split()
        for pair in pairs:
            word, tag = getWordTag(pair)
            if (len(word) >= (len(pair) - 1)) or (len(tag) >= (len(pair) - 1)):
                if fullLexicon == 'full':
                    print("ERROR: The %sth sentence is incorrectly formatted!" % str(i+1))
                    #print(pair)
            else:
                add2WordTagFreqDict(word, tag, wordTagCounter)
    
    from operator import itemgetter
    dictionary = {}
    suffixDictCounter = {}
    
    tagCounter_Alphabet = {}
    tagCounter_CapitalizedWord = {}
    tagCounter_Numeric = {}
    
    for word in wordTagCounter:
        tagFreq4Word = wordTagCounter[word]
        pairs = list(tagFreq4Word.items())
        pairs.sort(key = itemgetter(1), reverse = True)
        tag = pairs[0][0]
        
        decodedWord = word
        isCapital = decodedWord[0].isupper()
              
        if fullLexicon == 'full':
            dictionary[word] = tag
        else:# Get the lexicon without 1-time-occurrence word types
            if (len(pairs) == 1 and  pairs[0][1] > 1) or len(pairs) > 1:
                dictionary[word] = tag
                
        if re.search(r"[0-9]+", word) != None:
            if tag not in tagCounter_Numeric:
                tagCounter_Numeric[tag] = 1
            else:
                tagCounter_Numeric[tag] += 1
        else:
            if isCapital:
                if tag not in tagCounter_CapitalizedWord:
                    tagCounter_CapitalizedWord[tag] = 1
                else:
                    tagCounter_CapitalizedWord[tag] += 1
            else:
                if tag not in tagCounter_Alphabet:
                    tagCounter_Alphabet[tag] = 1
                else:
                    tagCounter_Alphabet[tag] += 1
        
            if len(decodedWord) >= 4:
                suffix = ".*" + decodedWord[-3:]
                add2WordTagFreqDict(suffix, tag, suffixDictCounter)
                suffix = ".*" + decodedWord[-2:]
                add2WordTagFreqDict(suffix, tag, suffixDictCounter)
            if len(decodedWord) >= 5:
                suffix = ".*" + decodedWord[-4:]
                add2WordTagFreqDict(suffix, tag, suffixDictCounter)
            if len(decodedWord) >= 6:
                suffix = ".*" + decodedWord[-5:]
                add2WordTagFreqDict(suffix, tag, suffixDictCounter)
        
    from collections import OrderedDict
    dictionary = OrderedDict(sorted(dictionary.items(), key = itemgetter(0)))
    
    # Get the most frequent tag in the lexicon to label unknown words and numbers
    tagCounter_Alphabet = OrderedDict(sorted(tagCounter_Alphabet.items(), key = itemgetter(1), reverse = True))
    tagCounter_CapitalizedWord = OrderedDict(sorted(tagCounter_CapitalizedWord.items(), key = itemgetter(1), reverse = True))
    tagCounter_Numeric = OrderedDict(sorted(tagCounter_Numeric.items(), key = itemgetter(1), reverse = True))
    tag4UnknWord = list(tagCounter_Alphabet.keys())[0]
    tag4UnknCapitalizedWord = tag4UnknWord
    tag4UnknNum = tag4UnknWord
    if len(tagCounter_CapitalizedWord) > 0:
        tag4UnknCapitalizedWord = list(tagCounter_CapitalizedWord.keys())[0]
    if len(tagCounter_Numeric) > 0:
        tag4UnknNum = list(tagCounter_Numeric.keys())[0]
    
    # Write to file
    fileSuffix = ".sDict"
    if fullLexicon == 'full':
        fileSuffix = ".DICT"
    fileOut = open(corpusFilePath + fileSuffix, "w")
    
    
    fileOut.write("TAG4UNKN-WORD " + tag4UnknWord + "\n")
    fileOut.write("TAG4UNKN-CAPITAL " + tag4UnknCapitalizedWord + "\n")
    fileOut.write("TAG4UNKN-NUM " + tag4UnknNum + "\n")
    for key in dictionary:
        fileOut.write(key + " " + dictionary[key] + "\n")
    
    for suffix in suffixDictCounter:
        tagFreq4Suffix = suffixDictCounter[suffix]
        pairs = list(tagFreq4Suffix.items())
        pairs.sort(key = itemgetter(1), reverse = True)
        tag = pairs[0][0]
        freq = pairs[0][1]
        if len(suffix) == 7 and freq >= 2:
            fileOut.write(suffix + " " + tag + "\n")
        if len(suffix) == 6 and freq >= 3:
            fileOut.write(suffix + " " + tag + "\n")
        if len(suffix) == 5 and freq >= 4:
            fileOut.write(suffix + " " + tag + "\n")
        if len(suffix) == 4 and freq >= 5:
            fileOut.write(suffix + " " + tag + "\n")
            
    fileOut.close()
