import json


class TaxonomyTree:
    def __init__(self):
        self.RootNode = TaxonomyTreeNode("ROOT", None)
        pass

    """Adding a node below root"""

    def AddNode(self, name: str):
        return self.RootNode.AddChildNode(name)

    def GetNodeByName(self, name: str):
        return self.RootNode.GetChildByName(name)

    """RootNode is Level 0. Returns a dictionary, where the keys are the values below level x and the values are their according parents on level x"""

    def GetGeneralizedDict_NodeNameToDepthXParentalName(self, depthX):
        if(depthX < 0):
            raise NotImplementedError("Unable to perform negative level generalization")
        return self.RootNode.__generalizeNodesByNameDict__(depthX, 0)

    def GetPathDict_NodeNamesUntilLeaf(self, node=None):
        if(node is None):
            node = self.RootNode

        pathDict = {}

        path = node.GetNodePath()
        if('/' in path):
            pArr = path.split('/')
            pathDict[pArr[-1]] = pArr[1:]

        if len(node.Children) > 0:
            for c in node.Children:
                childDict = self.GetPathDict_NodeNamesUntilLeaf(c)

                # Merge dictionaries
                pathDict = {**pathDict, **childDict}

        return pathDict

    def PrintTree(self):
        self.RootNode.Print()

    @staticmethod
    def CreateFromJSON(jsonData, nameAttribute, childrenAttribute):
        nodeTree = json.loads(jsonData)
        tree = TaxonomyTree()

        tree.__jsonImport_CreateChildrenRecursively(tree.RootNode, nodeTree, nameAttribute, childrenAttribute)

        return tree

    def __jsonImport_CreateChildrenRecursively(self, parentNode, nodeTree, nameAttribute, childrenAttribute):
        for node in nodeTree:
            child = parentNode.AddChildNode(node[nameAttribute])
            if(len(node[childrenAttribute]) > 0):
                self.__jsonImport_CreateChildrenRecursively(child, node[childrenAttribute], nameAttribute, childrenAttribute)


class TaxonomyTreeNode:
    def __init__(self, nodeName: str, parent: 'TaxonomyTreeNode'):  # String type required for Py 3.5 as recursive typing isn't supportes yet...really?!
        self.Name = nodeName
        self.Parent = parent
        self.Children = []
        pass

    def AddChildNode(self, name: str):
        node = TaxonomyTreeNode(name, self)
        self.Children.append(node)
        return node

    def GetNodePath(self):
        if self.Parent is not None:
            return self.Parent.GetNodePath() + '/' + self.Name
        else:
            return self.Name

    def GetChildByName(self, name: str):
        if len(self.Children) > 0:
            for c in self.Children:
                if c.Name == name:
                    return c
                else:
                    r = c.GetChildByName(name)
                    if r is not None:
                        return r
        return None

    def __generalizeNodesByNameDict__(self, depthX, currentDepth):
        genDict = {}

        # Dive deeper until we reach the level to generalize
        if currentDepth < depthX:
            if len(self.Children) > 0:
                for c in self.Children:
                    childDict = c.__generalizeNodesByNameDict__(depthX, currentDepth + 1)

                    # Merge dictionaries
                    genDict = {**genDict, **childDict}

        # Generalization level reached
        elif depthX == currentDepth:
            nodesBelow = self.__getNodesBelowDepthX__(depthX, currentDepth + 1)

            for n in nodesBelow:
                genDict[n.Name] = self.Name

        return genDict

    def __getNodesBelowDepthX__(self, depthX, currentDepth):
        nodes = []

        # Go deeper
        if len(self.Children) > 0:
            for c in self.Children:
                childList = c.__getNodesBelowDepthX__(depthX, currentDepth + 1)

                # Merge lists
                nodes = nodes + childList

        # If current node is below the desired level => add to list
        # (currentDepth - 1) as this node actually belongs to its parent
        if (currentDepth - 1) > depthX:
            nodes.append(self)

        return nodes

    def Print(self, indent=0):
        print(str(int(indent/4)) + ' - ', end='')
        print(' ' * indent, end='')
        print(self.Name)

        if len(self.Children) > 0:
            for c in self.Children:
                c.Print(indent + 4)


# {
#   'Node1LevelX+1_Name': NodeLevelX_Name,
#   'Node2LevelX+1_Name': NodeLevelX_Name,
#   'NodeLevelX+2_Name': NodeLevelX_Name,
#   'NodeLevelX+3_Name': NodeLevelX_Name
# }
