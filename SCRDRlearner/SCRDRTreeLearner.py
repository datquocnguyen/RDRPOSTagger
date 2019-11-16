# -*- coding: utf-8 -*-

from .Node import Node
from .Object import getObjectDictionary
from .SCRDRTree import SCRDRTree


# Generate concrete rules based on input object of 5-word window context object
def generateRules(object):
    # 1. Current word
    rule1 = 'object.word == "' + object.word + '"'
    # 2. Next 1st word
    rule2 = 'object.nextWord1 == "' + object.nextWord1 + '"'
    # 3. Next 2nd word
    rule3 = 'object.nextWord2 == "' + object.nextWord2 + '"'
    # 4. Previous 1st word
    rule4 = 'object.prevWord1 == "' + object.prevWord1 + '"'
    # 5. Previous 2nd word
    rule5 = 'object.prevWord2 == "' + object.prevWord2 + '"'

    # 6. Current word and next 1st word
    rule6 = rule1 + " and " + rule2
    # 7. Previous 1st word and current word
    rule7 = rule4 + " and " + rule1
    # 11. Previous 1st word and next 1st word
    rule11 = rule4 + " and " + rule2
    # 29. Next 1st word and next 2nd word
    # rule29 = rule2 + " and " + rule3
    # 30. Previous 2nd word and previous 1st word
    # rule30 = rule5 + " and " + rule4
    # 19. Current word and next 2nd word
    rule19 = rule1 + " and " + rule3
    # 20. Previous 2nd word and current word
    rule20 = rule5 + " and " + rule1

    # 8. Current word, next 1st word and next 2nd word
    rule8 = rule6 + " and " + rule3
    # 9. Previous 2nd word, previous 1st word and current word
    rule9 = rule5 + " and " + rule7
    # 10. Previous 1st word, current word and next 1st word
    rule10 = rule4 + " and " + rule6

    # 12. Next 1st tag
    rule12 = 'object.nextTag1 == "' + object.nextTag1 + '"'
    # 13. Next 2nd tag
    rule13 = 'object.nextTag2 == "' + object.nextTag2 + '"'
    # 14. Previous 1st tag
    rule14 = 'object.prevTag1 == "' + object.prevTag1 + '"'
    # 15. Previous 2nd tag
    rule15 = 'object.prevTag2 == "' + object.prevTag2 + '"'
    # 16. Next 1st tag and next 2nd tag
    rule16 = rule12 + " and " + rule13
    # 17. Previous 2nd tag and previous 1st tag
    rule17 = rule15 + " and " + rule14
    # 18. Previous 1st tag and next 1st tag
    rule18 = rule14 + " and " + rule12

    # 21. Current word and next 1st tag
    rule21 = rule1 + " and " + rule12
    # 22. Current word and previous 1st tag
    rule22 = rule14 + " and " + rule1
    # 23. Previous 1st tag, current word and next 1st tag
    rule23 = rule14 + " and " + rule21
    # 24. Current word and 2 next tags.
    rule24 = rule1 + " and " + rule16
    # 25. 2 previous tags and current word
    rule25 = rule17 + " and " + rule1
    # 26. 2-character suffix
    rule26 = 'object.suffixL2 == "' + object.suffixL2 + '"'
    # 27. 3-character suffix
    rule27 = 'object.suffixL3 == "' + object.suffixL3 + '"'
    # 28. 4-character suffix
    rule28 = 'object.suffixL4 == "' + object.suffixL4 + '"'

    rules = []
    rules.append(rule1)
    rules.append(rule2)
    rules.append(rule3)
    rules.append(rule4)
    rules.append(rule5)
    rules.append(rule6)
    rules.append(rule7)
    rules.append(rule8)
    rules.append(rule9)
    rules.append(rule10)
    rules.append(rule11)
    rules.append(rule12)
    rules.append(rule13)
    rules.append(rule14)
    rules.append(rule15)
    rules.append(rule16)
    rules.append(rule17)
    rules.append(rule18)
    rules.append(rule19)
    rules.append(rule20)
    rules.append(rule21)
    rules.append(rule22)
    rules.append(rule23)
    rules.append(rule24)
    rules.append(rule25)
    rules.append(rule26)
    rules.append(rule27)
    rules.append(rule28)
    # rules.append(rule29)
    # rules.append(rule30)

    rules = set(rules)
    return rules


def countMatching(objects, ruleNotIn):
    counts = {}
    matchedObjects = {}
    for object in objects:
        rules = generateRules(object)
        for rule in rules:
            if rule in ruleNotIn:
                continue
            counts[rule] = counts.setdefault(rule, 0) + 1
            matchedObjects.setdefault(rule, []).append(object)
    return counts, matchedObjects


def satisfy(object, rule):
    return eval(rule)


def fire(rule, cornerstoneCases):
    for object in cornerstoneCases:
        if satisfy(object, rule):
            return True
    return False


def generateRulesFromObjectSet(objects):
    res = []
    for object in objects:
        rules = generateRules(object)
        res += rules
    return res


class SCRDRTreeLearner(SCRDRTree):
    def __init__(self, iThreshold=2, mThreshold=2):
        self.improvedThreshold = iThreshold
        self.matchedThreshold = mThreshold

    # For layer-2 exception structure
    def findMostImprovingRuleForTag(
        self, startTag, correctTag, correctCounts, wrongObjects
    ):
        impCounts, affectedObjects = countMatching(wrongObjects, [])

        maxImp = -1000000
        bestRule = ""
        for rule in impCounts:
            temp = impCounts[rule]
            if rule in correctCounts:
                temp -= correctCounts[rule]

            if temp > maxImp:
                maxImp = temp
                bestRule = rule

        if maxImp == -1000000:
            affectedObjects[bestRule] = []

        return bestRule, maxImp, affectedObjects[bestRule]

    def findMostEfficientRule(self, startTag, objects, correctCounts):
        maxImp = -1000000
        rule = ""
        correctTag = ""
        cornerstoneCases = []

        for tag in objects:
            if tag == startTag:
                continue
            if (
                len(objects[tag]) <= maxImp
                or len(objects[tag]) < self.improvedThreshold
            ):
                continue

            ruleTemp, imp, affectedObjects = self.findMostImprovingRuleForTag(
                startTag, correctTag, correctCounts, objects[tag]
            )
            if imp >= self.improvedThreshold and imp > maxImp:
                maxImp = imp
                rule = ruleTemp
                correctTag = tag
                cornerstoneCases = affectedObjects

        needToCorrectObjects = {}
        errorRaisingObjects = []
        if maxImp > -1000000:
            for tag in objects:
                if tag != correctTag:
                    for object in objects[tag]:
                        if satisfy(object, rule):
                            needToCorrectObjects.setdefault(tag, []).append(
                                object
                            )
                            if tag == startTag:
                                errorRaisingObjects.append(object)

        return (
            rule,
            correctTag,
            maxImp,
            cornerstoneCases,
            needToCorrectObjects,
            errorRaisingObjects,
        )

    def findMostMatchingRule(self, matchingCounts):
        correctTag = ""
        bestRule = ""
        maxCount = -1000000

        for tag in matchingCounts:
            for rule in matchingCounts[tag]:
                if (
                    matchingCounts[tag][rule] >= self.matchedThreshold
                    and matchingCounts[tag][rule] > maxCount
                ):
                    maxCount = matchingCounts[tag][rule]
                    bestRule = rule
                    correctTag = tag

        return bestRule, correctTag

    def buildNodeForObjectSet(self, objects, root):
        cornerstoneCaseRules = generateRulesFromObjectSet(
            root.cornerstoneCases
        )

        matchingCounts = {}
        matchingObjects = {}
        for tag in objects:
            matchingCounts[tag], matchingObjects[tag] = countMatching(
                objects[tag], cornerstoneCaseRules
            )

        total = 0
        for tag in objects:
            total += len(objects[tag])

        currentNode = root
        elseChild = False
        while True:
            rule, correctTag = self.findMostMatchingRule(matchingCounts)

            if rule == "":
                break

            cornerstoneCases = matchingObjects[correctTag][rule]

            needToCorrectObjects = {}
            for tag in objects:
                if rule in matchingObjects[tag]:
                    if tag != correctTag:
                        needToCorrectObjects[tag] = matchingObjects[tag][rule]
                    for object in matchingObjects[tag][rule]:
                        rules = generateRules(object)
                        for rule1 in rules:
                            if rule1 not in matchingCounts[tag]:
                                continue
                            matchingCounts[tag][rule1] -= 1

            node = Node(
                rule,
                'object.conclusion = "' + correctTag + '"',
                currentNode,
                None,
                None,
                cornerstoneCases,
            )

            if not elseChild:
                currentNode.exceptChild = node
                elseChild = True
            else:
                currentNode.elseChild = node

            currentNode = node
            self.buildNodeForObjectSet(needToCorrectObjects, currentNode)

    def learnRDRTree(self, initializedCorpus, goldStandardCorpus):
        self.root = Node(
            "True", 'object.conclusion = "NN"', None, None, None, [], 0
        )

        objects = getObjectDictionary(initializedCorpus, goldStandardCorpus)

        currentNode = self.root
        for initializedTag in objects:
            print(
                "\n===> Building exception rules for tag %s" % initializedTag
            )
            correctCounts = {}
            for object in objects[initializedTag][initializedTag]:
                rules = generateRules(object)
                for rule in rules:
                    correctCounts[rule] = correctCounts.setdefault(rule, 0) + 1

            node = Node(
                'object.tag == "' + initializedTag + '"',
                'object.conclusion = "' + initializedTag + '"',
                self.root,
                None,
                None,
                [],
                1,
            )

            if self.root.exceptChild is None:
                self.root.exceptChild = node
            else:
                currentNode.elseChild = node

            currentNode = node
            objectSet = objects[initializedTag]

            elseChild = False
            currentNode1 = currentNode
            while True:
                rule, correctTag, imp, cornerstoneCases, needToCorrectObjects, errorRaisingObjects = self.findMostEfficientRule(
                    initializedTag, objectSet, correctCounts
                )
                if imp < self.improvedThreshold:
                    break

                node = Node(
                    rule,
                    'object.conclusion = "' + correctTag + '"',
                    currentNode,
                    None,
                    None,
                    cornerstoneCases,
                    2,
                )

                if not elseChild:
                    currentNode1.exceptChild = node
                    elseChild = True
                else:
                    currentNode1.elseChild = node

                currentNode1 = node

                for object in cornerstoneCases:
                    objectSet[correctTag].remove(object)

                for tag in needToCorrectObjects:
                    for object in needToCorrectObjects[tag]:
                        objectSet[tag].remove(object)

                for object in errorRaisingObjects:
                    rules = generateRules(object)
                    for rule in rules:
                        correctCounts[rule] -= 1

                self.buildNodeForObjectSet(needToCorrectObjects, currentNode1)
