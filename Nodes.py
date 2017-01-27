"""
This program defines the classes for each of the
three different kinds of nodes required for a
trapezoidal map

Author: Ajinkya Dhaigude (ad8454@rit.edu)
"""

from SegmentData import Point, Segment

class XNode:
    def __init__(self, point, left=None, right=None):
        self.isLeaf = False
        self.type = 'xnode'
        self.setLeft(left)
        self.setRight(right)
        self.endPoint = point
        self.endPoint.seen = True

    def setLeft(self, node):
        self.left = node
        if node is None:
            return
        if node.isLeaf and self not in node.parents:
            node.parents.append(self)

    def setRight(self, node):
        self.right = node
        if node is None:
            return
        if node.isLeaf and self not in node.parents:
            node.parents.append(self)

    def getName(self):
        return self.endPoint.name


class YNode:
    def __init__(self, segment, above=None, below=None):
        self.isLeaf = False
        self.type = 'ynode'
        self.setAbove(above)
        self.setBelow(below)
        self.lineSegment = segment

    def setAbove(self, node):
        self.above = node
        if node is None:
            return
        if node.isLeaf and self not in node.parents:
            node.parents.append(self)

    def setBelow(self, node):
        self.below = node
        if node is None:
            return
        if node.isLeaf and self not in node.parents:
            node.parents.append(self)

    def getName(self):
        return self.lineSegment.name


class TrapezoidNode:
    def __init__(self, topSegment, bottomSegment, leftPoint, rightPoint):
        self.isLeaf = True
        self.type = 'tnode'
        self.topSegment = topSegment
        self.bottomSegment = bottomSegment
        self.leftPoint = leftPoint
        self.rightPoint = rightPoint
        self.parents = []
        self.name = None

    def containsSegment(self, segment):
        if self.containsPoint(segment.leftPoint) or self.containsPoint(segment.rightPoint):
            return True
        resY = segment.getY(self.leftPoint.x)
        if resY is not None:
            leftIntersection = Point(None, self.leftPoint.x, resY)
            if self.containsPoint(leftIntersection):
                return True
        return False

    def containsPoint(self, point):
        if self.leftPoint.x <= point.x <= self.rightPoint.x:
            return self.bottomSegment.isPointAbove(point) and not self.topSegment.isPointAbove(point)
        return False

    def replacePositionWith(self, tzMap, node):
        if not self.parents:
            tzMap.updateRoot(node)
            return
        for parent in self.parents:
            if parent.type == 'xnode':
                if parent.left == self:
                    parent.setLeft(node)
                else:
                    parent.setRight(node)
            else:
                if parent.above == self:
                    parent.setAbove(node)
                else:
                    parent.setBelow(node)

    def getName(self):
        return self.name