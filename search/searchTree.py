class TreeNode:

    # Constructor
    def __init__(self, state, parent = None, action = None, pathCost = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.pathCost = pathCost
        # Calculate the depth of the node
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1
    
    # Create a child node based on an action
    #def createChildNode(self, )