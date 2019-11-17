# -*- coding: utf-8 -*-

import os
import sys
from multiprocessing import Pool

os.chdir("../")
sys.setrecursionlimit(100000)
sys.path.append(os.path.abspath(""))
os.chdir("./pSCRDRtagger")

from InitialTagger.InitialTagger4Vn import (
    initializeVnCorpus,
    initializeVnSentence,
)
from SCRDRlearner.Object import FWObject
from SCRDRlearner.SCRDRTree import SCRDRTree
from SCRDRlearner.SCRDRTreeLearner import SCRDRTreeLearner
from Utility.Config import NUMBER_OF_PROCESSES, THRESHOLD
from Utility.LexiconCreator import createLexicon
from Utility.Utils import getRawText, getWordTag, readDictionary


def unwrap_self_RDRPOSTagger4Vn(arg, **kwarg):
    return RDRPOSTagger4Vn.tagRawVnSentence(*arg, **kwarg)


class RDRPOSTagger4Vn(SCRDRTree):
    """
    RDRPOSTagger for Vietnamese
    """

    def __init__(self):
        self.root = None

    def tagRawVnSentence(self, DICT, rawLine):
        line = initializeVnSentence(DICT, rawLine)
        sen = []
        wordTags = line.split()
        for i in range(len(wordTags)):
            fwObject = FWObject.getFWObject(wordTags, i)
            word, tag = getWordTag(wordTags[i])
            node = self.findFiredNode(fwObject)
            if node.depth > 0:
                sen.append(word + "/" + node.conclusion)
            else:  # Fired at root, return initialized tag
                sen.append(word + "/" + tag)
        return " ".join(sen)

    def tagRawVnCorpus(self, DICT, rawCorpusPath):
        lines = open(rawCorpusPath, "r").readlines()
        # Change the value of NUMBER_OF_PROCESSES to obtain faster tagging process!
        pool = Pool(processes=NUMBER_OF_PROCESSES)
        taggedLines = pool.map(
            unwrap_self_RDRPOSTagger4Vn,
            zip([self] * len(lines), [DICT] * len(lines), lines),
        )
        with open(rawCorpusPath + ".TAGGED", "w") as out:
            for line in taggedLines:
                out.write(line + "\n")
        print("\nOutput file: " + rawCorpusPath + ".TAGGED")


def printHelp():
    print("\n===== Usage =====")
    print(
        "\n#1: To train RDRPOSTagger for Vietnamese on a gold standard training corpus with VietTreebank/VLSP POS tags:"
    )
    print(
        "\npython RDRPOSTagger4Vn.py train PATH-TO-GOLD-STANDARD-TRAINING-CORPUS"
    )
    print("\nExample: python RDRPOSTagger4Vn.py train ../data/vn/goldTrain")
    print(
        "\n#2: To use the trained model for POS tagging on a raw Vietnamese text corpus:"
    )
    print(
        "\npython RDRPOSTagger4Vn.py tag PATH-TO-TRAINED-MODEL PATH-TO-LEXICON PATH-TO-RAW-TEXT-CORPUS"
    )
    print(
        "\nExample: python RDRPOSTagger4Vn.py tag ../data/vn/goldTrain.RDR ../data/vn/goldTrain.DICT ../data/vn/rawTest"
    )
    print("\n#3: Find the full usage at http://rdrpostagger.sourceforge.net !")


def run(args=sys.argv[1:]):
    if len(args) == 0:
        printHelp()
    elif args[0].lower() == "train":
        try:
            print("\n====== Start ======")
            print(
                "\nGenerate from the gold standard training corpus a Vietnamese lexicon "
                + args[1]
                + ".DICT"
            )
            createLexicon(args[1], "full")
            createLexicon(args[1], "short")
            print(
                "\nExtract from the gold standard training corpus a raw text corpus "
                + args[1]
                + ".RAW"
            )
            getRawText(args[1], args[1] + ".RAW")
            print(
                "\nPerform initially POS tagging on the raw text corpus, to create "
                + args[1]
                + ".INIT"
            )
            DICT = readDictionary(args[1] + ".sDict")
            initializeVnCorpus(DICT, args[1] + ".RAW", args[1] + ".INIT")
            print(
                "\nLearn a tree model of rules for Vietnamese POS tagging from %s and %s"
                % (args[1], args[1] + ".INIT")
            )
            rdrTree = SCRDRTreeLearner(THRESHOLD[0], THRESHOLD[1])
            rdrTree.learnRDRTree(args[1] + ".INIT", args[1])
            print("\nWrite the learned tree model to file " + args[1] + ".RDR")
            rdrTree.writeToFile(args[1] + ".RDR")
            print("\nDone!")
            os.remove(args[1] + ".INIT")
            os.remove(args[1] + ".RAW")
            os.remove(args[1] + ".sDict")
        except Exception as e:
            print("\nERROR ==> ", e)
            printHelp()
    elif args[0].lower() == "tag":
        try:
            r = RDRPOSTagger4Vn()
            print("\n=> Read a Vietnamese POS tagging model from " + args[1])
            r.constructSCRDRtreeFromRDRfile(args[1])
            print("\n=> Read a Vietnamese lexicon from " + args[2])
            DICT = readDictionary(args[2])
            print("\n=> Perform Vietnamese POS tagging on " + args[3])
            r.tagRawVnCorpus(DICT, args[3])
        except Exception as e:
            print("\nERROR ==> ", e)
            printHelp()
    else:
        printHelp()


if __name__ == "__main__":
    run()
    pass
