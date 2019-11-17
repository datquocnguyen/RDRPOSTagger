# -*- coding: utf-8 -*-


class Object:
    attributes = [
        "word",
        "tag",
        "prevWord2",
        "prevWord1",
        "nextWord1",
        "nextWord2",
        "prevTag2",
        "prevTag1",
        "nextTag1",
        "nextTag2",
        "suffixL2",
        "suffixL3",
        "suffixL4",
    ]
    code = "def __init__(self"
    for att in attributes:
        code = code + ", " + att + " = None"
    code = code + "):\n"
    for att in attributes:
        code = code + "    self." + att + "=" + att + "\n"

    exec(code)

    def toStr(self):
        res = "("
        for att in Object.attributes:
            boo = eval("isinstance(self. " + att + ", str)")
            if not boo:
                res = res + str(eval("self." + att))
            else:
                res = res + '"' + str(eval("self." + att)) + '"'

            if att != Object.attributes[len(Object.attributes) - 1]:
                res = res + ","
        res += ")"
        return res


def getWordTag(wordTag):
    if wordTag == "///":
        return "/", "/"
    index = wordTag.rfind("/")
    if index == -1:
        return None, None
    word = wordTag[:index].strip()
    tag = wordTag[index + 1 :].strip()
    return word, tag


def getObject(wordTags, index):  # Sequence of "Word/Tag"
    word, tag = getWordTag(wordTags[index])
    preWord1 = preTag1 = preWord2 = preTag2 = ""
    nextWord1 = nextTag1 = nextWord2 = nextTag2 = ""
    suffixL2 = suffixL3 = suffixL4 = ""

    decodedW = word
    if len(decodedW) >= 4:
        suffixL3 = decodedW[-3:]
        suffixL2 = decodedW[-2:]
    if len(decodedW) >= 5:
        suffixL4 = decodedW[-4:]

    if index > 0:
        preWord1, preTag1 = getWordTag(wordTags[index - 1])
    if index > 1:
        preWord2, preTag2 = getWordTag(wordTags[index - 2])
    if index < len(wordTags) - 1:
        nextWord1, nextTag1 = getWordTag(wordTags[index + 1])
    if index < len(wordTags) - 2:
        nextWord2, nextTag2 = getWordTag(wordTags[index + 2])

    return Object(
        word,
        tag,
        preWord2,
        preWord1,
        nextWord1,
        nextWord2,
        preTag2,
        preTag1,
        nextTag1,
        nextTag2,
        suffixL2,
        suffixL3,
        suffixL4,
    )


def getObjectDictionary(initializedCorpus, goldStandardCorpus):
    goldStandardSens = open(goldStandardCorpus, "r").readlines()
    initializedSens = open(initializedCorpus, "r").readlines()

    objects = {}

    j = 0
    for i in range(len(initializedSens)):
        init = initializedSens[i].strip()
        if len(init) == 0:
            continue

        while j < len(goldStandardSens) and goldStandardSens[j].strip() == "":
            j += 1

        if j >= len(goldStandardSens):
            continue

        gold = goldStandardSens[j].strip()
        j += 1

        initWordTags = (
            init.replace("“", "''")
            .replace("”", "''")
            .replace('"', "''")
            .split()
        )
        goldWordTags = (
            gold.replace("“", "''")
            .replace("”", "''")
            .replace('"', "''")
            .split()
        )

        for k in range(len(initWordTags)):
            initWord, initTag = getWordTag(initWordTags[k])
            goldWord, correctTag = getWordTag(goldWordTags[k])

            if initWord != goldWord:
                print(
                    "\nERROR (Raw texts are mismatched || Some sentence is incorrectly formatted):"
                )
                print(
                    str(i + 1)
                    + "th initialized sentence:   "
                    + " ".join(initWordTags)
                )
                print(
                    str(i + 1)
                    + "th gold standard sentence: "
                    + " ".join(goldWordTags)
                )
                return None

            if initTag not in objects.keys():
                objects[initTag] = {}
                objects[initTag][initTag] = []

            if correctTag not in objects[initTag].keys():
                objects[initTag][correctTag] = []

            objects[initTag][correctTag].append(getObject(initWordTags, k))

    return objects


class FWObject:
    """
    RDRPOSTaggerV1.1: new implementation scheme
    RDRPOSTaggerV1.2: add suffixes
    """

    def __init__(self, check=False):
        self.context = [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]
        if check == True:
            i = 0
            while i < 10:
                self.context[i] = "<W>"
                self.context[i + 1] = "<T>"
                i = i + 2
            self.context[10] = "<SFX>"  # suffix
            self.context[11] = "<SFX>"
            self.context[12] = "<SFX>"
        self.notNoneIds = []

    @staticmethod
    def getFWObject(startWordTags, index):
        object = FWObject(True)
        word, tag = getWordTag(startWordTags[index])
        object.context[4] = word
        object.context[5] = tag

        decodedW = word
        if len(decodedW) >= 4:
            object.context[10] = decodedW[-2:]
            object.context[11] = decodedW[-3:]
        if len(decodedW) >= 5:
            object.context[12] = decodedW[-4:]

        if index > 0:
            preWord1, preTag1 = getWordTag(startWordTags[index - 1])
            object.context[2] = preWord1
            object.context[3] = preTag1

        if index > 1:
            preWord2, preTag2 = getWordTag(startWordTags[index - 2])
            object.context[0] = preWord2
            object.context[1] = preTag2

        if index < len(startWordTags) - 1:
            nextWord1, nextTag1 = getWordTag(startWordTags[index + 1])
            object.context[6] = nextWord1
            object.context[7] = nextTag1

        if index < len(startWordTags) - 2:
            nextWord2, nextTag2 = getWordTag(startWordTags[index + 2])
            object.context[8] = nextWord2
            object.context[9] = nextTag2

        return object


#    def isSatisfied(self, fwObject):
#        for i in range(13):
#            key = self.context[i]
#            if (key is not None):
#                if key != fwObject.context[i]:
#                    return False
#        return True
