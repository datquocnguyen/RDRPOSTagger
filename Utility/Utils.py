# -*- coding: utf-8 -*-

def getWordTag(wordTag):
    if wordTag == "///":
        return "/", "/"
    index = wordTag.rfind("/")
    if index == -1:
        return wordTag, None
    word = wordTag[:index].strip()
    tag = wordTag[index + 1:].strip()
    return word, tag

def getRawText(inputFile, outFile):
    out = open(outFile, "w")
    sents = open(inputFile, "r").readlines()
    for sent in sents:
        wordTags = sent.strip().split()
        for wordTag in wordTags:
            word, tag = getWordTag(wordTag)
            out.write(word + " ")
        out.write("\n")
    out.close()
    
def readDictionary(inputFile, encoding='utf-8'):
    dictionary = {}
    lines = open(inputFile, "r", encoding=encoding).readlines()
    for line in lines:
        wordtag = line.strip().split()
        dictionary[wordtag[0]] = wordtag[1]
    return dictionary

