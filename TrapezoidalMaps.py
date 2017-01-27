"""
This is the main program that reads in the input file and
builds the trapezoidal map. It then accepts a user input for
coordinates and calls a method to output the traversal path.

Author: Ajinkya Dhaigude (ad8454@rit.edu)
"""
from Nodes import XNode, YNode, TrapezoidNode
from SegmentData import Point, Segment
from TZMap import TZMap


def main():
    """
    Main function that asks user for the input file name
    and reads in the coordinates. The trapezoidal map is
    then built with these coordinates.
    :return: None
    """
    fileName = raw_input('Enter file name: ')
    boundingBox = None
    lineSegments = []
    idNum = 1
    uniquePoints = []
    with open(fileName) as fn:
        for line in fn:
            if ' ' in line:
                coords = line.rstrip('\n').split(' ')
                x1 = int(coords[0])
                y1 = int(coords[1])
                x2 = int(coords[2])
                y2 = int(coords[3])
                # assign bounds for bounding box initially
                if boundingBox == None:
                    lowerLeft = Point('ll', x1, y1)
                    upperRight = Point('ur', x2, y2)
                    lowerRight = Point('lr', x2, y1)
                    upperLeft = Point('ul', x1, y2)
                    topSegment = Segment('bT', upperLeft, upperRight)
                    bottomSegment = Segment('bB', lowerLeft, lowerRight)
                    boundingBox = TrapezoidNode(topSegment, bottomSegment, upperLeft, upperRight)

                else:
                    point1 = Point('P'+str(idNum), x1, y1)
                    point2 = Point('Q'+str(idNum), x2, y2)
                    isPoint1Unique = True
                    isPoint2Unique = True
                    # store point only if it is unique
                    for point in uniquePoints:
                        if point.x == point1.x and point.y == point1.y:
                            point1 = point
                            isPoint1Unique = False
                        if point.x == point2.x and point.y == point2.y:
                            point2 = point
                            isPoint2Unique = False

                    if isPoint1Unique:
                        uniquePoints.append(point1)
                    if isPoint2Unique:
                        uniquePoints.append(point2)
                    lineSegments.append(Segment('S'+str(idNum), point1, point2))
                    idNum += 1

    # create a map instance with initially only the bounding box
    tzMap = TZMap(boundingBox)

    # add segments incrementally to the map
    for segment in lineSegments:
        intersectingTrapezoids = []
        findIntersectingTrapezoids(tzMap.root, segment, intersectingTrapezoids)
        # handle new segment in two cases: it either intersects one trapezoid or many of them
        if len(intersectingTrapezoids) == 1:
            updateMapForOneTrapezoid(tzMap, intersectingTrapezoids[0], segment)
        else:
            updateMapForManyTrapezoids(tzMap, intersectingTrapezoids, segment)

    # assign unique names to all trapezoids in the map
    totTrapezoids = tzMap.assignTrapezpoidNames()
    print 'Map built successfully:- Points: '+ str(len(uniquePoints)) \
          + ', Segments:' + str(len(lineSegments)) + ', Trapezoids: ' + str(totTrapezoids)

    # convert map to a adjacency matrix and print to file
    tzMap.createAdjMatrix(uniquePoints, len(lineSegments), totTrapezoids)

    # ask user for coordinates and print traversal path
    user_coords = raw_input('Enter coordinates: ').split(' ')
    userPoint = Point('userPoint', int(user_coords[0]), int(user_coords[1]))
    tzMap.printTraversalPath(userPoint)

def updateMapForOneTrapezoid(tzMap, trapezoid, segment):
    """
    Function to update the map if the new segment lies entirely
    within one existing trapezoid.
    :param tzMap: graph instance of the trapezoidal map
    :param trapezoid: existing trapezoid encompassing the segment
    :param segment: new segment to be added to the map
    :return: None
    """
    leftTrapezoid = TrapezoidNode(trapezoid.topSegment, trapezoid.bottomSegment, trapezoid.leftPoint, segment.leftPoint)
    topTrapezoid = TrapezoidNode(trapezoid.topSegment, segment, segment.leftPoint, segment.rightPoint)
    bottomTrapezoid = TrapezoidNode(segment, trapezoid.bottomSegment, segment.leftPoint, segment.rightPoint)
    rightTrapezoid = TrapezoidNode(trapezoid.topSegment, trapezoid.bottomSegment, segment.rightPoint, trapezoid.rightPoint)

    segNode = YNode(segment, topTrapezoid, bottomTrapezoid)
    q = XNode(segment.rightPoint, segNode, rightTrapezoid)
    p = XNode(segment.leftPoint, leftTrapezoid, q)
    trapezoid.replacePositionWith(tzMap, p)


def updateMapForManyTrapezoids(tzMap, intersectingTrapezoids, segment):
    """
    Function to update map if the new segment lies within
    several existing trapezoids.
    :param tzMap:graph instance of the trapezoidal map
    :param intersectingTrapezoids: list of existing trapezoids
                                        encompassing the segment
    :param segment: new segment to be added to the map
    :return: None
    """
    upperMidTrapezoid = None
    lowerMidTrapezoid = None
    mergeUpper = False

    for trapezoid in intersectingTrapezoids:

        if trapezoid.containsPoint(segment.leftPoint):
            # case where the left endpoint of the new segment lies in the trapezoid
            leftTrapezoid = TrapezoidNode(trapezoid.topSegment, trapezoid.bottomSegment, trapezoid.leftPoint, segment.leftPoint)
            if segment.isPointAbove(trapezoid.rightPoint):
                upperMidTrapezoid = TrapezoidNode(trapezoid.topSegment, segment, segment.leftPoint, trapezoid.rightPoint)
                lowerMidTrapezoid = TrapezoidNode(segment, trapezoid.bottomSegment, segment.leftPoint, None)
                mergeUpper = False
            else:
                upperMidTrapezoid = TrapezoidNode(trapezoid.topSegment, segment, segment.leftPoint, None)
                lowerMidTrapezoid = TrapezoidNode(segment, trapezoid.bottomSegment, segment.leftPoint, trapezoid.rightPoint)
                mergeUpper = True

            if segment.leftPoint.seen:
                continue
            segNode = YNode(segment, upperMidTrapezoid, lowerMidTrapezoid)
            p = XNode(segment.leftPoint, leftTrapezoid, segNode)
            trapezoid.replacePositionWith(tzMap, p)

        elif trapezoid.containsPoint(segment.rightPoint):
            # case where the right endpoint of the new segment lies in the trapezoid
            rightTrapezoid = TrapezoidNode(trapezoid.topSegment, trapezoid.bottomSegment, segment.rightPoint, trapezoid.rightPoint)
            if mergeUpper:
                upperMidTrapezoid.rightPoint = segment.rightPoint
                lowerMidTrapezoid = TrapezoidNode(segment, trapezoid.bottomSegment, trapezoid.leftPoint, segment.rightPoint)
            else:
                upperMidTrapezoid = TrapezoidNode(trapezoid.topSegment, segment, trapezoid.leftPoint, segment.rightPoint)
                lowerMidTrapezoid.rightPoint = segment.rightPoint
            if segment.rightPoint.seen:
                continue
            segNode = YNode(segment, upperMidTrapezoid, lowerMidTrapezoid)
            q = XNode(segment.rightPoint, segNode, rightTrapezoid)
            trapezoid.replacePositionWith(tzMap, q)

        else:
            # case where the no endpoint of the new segment lies in the trapezoid
            if mergeUpper:
                lowerMidTrapezoid = TrapezoidNode(segment, trapezoid.bottomSegment, trapezoid.leftPoint, None)
            else:
                upperMidTrapezoid = TrapezoidNode(trapezoid.topSegment, segment, trapezoid.leftPoint, None)

            if segment.isPointAbove(trapezoid.rightPoint):
                upperMidTrapezoid.rightPoint = trapezoid.rightPoint
                mergeUpper = False
            else:
                lowerMidTrapezoid.rightPoint = trapezoid.rightPoint
                mergeUpper = True

            segNode = YNode(segment, upperMidTrapezoid, lowerMidTrapezoid)
            trapezoid.replacePositionWith(tzMap, segNode)


def findIntersectingTrapezoids(node, segment, intersectingTrapezoids):
    """
    Recursive function that finds all existing trapezoids in the map
    that the new segment intersects.
    :param node: a node in the map. Initially it's the root
    :param segment: new segment to be added to the map
    :param intersectingTrapezoids: a list of intersecting trapezoids
                                    to be filled by the function.
                                    Initially empty
    :return: None
    """
    if node.isLeaf:
        if node.containsSegment(segment):
            if node not in intersectingTrapezoids:
                intersectingTrapezoids.append(node)

    elif node.type == 'xnode':
        if segment.leftPoint.x >= node.endPoint.x:
            findIntersectingTrapezoids(node.right, segment, intersectingTrapezoids)
        else:
            findIntersectingTrapezoids(node.left, segment, intersectingTrapezoids)
            if segment.rightPoint.x >= node.endPoint.x:
                findIntersectingTrapezoids(node.right, segment, intersectingTrapezoids)

    else:
        if node.lineSegment.isPointAbove(segment.leftPoint):
            findIntersectingTrapezoids(node.above, segment, intersectingTrapezoids)
        else:
            findIntersectingTrapezoids(node.below, segment, intersectingTrapezoids)


if __name__ == '__main__':
    main()
