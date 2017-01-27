"""
This program defines the classes for
line segments in a 2D geometric space

Author: Ajinkya Dhaigude (ad8454@rit.edu)
"""

class Point:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.seen = False


class Segment:
    def __init__(self, name, p, q):
        self.name = name
        self.leftPoint = p
        self.rightPoint = q
        if q.x < p.x:
            self.leftPoint = q
            self.rightPoint = p

        self.slope = (self.rightPoint.y - self.leftPoint.y) / (self.rightPoint.x - self.leftPoint.x)
        self.const = self.leftPoint.y - (self.slope * self.leftPoint.x)

    def isPointAbove(self, point):
        if point.y > (self.slope * point.x) + self.const:
            return True
        return False

    def getY(self, x):
        if self.leftPoint.x <= x <= self.rightPoint.x:
            return (self.slope * x) + self.const
        return None