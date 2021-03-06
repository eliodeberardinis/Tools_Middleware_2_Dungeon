# This module contains the methods used for collision detection

from MathModule import *
import numpy as np

class CollisionSystem:
    # Initializes the collision system instance
    def __init__(self, useOptimizedAABBCollisions):
        self.useOptimizedAABBCollisions = useOptimizedAABBCollisions
        self.bbs = []

    # Checks if the given BB overlaps with any of the of BB's in the list
    def checkAndAddCollision(self, bb1):
        if self.useOptimizedAABBCollisions:
            aabb = np.array(BBToAABB(bb1))[np.newaxis]
            if self.bbs == []:
                self.bbs = aabb
            else:
                if checkCollisionAABBBulk(self.bbs, aabb):
                    return False
                self.bbs = np.append(self.bbs, aabb, 0)
            return True
        else:
            for bb in self.bbs:
                if testCollision(bb1, bb):
                    return False
            self.bbs.append(bb1)
            return True

    # Removes the last element from the collision system
    def removeLast(self):
        self.bbs = self.bbs[:-1]

# Checks if two BB's (Bounding Boxes) overlap
# A BB is defined by: [centre, [sizeX, sizeY, sizeZ]]
#   where centre is a transform (4D vector),
#   and sizeN is a pair of two values (each one for each direction)
# This collision test is based on checking collisions in the projections to the planes of each BB
#   This is called the Separating Axis Theorem (reference: http://www.dyn4j.org/2010/01/sat/)
def testCollision(bb1, bb2):
    return testCollisionOnProjectionPlane(bb1[0][3], bb1, bb2) and \
        testCollisionOnProjectionPlane(bb1[0][3] + 90, bb1, bb2) and \
        testCollisionOnProjectionPlane(bb2[0][3], bb1, bb2) and \
        testCollisionOnProjectionPlane(bb2[0][3] + 90, bb1, bb2)

# Checks if two BB's collide when projected onto the vertical origin-passing plane given by the angle
def testCollisionOnProjectionPlane(angle, bb1, bb2):
    # Get the corner points of each BB
    bb1points = getBBpoints(bb1)
    bb2points = getBBpoints(bb2)

    # Project every point onto the plane
    projbb1 = [projectPointOntoPlane(angle, point) for point in bb1points]
    projbb2 = [projectPointOntoPlane(angle, point) for point in bb2points]

    # Check if the AABB's that contain the projected points collide
    aabb1 = AABB(projbb1)
    aabb2 = AABB(projbb2)
    return checkCollisionAABB(aabb1, aabb2)

# Checks if the two AABB's (Axis Aligned Bounding Box) collide
# Reference: https://developer.mozilla.org/en-US/docs/Games/Techniques/2D_collision_detection
def checkCollisionAABB(aabb1, aabb2):
    for i in range(len(aabb1)):
        if aabb1[i][0] >= aabb2[i][1] or aabb1[i][1] <= aabb2[i][0]:
            return False
    return True

# Checks if the given aabb collides with any of the given aabbs
def checkCollisionAABBBulk(aabbs, aabb):
    checks = np.dstack((aabbs[:,:,0] < aabb[:,:,1], aabbs[:,:,1] > aabb[:,:,0]))
    return np.any(np.all(np.all(checks, 2), 1))