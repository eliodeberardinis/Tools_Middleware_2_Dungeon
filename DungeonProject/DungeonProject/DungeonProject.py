from fbx import *
import sys
import math
import random
import TileFile
from TileFile import *
import MathModule
from MathModule import *
import TileGenerator
from TileGenerator import *

# Creates a box mesh with the specified dimensions and returns a node that contains it
def makeBox(width, height, depth, manager, nodeName = "", meshName = ""):
    width *= 0.5
    depth *= 0.5
    newNode = FbxNode.Create(manager, nodeName)
    newMesh = FbxMesh.Create(manager, meshName)

    #Copy the vertices in the mesh
    newMesh.InitControlPoints(8)
    newMesh.SetControlPointAt(FbxVector4(width, 0.0, depth, 0.0), 0)
    newMesh.SetControlPointAt(FbxVector4(width, 0.0, -depth, 0.0), 1)
    newMesh.SetControlPointAt(FbxVector4(-width, 0.0, -depth, 0.0), 2)
    newMesh.SetControlPointAt(FbxVector4(-width, 0.0, depth, 0.0), 3)
    newMesh.SetControlPointAt(FbxVector4(width, height, depth, 0.0), 4)
    newMesh.SetControlPointAt(FbxVector4(width, height, -depth, 0.0), 5)
    newMesh.SetControlPointAt(FbxVector4(-width, height, -depth, 0.0), 6)
    newMesh.SetControlPointAt(FbxVector4(-width, height, depth, 0.0), 7)
    newMesh.BeginPolygon(); #bottom
    newMesh.AddPolygon(0);
    newMesh.AddPolygon(3);
    newMesh.AddPolygon(2);
    newMesh.AddPolygon(1);
    newMesh.EndPolygon();
    newMesh.BeginPolygon(); #top
    newMesh.AddPolygon(4);
    newMesh.AddPolygon(5);
    newMesh.AddPolygon(6);
    newMesh.AddPolygon(7);
    newMesh.EndPolygon();    
    newMesh.BeginPolygon(); #front
    newMesh.AddPolygon(0);
    newMesh.AddPolygon(4);
    newMesh.AddPolygon(7);
    newMesh.AddPolygon(3);
    newMesh.EndPolygon();    
    newMesh.BeginPolygon(); #back
    newMesh.AddPolygon(1);
    newMesh.AddPolygon(2);
    newMesh.AddPolygon(6);
    newMesh.AddPolygon(5);
    newMesh.EndPolygon();    
    newMesh.BeginPolygon(); #right
    newMesh.AddPolygon(0);
    newMesh.AddPolygon(1);
    newMesh.AddPolygon(5);
    newMesh.AddPolygon(4);
    newMesh.EndPolygon();    
    newMesh.BeginPolygon(); #left
    newMesh.AddPolygon(2);
    newMesh.AddPolygon(3);
    newMesh.AddPolygon(7);
    newMesh.AddPolygon(6);
    newMesh.EndPolygon();
    
    #Add the mesh to the node
    newNode.SetNodeAttribute(newMesh)

    return newNode

# Generates a tree graph that represents the high level structure of the dungeon
# Nodes are represented by each letter character
# Two nodes connected by one path are represented by two consecutive letters: XX
# A node branching out into multiple paths is represented by X[path1, path2, ..., pathN]
# The character '_' represents the points where the grammar will be expanding the tree on each iteration
def buildGraph(numIter, difficultyLevel):
    g = "O_" #Axiom of the grammar
    prevExpansions = 1
    prevSplits = 0
    numSubIter = -1
    num2Splits = 0
    num3Splits = 0
    mylist = range(5) # list of integers from 0 to 4 
    random.shuffle(mylist)

    for i in range(numIter): #Generate iterations
        g_ = ""
        numSubIter += 1
        prevSplits = 0
        if numSubIter > 4:
            numSubIter = 0
            random.shuffle(mylist)
            num2Splits = 0
            num3Splits = 0
                   
        numNewExpansions = 0
        for c in g:
            if c == "_": #If it is an expansion character, apply the rules
                #Decide on how many paths will branch out from this point (0 through 3)
                #Only allow for 0 when there is at least another expansion character in the current iteration
                #(meaning that at least one branch of the tree will reach the maximum number of iterations)

                #Very Easy
                if difficultyLevel == 1:
                    branches = 1
                #Easy   
                elif difficultyLevel == 2:
                    if numSubIter == mylist[0] and prevSplits < 1:  # Use prevSplit parameter if you want to count the splits globally
                        branches = 2
                        prevSplits += 1

                    elif prevExpansions > 1:
                            branches = random.randint(0,1)
                    else:
                            branches = 1                     
                #Medium
                elif difficultyLevel == 3:
                     if numSubIter in mylist[:2] and prevSplits < 2: # Use prevSplit parameter if you want to count the splits globally
                        if num3Splits < 1:
                           branches = random.randint(2,3)
                        else:
                            branches = 2
                           
                        prevSplits += 1
                            
                     elif prevExpansions > 1:
                            branches = random.randint(0,1)
                     else:
                        branches = 1

                     if branches == 2:
                           num2Splits += 1
                     elif branches == 3:
                           num3Splits += 1
                #Hard
                elif difficultyLevel == 4:
                     if numSubIter in mylist[:3] and prevSplits < 3: # Maybe change the rules to add minmum 2 1:2 splits
                        if num2Splits + num3Splits < 2:
                           branches = random.randint(2,3)
                        else:
                            branches = random.randint(0,2)

                        prevSplits += 1
                            
                     elif prevExpansions > 2:
                            branches = random.randint(0,1)
                     else:
                        branches = 1

                     if branches == 2:
                           num2Splits += 1
                     elif branches == 3:
                           num3Splits += 1
                
                #VeryHard
                elif difficultyLevel == 5:
                     if numSubIter in mylist[:4] and prevSplits < 4: # Maybe change the rules to add minmum 2 1:3 splits
                        if num2Splits + num3Splits < 3:
                           branches = random.randint(2,3)
                        else:
                            branches = random.randint(0,3)

                        prevSplits += 1
                            
                     elif prevExpansions > 3:
                            branches = random.randint(0,1)
                     else:
                        branches = 1

                     if branches == 2:
                           num2Splits += 1
                     elif branches == 3:
                           num3Splits += 1
                

                prevExpansions -= 1
                numNewExpansions += branches

                if branches == 1:
                    #Expand the tree with one sequencial node
                    g_ += "X_"
                elif branches > 1:
                    #Expand the tree with a branching structure
                    g_ += "[X_"
                    for j in range(branches-1):
                        g_ += ",X_"
                    g_ += "]"

            else: #If it is any other character, copy it to the string
                g_ += c
        g = g_
        prevExpansions = numNewExpansions

    #Remove the expanding characters ('_') from the final graph string
    g_ = ""
    for c in g:
        if c != "_":
            g_ += c
    return g_

# Splits a graph into its immediate branches
# Examples:
# split("XXXX") = ["XXXX"]
# split("[X,XXX]") = ["X","XXX"]
def split(graph):
    if len(graph) == 0 or graph[0] != "[":
        return [graph]
    graphs = [""]
    depth = 0
    for c in graph[1:-1]:
        if c == "," and depth == 0:
            graphs += [""]
        else:
            graphs[-1] += c
            depth += 1 if c == "[" else -1 if c == "]" else 0
    return graphs

# Build a dungeon according to the given branch from the given transform point
# Builds a path followed by the first room in the graph, the recursively does so for the continuing branches
def buildDungeon(graph, transform, manager, kitScene, scene, placedTiles, difficultyLevel):
    if len(graph) == 0:
        return

    #If the spawn room is to be built, don't build a path first
    path = [transform]
    if graph[0] != "O":
        scene.GetRootNode().AddChild(makeBox(32, 128, 32, manager))
        path = buildPath(transform, manager, kitScene, scene, placedTiles, difficultyLevel)

    #Obtain the branches after the room to be built
    graphs = split(graph[1:]) if len(graph) > 1 else [] 

    #Build the room
    properties = {
        "isSpawnRoom": graph[0] == "O",
        "numExits": len(graphs)
        }
    transform = buildRoom(properties, path[-1], manager, kitScene, scene, placedTiles)

    #If failed to place room, retry
    if not transform:
        for back in range(len(path)-1): # Backtrack until no more path is available
            #Remove last tile
            node = scene.GetRootNode().GetChild(scene.GetRootNode().GetChildCount() - 1)
            scene.GetRootNode().RemoveChild(node)
            node.Destroy()
            path.pop()
            placedTiles.pop()

            #Retry without adding anything
            transform = buildRoom(properties, path[-1], manager, kitScene, scene, placedTiles)
            #Break when successfully placed the room
            if transform:
                break

        #If still failed to place the room, stop this branch's generation
        if not transform:
            return

    #Recursively build the next part of the dungeon
    for i in range(len(graphs)):
        buildDungeon(graphs[i], transform[i], manager, kitScene, scene, placedTiles, difficultyLevel)

# Builds a room from the given transform point according to the given properties
# Returns the list of points from where build the next paths of the dungeon
def buildRoom(properties, transform, manager, kitScene, scene, placedTiles):
    #Save original transform to place a door if room succeeds to be placed
    originalTransform = [i for i in transform]

    #Build the room with one tile according to the number of exits needed for the room
    transform = TileGenerator.generateTile({
            0: 12 if originalTransform[4] == 400 or properties["isSpawnRoom"] else 30,
            1: 12 if originalTransform[4] == 400 or properties["isSpawnRoom"] else 30,
            2: 15 if originalTransform[4] == 400 or properties["isSpawnRoom"] else 33,
            3: 18 if originalTransform[4] == 400 or properties["isSpawnRoom"] else 36
        }[properties["numExits"]], transform, manager, kitScene, scene, placedTiles)

    #If room collided, remove added tiles and return error
    if not transform:
        return False

    #Build entry door
    TileGenerator.generateTile({
            400: 22 if not properties["isSpawnRoom"] else 19,
            800: 40 if not properties["isSpawnRoom"] else 37,
            1600: 42 if not properties["isSpawnRoom"] else 39
        }[originalTransform[4] if not properties["isSpawnRoom"] else 400], originalTransform, manager, kitScene, scene, [])

    #Build doors on each exit
    for i in range(len(transform)):
        transform[i] = TileGenerator.generateTile({
                400: 8 if properties["numExits"] > 0 else 9,
                800: 23 if properties["numExits"] > 0 else 26,
                1600: 41 if properties["numExits"] > 0 else 44
            }[transform[i][4]], transform[i], manager, kitScene, scene, [])[0]

    return transform

# Returns a random key using the given weights
# Data must be inputed as a dictionary, with choices as keys and weights as values.
def randomWeightedChoice(data):
    cumulative = [sum(data.values()[:i+1]) for i in range(len(data.values()))]
    value = random.uniform(0, cumulative[-1])
    index = next(i for i in range(len(cumulative)) if cumulative[i] > value)
    return data.keys()[index]

# Builds a path from the given transform point
# Returns the sequence of path transforms (allowing for simple backtracking)
#   Path transform: end point of the path, from where to build the next part of the dungeon
# For now, paths should only return one path, since they are built between one room and another
def buildPath(transform, manager, kitScene, scene, placedTiles, difficultyLevel):
    transforms = [transform]
    weights = []

    # Choose the length of the corridor depending on the chosen difficulty
    numTiles = random.randint(*[[5, 10], [5, 15], [10, 20], [15, 25], [20, 30]][difficultyLevel-1])

    # Repeat the generation until the number of tiles to place has been reached
    i = 0
    while i < numTiles: 
        ret = False
        # If the generator comes from backtracking, use the remaining weights that 
        #   were not explored when generating this tile
        if len(weights) <= i:
            weights.append({
                    400: [
                        {0: 10, 1: 1, 2: 1, 8: 1},
                        {0: 10, 1: 2.5, 2: 2.5, 8: 1},
                        {0: 10, 1: 2.5, 2: 2.5, 10: 1, 11: 1, 8: 1, 22: 0.5},
                        {0: 10, 1: 3.33, 2: 3.33, 10: 2.5, 11: 2.5, 8: 1, 22: 1},
                        {0: 10, 1: 5, 2: 5, 10: 3.33, 11: 3.33, 8: 1, 22: 1.5}
                    ],
                    800: [
                        {12: 10, 13: 1, 14: 1, 24: 1},
                        {12: 10, 13: 2.5, 14: 2.5, 24: 1},
                        {12: 10, 13: 2.5, 14: 2.5, 28: 1, 29: 1, 24: 1, 23: 0.25, 40: 0.25},
                        {12: 10, 13: 3.33, 14: 3.33, 28: 2.5, 29: 2.5, 24: 1, 23: 0.25, 40: 0.25},
                        {12: 10, 13: 5, 14: 5, 28: 3.33, 29: 3.33, 24: 1, 23: 0.25, 40: 0.25}
                    ],
                    1600: [
                        {30: 10, 31: 1, 32: 1, 42: 1},
                        {30: 10, 31: 2.5, 32: 2.5, 42: 1},
                        {30: 10, 31: 2.5, 32: 2.5, 42: 1, 41: 2.5},
                        {30: 10, 31: 3.33, 32: 3.33, 42: 1, 41: 6},
                        {30: 10, 31: 5, 32: 5, 42: 1, 41: 8.16}
                    ],
                }[transforms[-1][4]][difficultyLevel-1])

        # Try with all alternatives
        while not ret and len(weights[-1]) > 0:
            tile = randomWeightedChoice(weights[-1])
            ret = TileGenerator.generateTile(tile, transforms[-1], manager, kitScene, scene, placedTiles)
            del weights[-1][tile]

        if ret:
            transforms += [ret[0]]
            i += 1
        # If all alternatives failed, backtrack and continue generation
        else: 
            if i == 0: # Do not backtrack if no more elements available
                break
            node = scene.GetRootNode().GetChild(scene.GetRootNode().GetChildCount() - 1)
            scene.GetRootNode().RemoveChild(node)
            node.Destroy()
            placedTiles.pop()
            weights.pop()
            transforms.pop()
            i -= 1

    return transforms

# Checks if the given BB overlaps with any of the of BB's in the list
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

# Returns the eight corner points of the given BB
def getBBpoints(bb):
    vectors = [
        [[bb[1][0][0] * MathModule.cos(bb[0][3]), 0, bb[1][0][0] * MathModule.sin(bb[0][3])], 
         [bb[1][0][1] * MathModule.cos(bb[0][3]), 0, bb[1][0][1] * MathModule.sin(bb[0][3])],],
        [[0, bb[1][1][0], 0], [0, bb[1][1][1], 0]],
        [[-bb[1][2][0] * MathModule.sin(bb[0][3]), 0, bb[1][2][0] * MathModule.cos(bb[0][3])], 
         [-bb[1][2][1] * MathModule.sin(bb[0][3]), 0, bb[1][2][1] * MathModule.cos(bb[0][3])]],
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

# Checks if the two AABB's (Axis Aligned Bounding Box) collide
# Reference: https://developer.mozilla.org/en-US/docs/Games/Techniques/2D_collision_detection
def checkCollisionAABB(aabb1, aabb2):
    return aabb1[0] < aabb2[0] + aabb2[2] and \
        aabb1[0] + aabb1[2] > aabb2[0] and \
        aabb1[1] < aabb2[1] + aabb2[3] and \
        aabb1[1] + aabb1[3] > aabb2[1]

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
    normal = [-MathModule.sin(angle), 0, MathModule.cos(angle)]
    dotProduct = point[0] * normal[0] + point[2] * normal[2]
    projection = [v * dotProduct for v in normal]

    # Substract the projection the the original point to obtain the projected point
    projected = [point[i] - projection[i] for i in range(len(point))]

    # Change the point to return it in the local coordinates of the plane
    return [projected[0] * MathModule.cos(-angle) - projected[2] * MathModule.sin(-angle), projected[1]]

# Function to limit the input of difficulty to three letter only (E/M/H)
def inputDifficulty():
    # Get input from command line
    diff = raw_input("Enter dungeon difficulty (1-5): ")
    while True:
        # If it´s one of the values we need we exit the function
        if (int(diff)>0 and int(diff)<= 5):
            break
        else:
            #We ask for the input again until it´s one of the values we want
            diff = raw_input("Enter dungeon difficulty (1-5): ")

    # Return the upper case to avoid problems in the generation
    return int(diff)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Error: no kit file path specified.")
        sys.exit(-1)

    #Load the kit scene
    manager = FbxManager.Create()
    scene = FbxScene.Create(manager, '')
    importer = FbxImporter.Create(manager, '')
    if not importer.Initialize(sys.argv[1]):
        print("Error: kit file path not valid: '%s'." % sys.argv[1])
        sys.exit(-1)
    importer.Import(scene)
    importer.Destroy()

    #Input the number of iterations ([1-10])
    numIteration = raw_input("Enter the number of dungeon iterations: ")
    print("ITERATIONS: '%s'." % numIteration)

    #Input the difficulty of the dungeon (E/M/H)
    difficulty = inputDifficulty()
    print("DIFFICULTY: '%s'." % difficulty)

    #Create the graph for the dungeon
    graph = buildGraph(int(numIteration), difficulty)
    print graph

    #Make a scene with a composite mesh
    scene2 = FbxScene.Create(manager, '')
    buildDungeon(graph, [0, 0, 0, 0, 0], manager, scene, scene2, [], difficulty)

    #Save the scene in a new file
    if len(sys.argv) > 2:
        print("Saving the scene into '%s'." % sys.argv[2])
        exporter = FbxExporter.Create(manager, '')
        if not exporter.Initialize(sys.argv[2]):
            print("Error: failed to save the scene into '%s'." % sys.argv[2])
            sys.exit(-1)
        exporter.Export(scene2)
        exporter.Destroy()

    manager.Destroy()
    del scene
    del scene2
    del manager