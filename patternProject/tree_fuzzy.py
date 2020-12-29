import matplotlib.pyplot as plt
import json

# A class for the node of the pattern tree
class TreeNode():

    # The constructor
    def __init__(self, parent, value, tolerance):
        self.value = value
        self.tolerance = tolerance
        self.visits = 0
        self.children = []
        self.parent = parent
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    # The representation
    def __repr__(self):
        if self.parent:
            return (self.depth * "  ") + "<Node {} Tolerance {} Visits {} NumChildren {}>".format(self.value, round(self.tolerance, 2), self.visits, len(self.children))
        else:
            return "<RootNode Visits {}>".format(self.visits)
    
    # Get the relative popularity of a node compared to its peers
    def getPopularity(self):
        if self.parent:
            if self.parent.visits > 0:
                return self.visits / self.parent.visits
            else:
                return 0
        else:
            return 1
    
    # Prune a node and its children
    def prune(self):

        # Remove the reference from the parent
        parentNode = self.parent

        # Remove all the children from the child
        for child in self.children:
            child.prune()

        # Clear the dictionary and itself
        self.children = []
        self = None

        # Return a status code
        return 1

# Tree Parameters
class TreeParams():
    def __init__(self):
        self.popularityThreshold = 0    # What popularity for a pattern is unacceptable
        self.tolGranularity = 0.1       # Add to the tolerance when we get a rejection
        self.tolDecrease = 2            # Divide tolerance when we find a match
        self.tolThreshold = 2           # At what point do we just get rid of the node

class Pattern():
    def __init__(self, sequence, cumPopularity):
        self.sequence = sequence
        self.cumPopularity = popularity
    
    def __repr__(self):
        return "Pattern {}, Cum Popularity {}\n".format([round(x, 2) for x in sequence], cumPopularity)

    def plot(self):
        plotArray = [10]
        for i in range(len(self.sequence)):
            plotArray.append(((self.sequence[i] + 100) / 100) * plotArray[i])
        print(plotArray)

# Pattern Tree
class PatternTree():

    # The constructor
    def __init__(self, root):
        self.root = root
    
    def __repr__(self):
        return printNodes(self.root)

    # Insert an array in the tree, starting at root
    def insertArray(self, array, params):
        insertArrayRecursive(self.root, array, params)
        if array == []:
            return
    
    def insertPattern(self, pattern, params):
        for i in range(len(pattern)):
            insertArrayRecursive(self.root, pattern[i:], params)
    
    def printDiscoveredPatterns(self, params):
        print(printPatternsRecursive(self.root, [], 1))

    def prune(self, params):
        pruneTreeRecursively(self.root, 1, params)


    
# Other helper methods
def insertArrayRecursive(treePos, array, params):
    if len(array) == 0:
        return

    # Increase the visits by 1
    treePos.visits += 1

    # Try to find a child that matches the criterion
    found = False
    for child in treePos.children:

        # If we get a tolerance match
        if not found and array[0] >= child.value - child.tolerance and array[0] <= child.value + child.tolerance:
            found = True
            insertArrayRecursive(child, array[1:], params)

            # Update the tolerance and the actual value itself (centroid)
            child.tolerance /= params.tolDecrease
            if child.visits >= 1:
                child.value = (child.visits * child.value + array[0]) / (child.visits + 1)
        
        # Increase the tolerance since we did not get a match yet
        child.tolerance += params.tolGranularity

    if not found:
        # Add new node if it does not exist in the children dict
        newNode = TreeNode(treePos, array[0], 0)
        newNode.visits = 0
        treePos.children.append(newNode)

        # Add child node of the new node
        if len(array) >= 2:
            newSecondNode = TreeNode(newNode, array[1], 0)
            newNode.children.append(newSecondNode)
            newSecondNode.visits = 0

# Print the nodes in the tree in a hierarchy
def printNodes(root):
    currentString = str(root) + "\n"
    for child in root.children:
        currentString += printNodes(child)
    return currentString

# Print all the meaningful patterns we can find
def printPatternsRecursive(treeNode, parents, prevPopularity):

    # If there are no children, then return the string with the pattern
    if len(treeNode.children) == 0:

        # If the pattern is too short, don't print it
        if treeNode.depth <= 2:
            return ""
        
        # Else return the pattern we found
        return "Pattern {}, Cum Popularity {}\n".format([round(x, 2) for x in parents], prevPopularity * treeNode.getPopularity())

    # We do have children
    else:
        printString = ""

        # Iterate through the children
        for child in treeNode.children:
            parents.append(child.value)
            printString += printPatternsRecursive(child, parents, prevPopularity * treeNode.getPopularity())
            parents.pop()
        return printString

# # Print all the meaningful patterns we can find
# def printPatternsRecursive(treeNode, parents, prevPopularity):

#     # If there are no children, then return the string with the pattern
#     if len(treeNode.children) == 0:

#         # If the pattern is too short, don't print it
#         if treeNode.depth <= 2:
#             return ""
        
#         # Else return the pattern we found
#         return "Pattern {}, Cum Popularity {}\n".format([round(x, 2) for x in parents], prevPopularity * treeNode.getPopularity())

#     # We do have children
#     else:
#         printString = ""

#         # Iterate through the children
#         for child in treeNode.children:
#             parents.append(child.value)
#             printString += printPatternsRecursive(child, parents, prevPopularity * treeNode.getPopularity())
#             parents.pop()
#         return printString

# Prune the tree
def pruneTreeRecursively(treeNode, prevPopularity, params):
    # If there are no children
    if len(treeNode.children) == 0:

        # If the pattern is too short, then prune
        if treeNode.depth <= 2:
            return treeNode.prune()
    
    # We do have children
    else:
        # Iterate through the children
        i = 0
        while i < len(treeNode.children):
            if treeNode.children[i].visits == 0:
                treeNode.children[i].prune()
                treeNode.children.pop(i)
                i -= 1
            else:
                if pruneTreeRecursively(treeNode.children[i], prevPopularity * treeNode.getPopularity(), params) == 1:
                    treeNode.children.pop(i)
                    i -= 1
            i += 1
        return 0

# Main method
if __name__ == "__main__":

    # Create the root and the tree
    root = TreeNode(None, None, None)
    patternTree = PatternTree(root)
    params = TreeParams()

    # Read stock data
    stockDataStream = open("data/stock-data/aapl-1year-daily-12-28-20.txt", "r")
    stockData = json.loads(stockDataStream.read())
    stockPrices = []
    for i in range(len(stockData["candles"])):
        stockPrices.append(stockData["candles"][i]["close"])
    
    # Calculate stock price changes as percentages
    stockPercentChanges = []
    for i in range(len(stockPrices) - 1):
        stockPercentChanges.append((stockPrices[i + 1] - stockPrices[i]) * 100 / stockPrices[i])

    # print(stockPercentChanges)
    sampleStockData = stockPercentChanges

    epochs = 10
    for epoch in range(epochs):

        # Insert an array in the pattern tree
        print("Epoch " + str(epoch + 1) + ":")
        patternTree.insertPattern(sampleStockData, params)
        patternTree.prune(params)
        patternTree.printDiscoveredPatterns(params)
        print(patternTree)
        print()