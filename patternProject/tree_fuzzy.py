import matplotlib.pyplot as plt
import json
import os
import ast
import random

# A class for the node of the pattern tree
class TreeNode():

    # The constructor
    def __init__(self, parent, value, tolerance):
        self.value = value
        self.tolerance = tolerance
        self.visits = 0
        self.children = []
        self.references = set()
        self.parent = parent
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    # The representation
    def __repr__(self):
        if self.parent:
            return (self.depth * "  ") + "<Node {} Tolerance {} Visits {} NumChildren {} References {}>".format(self.value, round(self.tolerance, 2), self.visits, len(self.children), list(self.references))
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
        self.tolGranularity = 0.05       # Add to the tolerance when we get a rejection
        self.tolDecrease = 2            # Divide tolerance when we find a match
        self.tolThreshold = 1           # At what point do we just get rid of the node

class Pattern():

    # Constructor
    def __init__(self, sequence, avgTolerance, weight, references):
        self.sequence = sequence.copy()
        self.avgTolerance = avgTolerance
        self.weight = weight
        self.references = list(references).copy()
    
    # Representation
    def __repr__(self):
        return "Pattern {}, Avg Tolerance {}, Weight {}, References {}".format([round(x, 2) for x in self.sequence], self.avgTolerance, self.weight, self.references)

    # Plot a sample of a pattern
    def plot(self):
        plotArray = [100]

        # PlotArray is the y-axis and we have a simple x-axis
        for i in range(len(self.sequence)):
            plotArray.append(((self.sequence[i] + 100) / 100) * plotArray[i])
        xaxis = range(1, len(plotArray) + 1)

        # Use a line plot
        plt.plot(xaxis, plotArray)
        plt.show()


# Pattern Tree
class PatternTree():

    # The constructor
    def __init__(self, root):
        self.root = root
    
    def __repr__(self):
        return printNodes(self.root)

    # Insert an array in the tree, starting at root
    def insertArray(self, array, refName, params):
        insertArrayRecursive(self.root, array, refName, 0, params)
        if array == []:
            return
    
    def insertPattern(self, pattern, refName, params):
        for i in range(len(pattern)):
            insertArrayRecursive(self.root, pattern, refName, i, params)
    
    def printDiscoveredPatterns(self):
        print(printPatternsRecursive(self.root, [], 1))

    def downloadDiscoveredPatterns(self):
        return downloadPatternsRecursive(self.root, [], 0)

    def prune(self, params):
        pruneTreeRecursively(self.root, params)

# A simple class to store stock data from Ameritrade API
class StockData():

    # The constructor
    def __init__(self):
        self.values = []
        self.jumpValues = []
    
    # Add information to both arrays from Ameritrade file
    def addFromAmeritradeFile(self, filename):

        # Read the file
        fd = open(filename, "r")
        data = ast.literal_eval(fd.read())

        # Parse out the prices themselves
        for i in range(len(data["candles"])):
            self.values.append(data["candles"][i]["close"])

        # Calculate stock price changes as percentages
        for i in range(len(self.values) - 1):
            self.jumpValues.append((self.values[i + 1] - self.values[i]) * 100 / self.values[i])
    
# Other helper methods
def insertArrayRecursive(treePos, array, refName, startPos, params):
    if startPos == len(array):
        return

    # Increase the visits by 1
    treePos.visits += 1

    # Try to find a child that matches the criterion
    found = False
    for child in treePos.children:

        # If we get a tolerance match
        if not found and isTolerant("stock", child.value, array[startPos], child.tolerance):
            found = True
            insertArrayRecursive(child, array, refName, startPos + 1, params)

            # Update the tolerance and the actual value itself (centroid)
            child.tolerance /= params.tolDecrease
            if child.visits >= 1:
                child.value = (child.visits * child.value + array[startPos]) / (child.visits + 1)
            
            # Create a reference to the actual data
            if child.depth >= 3:
                child.references.add((refName, startPos - child.depth + 1))

        elif isTolerant("stock", child.value, array[startPos], child.tolerance):
            child.prune()
        
        else:
            # Increase the tolerance since we did not get a match yet
            child.tolerance += params.tolGranularity

            # If the tolerance is higher than the threshold, restart it to 0
            if child.tolerance > params.tolThreshold:
                child.tolerance = 0

    if not found:
        # Add new node if it does not exist in the children dict
        newNode = TreeNode(treePos, array[startPos], 0)
        newNode.visits = 0
        treePos.children.append(newNode)

        # Add child node of the new node
        if startPos + 1 < len(array):
            newSecondNode = TreeNode(newNode, array[startPos + 1], 0)
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

# Print all the meaningful patterns we can find
def downloadPatternsRecursive(treeNode, parents, avgTolerance):

    # If there are no children, then return the string with the pattern
    if len(treeNode.children) == 0:

        # If the pattern is too short, don't print it
        if treeNode.depth <= 2:
            return []
        
        # Else return the pattern we found
        newAvgTolerance = ((treeNode.depth - 1) * avgTolerance + treeNode.tolerance) / treeNode.depth
        return [Pattern(parents, newAvgTolerance, treeNode.visits, treeNode.references)]

    # We do have children
    else:
        patternArray = []

        # Iterate through the children
        for child in treeNode.children:
            parents.append(child.value)

            # Set the new avg tolerance for the pattern
            if treeNode.depth > 0:
                newAvgTolerance = ((treeNode.depth - 1) * avgTolerance + treeNode.tolerance) / treeNode.depth
            else:
                newAvgTolerance = 0

            # Recursive call to child
            patternArray += downloadPatternsRecursive(child, parents, newAvgTolerance)
            parents.pop()
        
        return patternArray

# Prune the tree
def pruneTreeRecursively(treeNode, params):
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
                if pruneTreeRecursively(treeNode.children[i], params) == 1:
                    treeNode.children.pop(i)
                    i -= 1
            i += 1
        return 0

def isTolerant(domain, nodeValue, dataValue, tolerance):
    # If we meet the normal definition for tolerance, we may have other
    # constraints depending on the domain
    if dataValue >= nodeValue - tolerance and dataValue <= nodeValue + tolerance:

        # If the domain is for stock prices
        if domain == "stock":

            # We want both node value and data value to be of the same sign
            if (nodeValue < 0 and dataValue < 0) or (nodeValue > 0 and dataValue > 0):
                return True
            else:
                return False
    else:
        return False

# Create a dictionary that serves as a stock ticker data source
def createStockQuotesDict(dirName):
    # Create a new dictionary
    stockDataDict = {}

    # Iterate through each filename
    for filename in os.listdir(dirName):
        try:
            tickerName = filename.split(".")[0]
            newStock = StockData()
            newStock.addFromAmeritradeFile(os.path.join(dirName, filename))
            stockDataDict[tickerName] = newStock
        except:
            print("Something went wrong")

    # Return the dictionary        
    return stockDataDict

# Visualize a random pattern from a list
def visualizeRandomPattern(patternList, dataDict):

    # Select the random pattern
    index = random.randint(0, len(patternList))
    pattern = patternList[index]

    # Information about the pattern itself that is needed
    refArray = pattern.references
    patternLen = len(pattern.sequence)
    
    # Plotting similar pattern instances - 4 is max in this case (we should interpret references)
    fig, axs = plt.subplots(2, 2)
    for i in range(4):
        xaxis = range(1, 1 + patternLen + 2)
        yaxis = dataDict[refArray[i][0]].values[refArray[i][1]: refArray[i][1] + patternLen + 2]
        # Use a line plot
        axs[i // 2, i % 2].plot(xaxis, yaxis)
    plt.show()

# Main method
if __name__ == "__main__":

    # Initialize variables for the tree, params, and pattern storage
    root = TreeNode(None, None, 0)
    patternTree = PatternTree(root)
    params = TreeParams()

    # Dictionary with stock database
    tickerDict = createStockQuotesDict("data/stock-data")

    epochs = 10
    for epoch in range(epochs):

        # Iterate through the datasets in the dictionary
        for ticker in tickerDict.keys():
            # Insert the data into the pattern tree
            patternTree.insertPattern(tickerDict[ticker].jumpValues, ticker, params)

        # Insert an array in the pattern tree and then prune the tree
        patternTree.prune(params)

        patterns = patternTree.downloadDiscoveredPatterns()
        print("Epoch " + str(epoch + 1) + " (" + str(len(patterns)) + " patterns found)")

    patterns = patternTree.downloadDiscoveredPatterns()
    for x in patterns:
        print(x)

        # if epoch == 9:
            
            # # Plotting similar patterns
            # refArray = patterns[0].references
            # patternLen = len(patterns[0].sequence)
            # print(patternTree)
            
            # # Plotting similar patterns
            # fig, axs = plt.subplots(2, 2)
            # for i in range(len(refArray)):
            #     xaxis = range(refArray[i], refArray[i] + patternLen + 2)
            #     yaxis = stockPrices[refArray[i]: refArray[i] + patternLen + 2]
            #     # Use a line plot
            #     axs[i // 2, i % 2].plot(xaxis, yaxis)
            #     axs[1, 1].plot(range(100, 145), stockPrices[100:145])
            # plt.show()