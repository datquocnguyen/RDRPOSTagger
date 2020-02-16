# -*- coding: utf-8 -*-

from .Node import Node 
from .Object import FWObject 

class SCRDRTree:
    """
    Single Classification Ripple Down Rules tree for Part-of-Speech and morphological tagging
    """
    
    def __init__(self, root = None):
        self.root = root
                            
    def findDepthNode(self, node, depth):
        while node.depth != depth:
            node = node.father
        return node                
                
    def classify(self, object):
        self.root.check(object)
        
    def writeToFileWithSeenCases(self, outFile):
        out = open(outFile, "w")
        self.root.writeToFileWithSeenCases(out, 0)
        out.close()
    
    def writeToFile(self, outFile):
        out = open(outFile, "w")
        self.root.writeToFile(out, 0)
        out.close()
    
    #Build tree from file containing rules using FWObject
    def constructSCRDRtreeFromRDRfile(self, rulesFilePath, encoding='utf-8'):
        
        self.root = Node(FWObject(False), "NN", None, None, None, [], 0)
        currentNode = self.root
        currentDepth = 0
        
        rulesFile = open(rulesFilePath, "r", encoding=encoding)
        lines = rulesFile.readlines()
        
        for i in range(1, len(lines)):
            line = lines[i]
            depth = 0           
            for c in line:
                if c == '\t':
                    depth = depth + 1
                else:
                    break

            line = line.strip()
            if len(line) == 0:
                continue
                
            temp = line.find("cc")
            if temp == 0:   
                continue
            
            condition = getCondition(line.split(" : ", 1)[0].strip())
            conclusion = getConcreteValue(line.split(" : ", 1)[1].strip())
            
            node = Node(condition, conclusion, None, None, None, [], depth)
            
            if depth > currentDepth:
                currentNode.exceptChild = node
            elif depth == currentDepth:
                currentNode.elseChild = node
            else:
                while currentNode.depth != depth:
                    currentNode = currentNode.father
                currentNode.elseChild = node
            
            node.father = currentNode
            currentNode = node
            currentDepth = depth
    
    def findFiredNode(self, fwObject):
        currentNode = self.root
        firedNode = None
        obContext = fwObject.context
        while True:
            #Check whether object satisfying the current node's condition
            cnContext = currentNode.condition.context
            notNoneIds = currentNode.condition.notNoneIds
            satisfied = True
            for i in notNoneIds:
                if cnContext[i] != obContext[i]:
                    satisfied = False
                    break
                    
            if(satisfied):
                firedNode = currentNode
                exChild = currentNode.exceptChild
                if exChild is None:
                    break
                else:
                    currentNode = exChild
            else:
                elChild = currentNode.elseChild
                if elChild is None:
                    break
                else:
                    currentNode = elChild
        return firedNode
    
#    def findFiredNodeInDepth(self, fwObject, depth):
#        currentNode = self.root
#        firedNode = None
#        while True:
#            if(currentNode.condition.isSatisfied(fwObject)):
#                firedNode = currentNode
#                if currentNode.exceptChild is None:
#                    break
#                else:
#                    currentNode = currentNode.exceptChild
#            else:
#                if currentNode.elseChild is None:
#                    break
#                else:
#                    currentNode = currentNode.elseChild
#            if currentNode.depth > depth:
#                break
#        return firedNode
#    
#    #Count number of nodes in exception-structure levels
#    def countNodes(self, inDepth):
#        currentNode = self.root
#        nodeQueue = []
#        nodeQueue.append(currentNode)
#        count = 0
#        while len(nodeQueue) > 0:
#            currentNode = nodeQueue[0]
#            #Current node's depth is smaller than a given threshold
#            if currentNode.depth <= inDepth:
#                count += 1                    
#            if currentNode.exceptChild is not None:
#                nodeQueue.append(currentNode.exceptChild)
#            if currentNode.elseChild is not None:
#                nodeQueue.append(currentNode.elseChild)
#            nodeQueue = nodeQueue[1:] 
#        return count
                
def getConcreteValue(str):
    if str.find('""') > 0:
        if str.find("Word") > 0:
            return "<W>"
        elif str.find("suffixL") > 0:
            return "<SFX>"
        else:
            return "<T>"
    return str[str.find("\"") + 1 : len(str) - 1]
       
def getCondition(strCondition):
    condition = FWObject(False)
    for rule in strCondition.split(" and "):
        rule = rule.strip()
        key = rule[rule.find(".") + 1 : rule.find(" ")]
        value = getConcreteValue(rule)
             
        if key == "prevWord2": 
            condition.context[0] = value
        elif key == "prevTag2":
            condition.context[1] = value
        elif key == "prevWord1":
            condition.context[2] = value
        elif key == "prevTag1":
            condition.context[3] = value
        elif key == "word":
            condition.context[4] = value
        elif key == "tag":
            condition.context[5] = value
        elif key == "nextWord1":
            condition.context[6] = value
        elif key == "nextTag1":
            condition.context[7] = value
        elif key == "nextWord2":
            condition.context[8] = value
        elif key == "nextTag2":
            condition.context[9] = value
        elif key == "suffixL2":
            condition.context[10] = value
        elif key == "suffixL3":
            condition.context[11] = value
        elif key == "suffixL4":
            condition.context[12] = value
    for i in range(13):
        if condition.context[i] is not None:
            condition.notNoneIds.append(i)        
    return condition
    
if __name__ == "__main__":
    pass
