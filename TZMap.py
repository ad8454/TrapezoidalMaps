"""
This program defines a class that stores the trapezoidal map.
It also provides related helper functions.

Author: Ajinkya Dhaigude (ad8454@rit.edu)
"""
class TZMap:

    def __init__(self, root):
        self.root = root
        self.adjMatrix = None
        self.allPNames = []
        self.allQNames = []
        self.totSegments = 0
        self.totTrapezoids = 0

    def updateRoot(self, root):
        self.root = root

    def assignTrapezpoidNames(self, idNum=0, node=None):
        """
        Recursive function that assigns a unique name to
        each trapezoid. This function should be called
        after the whole map is built as the trapezoids are
        constantly modified and deleted during the building
        process.
        :param idNum: sequential number part of the name
        :param node: current node under consideration
        :return: last assigned number
        """
        if node is None:
            node = self.root

        if node.isLeaf and node.name is None:
                idNum += 1
                node.name = 'T'+str(idNum)

        elif node.type == 'xnode':
            idNum = self.assignTrapezpoidNames(idNum, node.left)
            idNum = self.assignTrapezpoidNames(idNum, node.right)

        elif node.type == 'ynode':
            idNum = self.assignTrapezpoidNames(idNum, node.above)
            idNum = self.assignTrapezpoidNames(idNum, node.below)

        return idNum

    def printTraversalPath(self, userPoint, node=None):
        """
        Print to console the traversal path of the given
        point in the map.
        :param userPoint: destination point
        :param node: current node on the path to destination
        :return: None
        """
        if node is None:
            node = self.root
            print 'Traversal Path:',
        else:
            print '->',

        print node.getName(),

        if node.type == 'xnode':
            if userPoint.x >= node.endPoint.x:
                self.printTraversalPath(userPoint, node.right)
            else:
                self.printTraversalPath(userPoint, node.left)
        elif node.type == 'ynode':
            if node.lineSegment.isPointAbove(userPoint):
                self.printTraversalPath(userPoint, node.above)
            else:
                self.printTraversalPath(userPoint, node.below)

    def createAdjMatrix(self, uniquePoints, numSegments, numTrapezoids):
        """
        Convert trapezoidal map to an adjacency matrix and write the
        output to a file.
        :param uniquePoints: list of unique points in the map
        :param numSegments: total number of segments in the map
        :param numTrapezoids: total number of trapezoids in the map
        :return: None
        """
        for point in uniquePoints:
            if point.name[0] == 'P':
                self.allPNames.append(int(point.name[1:]))
            else:
                self.allQNames.append(int(point.name[1:]))
        self.totSegments = numSegments
        self.totTrapezoids = numTrapezoids
        n = len(uniquePoints) + numSegments + numTrapezoids + 2
        self.adjMatrix = [[0]*n for i in range(n)]

        self.headerForAdjMatrix(0, '   ')
        self.headerForAdjMatrix(len(self.adjMatrix) - 1, 'Sum')
        self.fillAdjMatrix()

        adjFileName = "adjMatrixOutput.txt"
        outFile = open(adjFileName, "w")
        for arr in self.adjMatrix:
            for col, elem in enumerate(arr):
                elem = str(elem)
                if len(elem) == 1:
                    elem = ' ' + elem + ' '
                if len(elem) == 2:
                    elem = ' ' + elem

                outFile.write(elem + ' ')

            outFile.write('\n')
        outFile.close

        print 'Adjacency matrix saved in file:', adjFileName

    def fillAdjMatrix(self, node=None):
        """
        Recursive function that traverses the map to fill in
        appropriate vales in the adjacency matrix.
        :param node: current node under consideration
        :return: None
        """
        if node is None:
            node = self.root

        col = self.getIdx(node)
        if node.type == 'xnode':
            self.addToAdjMatrix(self.getIdx(node.left), col)
            self.fillAdjMatrix(node.left)
            self.addToAdjMatrix(self.getIdx(node.right), col)
            self.fillAdjMatrix(node.right)

        if node.type == 'ynode':
            self.addToAdjMatrix(self.getIdx(node.above), col)
            self.fillAdjMatrix(node.above)
            self.addToAdjMatrix(self.getIdx(node.below), col)
            self.fillAdjMatrix(node.below)

    def getIdx(self, node):
        """
        Get corresponding index in the matrix of a node
        from its name.
        :param node: node to be indexed
        :return: index of node
        """
        name = node.getName()
        if len(name) == 2:
            name += ' '
        idx = int(name[1:])

        if name[0] == 'P':
            idx = self.allPNames.index(idx) + 1
            self.headerForAdjMatrix(idx, name)
            return idx

        if name[0] == 'Q':
            idx = self.allQNames.index(idx) + 1
            idx += len(self.allPNames)
            self.headerForAdjMatrix(idx, name)
            return idx

        if name[0] == 'S':
            idx += len(self.allPNames) + len(self.allQNames)
            self.headerForAdjMatrix(idx, name)
            return idx

        if name[0] == 'T':
            idx += len(self.allPNames) + len(self.allQNames) + self.totSegments
            self.headerForAdjMatrix(idx, name)
            return idx

    def addToAdjMatrix(self, row, col):
        if self.adjMatrix[row][col] == 0:
            self.adjMatrix[row][col] = 1
            self.adjMatrix[row][-1] += 1
            self.adjMatrix[-1][col] += 1

    def headerForAdjMatrix(self, idx, name):
        self.adjMatrix[0][idx] = name
        self.adjMatrix[idx][0] = name


