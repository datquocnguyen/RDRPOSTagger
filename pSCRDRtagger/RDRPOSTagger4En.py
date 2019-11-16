# -*- coding: utf-8 -*-

import os
import sys

os.chdir("../")
sys.setrecursionlimit(100000)
sys.path.append(os.path.abspath(""))
os.chdir("./pSCRDRtagger")

from multiprocessing import Pool
from InitialTagger.InitialTagger4En import (
    initializeEnCorpus,
    initializeEnSentence,
)
from SCRDRlearner.Object import FWObject
from SCRDRlearner.SCRDRTree import SCRDRTree
from SCRDRlearner.SCRDRTreeLearner import SCRDRTreeLearner
from Utility.Config import NUMBER_OF_PROCESSES, THRESHOLD
from Utility.Utils import getWordTag, getRawText, readDictionary
from Utility.LexiconCreator import createLexicon


def unwrap_self_RDRPOSTagger4En(arg, **kwarg):
    return RDRPOSTagger4En.tagRawEnSentence(*arg, **kwarg)


class RDRPOSTagger4En(SCRDRTree):
    """
    RDRPOSTagger for English
    """

    def __init__(self):
        self.root = None

    def tagRawEnSentence(self, DICT, rawLine):
        line = initializeEnSentence(DICT, rawLine)
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

    def tagRawEnCorpus(self, DICT, rawCorpusPath):
        lines = open(rawCorpusPath, "r").readlines()
        # Change the value of NUMBER_OF_PROCESSES to obtain faster tagging process!
        pool = Pool(processes=NUMBER_OF_PROCESSES)
        taggedLines = pool.map(
            unwrap_self_RDRPOSTagger4En,
            zip([self] * len(lines), [DICT] * len(lines), lines),
        )
        with open(rawCorpusPath + ".TAGGED", "w") as out:
            for line in taggedLines:
                out.write(line + "\n")
        print("\nOutput file: " + rawCorpusPath + ".TAGGED")


def printHelp():
    print("\n===== Usage =====")
    print(
        "\n#1: To train RDRPOSTagger for English on a gold standard training corpus with Penn Treebank POS tags:"
    )
    print(
        "\npython RDRPOSTagger4En.py train PATH-TO-GOLD-STANDARD-TRAINING-CORPUS"
    )
    print("\nExample: python RDRPOSTagger4En.py train ../data/en/goldTrain")
    print(
        "\n#2: To use the trained model for POS tagging on a raw English text corpus:"
    )
    print(
        "\npython RDRPOSTagger4En.py tag PATH-TO-TRAINED-MODEL PATH-TO-LEXICON PATH-TO-RAW-TEXT-CORPUS"
    )
    print(
        "\nExample: python RDRPOSTagger4En.py tag ../data/en/goldTrain.RDR ../data/en/goldTrain.DICT ../data/en/rawTest"
    )
    print("\n#3: Find the full usage at http://rdrpostagger.sourceforge.net !")


def run(args=sys.argv[1:]):
    if len(args) == 0:
        printHelp()
    elif args[0].lower() == "train":
        try:
            print("\n====== Start ======")
            print(
                "\nGenerate from the gold standard training corpus an English lexicon "
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
            initializeEnCorpus(DICT, args[1] + ".RAW", args[1] + ".INIT")
            print(
                "\nLearn a tree model of rules for English POS tagging from %s and %s"
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
            r = RDRPOSTagger4En()
            print("\n=> Read an English POS tagging model from " + args[1])
            r.constructSCRDRtreeFromRDRfile(args[1])
            print("\n=> Read an English lexicon from " + args[2])
            DICT = readDictionary(args[2])
            print("\n=> Perform English POS tagging on " + args[3])
            r.tagRawEnCorpus(DICT, args[3])
        except Exception as e:
            print("\nERROR ==> ", e)
            printHelp()
    else:
        printHelp()


if __name__ == "__main__":
    run()
    pass
