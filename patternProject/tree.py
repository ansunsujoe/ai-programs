# A class for the node of the pattern tree
class TreeNode():

    # The constructor
    def __init__(self, parent, value):
        self.value = value
        self.visits = 0
        self.children = {}
        self.parent = parent
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    # The representation
    def __repr__(self):
        if self.parent:
            return (self.depth * "  ") + "<Node {} Popularity {} Visits {}>".format(self.value, round(self.getPopularity(), 2), self.visits)
        else:
            return "<RootNode Children {} Visits {}>".format(list(self.children.keys()), self.visits)
    
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
        del parentNode.children[self.value]

        # Remove all the children from the child
        for cnk in list(self.children.keys()):
            self.children[cnk].prune()

        # Clear the dictionary and itself
        self.children = None
        self = None

# Tree Parameters
class TreeParams():
    def __init__(self):
        self.popularityThreshold = 0

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
    
    def printDiscoveredPatterns(self, params):
        print(printPatternsRecursive(self.root, [], 1))

    def prune(self, params):
        pruneTreeRecursively(self.root, 1, params)


    
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
        newNode = TreeNode(treePos, array[0])
        newNode.visits = 0
        treePos.children[array[0]] = newNode

        # Add child node of the new node
        if len(array) >= 2:
            newNode.children[array[1]] = TreeNode(newNode, array[1])
            newNode.children[array[1]].visits = 0

# Print the nodes in the tree in a hierarchy
def printNodes(root):
    currentString = str(root) + "\n"
    for cnk in list(root.children.keys()):
        currentString += printNodes(root.children[cnk])
    return currentString

# Print all the meaningful patterns we can find
def printPatternsRecursive(treeNode, parents, prevPopularity):

    # If there are no children, then return the string with the pattern
    if len(treeNode.children) == 0:

        # If the pattern is too short, don't print it
        if treeNode.depth <= 2:
            return ""
        
        # Else return the pattern we found
        return "Pattern {}, Cum Popularity {}\n".format(parents, prevPopularity * treeNode.getPopularity())

    # We do have children
    else:
        printString = ""

        # Iterate through the children
        for cnk in list(treeNode.children.keys()):
            parents.append(cnk)
            printString += printPatternsRecursive(treeNode.children[cnk], parents, prevPopularity * treeNode.getPopularity())
            parents.pop()
        return printString

# Prune the tree
def pruneTreeRecursively(treeNode, prevPopularity, params):
    # If there are no children
    if len(treeNode.children) == 0:

        # If the pattern is too short, then prune
        if treeNode.depth <= 2:
            treeNode.prune()
    
    # We do have children
    else:
        # Iterate through the children
        for cnk in list(treeNode.children.keys()):
            if prevPopularity * treeNode.children[cnk].getPopularity() <= params.popularityThreshold:
                treeNode.children[cnk].prune()
            else:
                pruneTreeRecursively(treeNode.children[cnk], prevPopularity * treeNode.getPopularity(), params)


if __name__ == "__main__":
    # Create the root and the tree
    root = TreeNode(None, None)
    patternTree = PatternTree(root)
    params = TreeParams()

    # Insert an array in the pattern tree
    patternTree.insertPattern([2,1,2,4,2,2,3,1,2,4,2,2,1,3,4,2,4,1,3,2,1,2,3,2,2,1,2,2,2,1,2])
    patternTree.prune(params)
    patternTree.printDiscoveredPatterns(params)
    print()
    print(patternTree)
