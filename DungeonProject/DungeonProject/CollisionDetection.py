import sys

class CollisionDetection:

    # Checks if the given BB overlaps with any of the of BB's in the list
    @staticmethod
    def checkCollision(bb1, bbs):
        for bb in bbs:
            if testCollision(bb1, bb):
                return True
        return False

    # Checks if two BB's (Bounding Boxes) overlap
    # A BB is defined by: [centre, [sizeX, sizeY, sizeZ]]
    #   where centre is a transform (4D vector),
    #   and sizeN is a pair of two values (each one for each direction)
    # This collision test is based on checking collisions in the projections to the planes of each BB
    #   This is called the Separating Axis Theorem (reference: http://www.dyn4j.org/2010/01/sat/)
    @staticmethod
    def testCollision(bb1, bb2):
        return testCollisionOnProjectionPlane(bb1[0][3], bb1, bb2) and \
            testCollisionOnProjectionPlane(bb1[0][3] + 90, bb1, bb2) and \
            testCollisionOnProjectionPlane(bb2[0][3], bb1, bb2) and \
            testCollisionOnProjectionPlane(bb2[0][3] + 90, bb1, bb2)

    # Checks if two BB's collide when projected onto the vertical origin-passing plane given by the angle
    @staticmethod
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
    @staticmethod
    def checkCollisionAABB(aabb1, aabb2):
        return aabb1[0] < aabb2[0] + aabb2[2] and \
            aabb1[0] + aabb1[2] > aabb2[0] and \
            aabb1[1] < aabb2[1] + aabb2[3] and \
            aabb1[1] + aabb1[3] > aabb2[1]


