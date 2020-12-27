# A class for the node of the pattern tree
class TreeNode():

    # The constructor
    def __init__(self, parent):
        self.visits = 0
        self.children = {}
        self.parent = parent
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    # The representation
    def __repr__(self):
        if self.parent:
            return (self.depth * "  ") + "<Node Popularity {} Children {}>".format(round(self.visits / self.parent.visits, 2), list(self.children.keys()))
        else:
            return "<RootNode Children {}>".format(list(self.children.keys()))
    
    # Get the relative popularity of a node compared to its peers
    def getPopularity(self):
        if self.parent:
            return self.visits / self.parent.visits
        else:
            return 1

# Pattern Tree
class PatternTree():

    # The constructor
    def __init__(self, root):
        self.root = root
    
    def __repr__(self):
        return printNodes(self.root)

    # Insert an array in the tree, starting at root
    def insertArray(self, array):
        insertArrayRecursive(self.root, array)
        if array == []:
            return
    
    def insertPattern(self, pattern):
        for i in range(len(pattern)):
            insertArrayRecursive(self.root, pattern[i:])
    
    def printDiscoveredPatterns(self):
        parents = []
        print(printPatternsRecursive(self.root, parents, 1))

    
# Other helper methods
def insertArrayRecursive(treePos, array):
    if len(array) == 0:
        return
    try:
        # Increase the visits by 1
        treePos.visits += 1

        # Access the next child
        nextNode = treePos.children[array[0]]
        insertArrayRecursive(nextNode, array[1:])

    except KeyError:
        # Add new node if it does not exist in the children dict
        newNode = TreeNode(treePos)
        newNode.visits = 1
        treePos.children[array[0]] = newNode

        # Add child node of the new node
        if len(array) >= 2:
            newNode.children[array[1]] = TreeNode(newNode)
            newNode.children[array[1]].visits = 1

def printNodes(root):
    currentString = str(root) + "\n"
    for cnk in list(root.children.keys()):
        currentString += printNodes(root.children[cnk])
    return currentString

def printPatternsRecursive(treeNode, parents, prevProbability):
    # If there are no children, then return the string with the pattern
    if len(list(treeNode.children.keys())) == 0:
        return "Pattern {}, Probability {}\n".format(parents, prevProbability * treeNode.getPopularity())
    else:
        printString = ""
        for cnk in list(treeNode.children.keys()):
            if parents is None:
                printString += printPatternsRecursive(treeNode.children[cnk], [cnk], prevProbability * treeNode.getPopularity())
            else:
                newList = parents.append(cnk)
                printString += printPatternsRecursive(treeNode.children[cnk], newList, prevProbability * treeNode.getPopularity())
        return printString


if __name__ == "__main__":
    # Create the root and the tree
    root = TreeNode(None)
    patternTree = PatternTree(root)

    # Insert an array in the pattern tree
    patternTree.insertPattern([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(patternTree)
    print()
    print()
    patternTree.printDiscoveredPatterns()
