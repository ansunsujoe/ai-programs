# A class for the node of the pattern tree
class TreeNode():

    # The constructor
    def __init__(self):
        self.lastVisited = 0
        self.visited = 0
        self.children = {}

# Pattern Tree  
class PatternTree():

    # The constructor
    def __init__(self):
        # A list of nodes linked to each other
        self.nodeList = []

    # Insert an array in the tree, starting at root
    def insertArray(self, array, nodeList):
        insertArrayRecursive(self.root, array)
        if array == []:
            return
    
# Other helper methods
def insertArrayRecursive(treePos, array, nodeList):
    if len(array) == 0:
        return
    try:
        nextNodeIndex = treePos.children[array[0]]
    except KeyError:
        newNode = TreeNode()
        