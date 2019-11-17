# -*- coding: utf-8 -*-


class Node:
    """
    A class to represent the nodes in SCRDR tree
    """

    def __init__(
        self,
        condition,
        conclusion,
        father=None,
        exceptChild=None,
        elseChild=None,
        cornerstoneCases=[],
        depth=0,
    ):
        self.condition = condition
        self.conclusion = conclusion
        self.exceptChild = exceptChild
        self.elseChild = elseChild
        self.cornerstoneCases = cornerstoneCases
        self.father = father
        self.depth = depth

    def satisfied(self, object):
        return eval(self.condition)

    def executeConclusion(self, object):
        exec(self.conclusion)

    def appendCornerstoneCase(self, object):
        self.cornerstoneCases.append(object)

    def check(self, object):
        if self.satisfied(object):
            self.executeConclusion(object)
            if self.exceptChild:
                self.exceptChild.check(object)
        else:
            if self.elseChild:
                self.elseChild.check(object)

    def checkDepth(self, object, length):
        if self.depth <= length:
            if self.satisfied(object):
                self.executeConclusion(object)
                if self.exceptChild:
                    self.exceptChild.checkDepth(object, length)
            else:
                if self.elseChild:
                    self.elseChild.checkDepth(object, length)

    def findRealFather(self):
        node = self
        fatherNode = node.father
        while True and fatherNode:
            if fatherNode.exceptChild == node:
                break
            node = fatherNode
            fatherNode = node.father
        return fatherNode

    def addElseChild(self, node):
        fatherNode = self.findRealFather()
        for object in fatherNode.cornerstoneCases:
            if node.satisfied(object):
                print(
                    "The new rule fires the cornerstone cases of its father node!!!"
                )
                self.findRealFather().cornerstoneCases.remove(object)
        self.elseChild = node
        return True

    def addExceptChild(self, node):
        for object in self.cornerstoneCases:
            if node.satisfied(object):
                print(
                    "The new rule fires the cornerstone cases of its father node!!!"
                )
                self.cornerstoneCases.remove(object)
        self.exceptChild = node
        return True

    def writeToFileWithSeenCases(self, out, depth):
        space = tabStr(depth)
        out.write(space + self.condition + " : " + self.conclusion + "\n")
        for case in self.cornerstoneCases:
            out.write(" " + space + "cc: " + case.toStr() + "\n")
        if self.exceptChild:
            self.exceptChild.writeToFile(out, depth + 1)
        if self.elseChild:
            self.elseChild.writeToFile(out, depth)

    def writeToFile(self, out, depth):
        space = tabStr(depth)
        out.write(space + self.condition + " : " + self.conclusion + "\n")
        if self.exceptChild:
            self.exceptChild.writeToFile(out, depth + 1)
        if self.elseChild:
            self.elseChild.writeToFile(out, depth)


def tabStr(length):
    return "".join(["\t"] * length)
