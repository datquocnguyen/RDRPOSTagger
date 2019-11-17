# -*- coding: utf-8 -*-

import re


def initializeEnSentence(FREQDICT, sentence):
    words = sentence.strip().split()
    taggedSen = []
    for word in words:
        if word in ["“", "”", '"']:
            taggedSen.append("''/" + FREQDICT["''"])
            continue

        tag = ""
        lowerW = word.lower()
        if word in FREQDICT:
            tag = FREQDICT[word]
        elif lowerW in FREQDICT:
            tag = FREQDICT[lowerW]
        else:
            if re.search(r"([0-9]+-)|(-[0-9]+)", word) is not None:
                tag = "JJ"
            elif re.search(r"[0-9]+", word) is not None:
                tag = "CD"
            elif (
                re.search(
                    r"(.*ness$)|(.*ment$)|(.*ship$)|(^[Ee]x-.*)|(^[Ss]elf-.*)",
                    word,
                )
                is not None
            ):
                tag = "NN"
            elif re.search(r".*s$", word) is not None and word[0].islower():
                tag = "NNS"
            elif word[0].isupper():
                tag = "NNP"
            elif (
                re.search(
                    r"(^[Ii]nter.*)|(^[nN]on.*)|(^[Dd]is.*)|(^[Aa]nti.*)", word
                )
                is not None
            ):
                tag = "JJ"
            elif re.search(r".*ing$", word) is not None and word.find("-") < 0:
                tag = "VBG"
            elif re.search(r".*ed$", word) is not None and word.find("-") < 0:
                tag = "VBN"
            elif (
                re.search(
                    r"(.*ful$)|(.*ous$)|(.*ble$)|(.*ic$)|(.*ive$)|(.*est$)|(.*able$)|(.*al$)",
                    word,
                )
                is not None
                or word.find("-") > -1
            ):
                tag = "JJ"
            elif re.search(r".*ly$", word) is not None:
                tag = "RB"
            else:
                tag = "NN"

        taggedSen.append(word + "/" + tag)

    return " ".join(taggedSen)


def initializeEnCorpus(FREQDICT, inputFile, outputFile):
    lines = open(inputFile, "r").readlines()

    with open(outputFile, "w") as fileOut:
        for line in lines:
            fileOut.write(initializeEnSentence(FREQDICT, line) + "\n")
