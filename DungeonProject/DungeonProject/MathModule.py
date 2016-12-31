# This module contains math related methods and functions

import math

# Added for precision issues
def sin(angle):
    while angle < 0:
        angle += 360
    while angle >= 360:
        angle -= 360
    return {
        0: 0,
        90: 1,
        180: 0,
        270: -1
        }.get(angle, math.sin(math.radians(angle)))

# Added for precision issues
def cos(angle):
    while angle < 0:
        angle += 360
    while angle >= 360:
        angle -= 360
    return {
        0: 1,
        90: 0,
        180: -1,
        270: 0
        }.get(angle, math.cos(math.radians(angle)))

# Returns the eight corner points of the given BB
def getBBpoints(bb):
    vectors = [
        [[bb[1][0][0] * cos(bb[0][3]), 0, bb[1][0][0] * sin(bb[0][3])], 
            [bb[1][0][1] * cos(bb[0][3]), 0, bb[1][0][1] * sin(bb[0][3])],],
        [[0, bb[1][1][0], 0], [0, bb[1][1][1], 0]],
        [[-bb[1][2][0] * sin(bb[0][3]), 0, bb[1][2][0] * cos(bb[0][3])], 
            [-bb[1][2][1] * sin(bb[0][3]), 0, bb[1][2][1] * cos(bb[0][3])]],
        ]

    return [
        addVectors([bb[0][:3], vectors[0][0], vectors[1][0], vectors[2][0]]),
        addVectors([bb[0][:3], vectors[0][0], vectors[1][0], vectors[2][1]]),
        addVectors([bb[0][:3], vectors[0][0], vectors[1][1], vectors[2][0]]),
        addVectors([bb[0][:3], vectors[0][0], vectors[1][1], vectors[2][1]]),
        addVectors([bb[0][:3], vectors[0][1], vectors[1][0], vectors[2][0]]),
        addVectors([bb[0][:3], vectors[0][1], vectors[1][0], vectors[2][1]]),
        addVectors([bb[0][:3], vectors[0][1], vectors[1][1], vectors[2][0]]),
        addVectors([bb[0][:3], vectors[0][1], vectors[1][1], vectors[2][1]])
    ]

# Adds an infinite amount of vectors
# PRE: all vectors must have the same dimension (behaviour undefined if not true)
def addVectors(vectors):
    result = vectors[0]
    for v in vectors[1:]:
        for i in range(len(result)):
            result[i] += v[i]
    return result

# Creates the AABB that contains all points
def AABB(points):
    points = zip(*points)
    min_x = min(points[0])
    max_x = max(points[0])
    min_y = min(points[1])
    max_y = max(points[1])
    return (min_x, min_y, max_x - min_x, max_y - min_y)

# Projects a point onto a vertical origin-passing plane given by the angle
# Returns the projected point in the local coordinates of the plane
def projectPointOntoPlane(angle, point):
    # Computes the projection of the point onto the normal vector
    normal = [-sin(angle), 0, cos(angle)]
    dotProduct = point[0] * normal[0] + point[2] * normal[2]
    projection = [v * dotProduct for v in normal]

    # Substract the projection the the original point to obtain the projected point
    projected = [point[i] - projection[i] for i in range(len(point))]

    # Change the point to return it in the local coordinates of the plane
    return [projected[0] * cos(-angle) - projected[2] * sin(-angle), projected[1]]
