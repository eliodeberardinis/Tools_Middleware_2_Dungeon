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
import DungeonBuilder
from DungeonBuilder import *

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
    graph = DungeonBuilder.buildGraph(int(numIteration), difficulty)
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