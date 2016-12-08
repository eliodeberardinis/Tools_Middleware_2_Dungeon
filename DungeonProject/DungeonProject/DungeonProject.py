from fbx import *
import sys
import math
import random

'''
Structure with information about the tiles
First element is the index to the actual tile
    Note that the same tile can be used in several ways (the same corner tile can be used to
    turn right or left), so it will need several entries, one for each configuration.
Second element is the origin offset with which to place the tile so it matches the current transform
Third element is the offset from the origin where the exit of the tile is (so where to place the next tile)

Note that the offset is a 4-dimensional vector.
The three first values are the x, y and z coordinate values.
The fourth value is the rotation about the Y axis.
'''
tiles = [
    [36, [0, 0, 400, 0], [[0, 0, -800, 0]]], #narrow hallway
    [37, [0, 0, 200, 0], [[200, 0, -200, -90]]], #narrow corner right
    [37, [200, 0, 0, 90], [[-200, 0, -200, 90]]], #narrow corner left
    [34, [200, 0, 0, 90], [[-200, 0, -200, 90], [200, 0, -200, -90]]], #narrow corner 3 T
    [34, [0, 0, 200, 0], [[0, 0, -400, 0], [200, 0, -200, -90]]], #narrow corner 3 right
    [34, [0, 0, -200, 180], [[-200, 0, -200, 90], [0, 0, -400, 0]]], #narrow corner 3 left
    [33, [0, 0, 200, 0], [[-200, 0, -200, 90], [0, 0, -400, 0], [200, 0, -200, -90]]], #narrow corner 4
    [24, [0, 0, 0, 0], [[0, 0, 0, 0]]], #narrow door square-wide
    [28, [0, 0, 0, 0], [[0, 0, 0, 0]]], #narrow door angle
    [27, [0, 0, 0, 0], [[0, 0, 0, 0]]], #narrow door square
    [35, [0, 0, -400, 180], [[0, -400, -1600, 0]]], #narrow ramp down
    [35, [0, -400, 1200, 0], [[0, 400, -1600, 0]]], #narrow ramp up
    [17, [0, 0, 400, 0], [[0, 0, -800, 0]]], #wide hallway
    [30, [0, 0, 400, 0], [[400, 0, -400, -90]]], #wide corner right
    [30, [400, 0, 0, 90], [[-400, 0, -400, 90]]], #wide corner left
    [31, [400, 0, 0, 90], [[-400, 0, -400, 90], [400, 0, -400, -90]]], #wide corner 3 T
    [31, [0, 0, 400, 0], [[0, 0, -800, 0], [400, 0, -400, -90]]], #wide corner 3 right
    [31, [0, 0, -400, 180], [[-400, 0, -400, 90], [0, 0, -800, 0]]], #wide corner 3 left
    [32, [0, 0, 400, 0], [[-400, 0, -400, 90], [0, 0, -800, 0], [400, 0, -400, -90]]], #wide corner 4
    [25, [0, 0, 0, 0], [[0, 0, 0, 0]]], #wide door angle-wide
    [29, [0, 0, 0, 0], [[0, 0, 0, 0]]], #wide door angle
    [26, [0, 0, 0, 0], [[0, 0, 0, 0]]], #wide door square
    [18, [0, 0, -400, 180], [[0, -400, -1600, 0]]], #wide ramp down
    [18, [0, -400, 1200, 0], [[0, 400, -1600, 0]]], #wide ramp up
    [6, [0, 0, 800, 0], [[0, 0, -1600, 0]]], #extrawide hallway
    [5, [0, 0, 800, 0], [[800, 0, -800, -90]]], #extrawide corner right
    [5, [800, 0, 0, 90], [[-800, 0, -800, 90]]], #extrawide corner left
    [4, [800, 0, 0, 90], [[-800, 0, -800, 90], [800, 0, -800, -90]]], #extrawide corner 3 T
    [4, [0, 0, 800, 0], [[0, 0, -800, 0], [800, 0, -800, -90]]], #extrawide corner 3 right
    [4, [0, 0, -800, 180], [[-800, 0, -800, 90], [0, 0, -1600, 0]]], #extrawide corner 3 left
    [3, [0, 0, 800, 0], [[-800, 0, -800, 90], [0, 0, -1600, 0], [800, 0, -800, -90]]], #extrawide corner 4
    [2, [0, 0, 0, 0], [[0, 0, 0, 0]]], #extrawide door angle-wide
    [0, [0, 0, 0, 0], [[0, 0, 0, 0]]], #extrawide door angle
    [1, [0, 0, 0, 0], [[0, 0, 0, 0]]], #extrawide door square
]

def copyTile(index, manager, scene, nodeName = "", meshName = ""):
    node = scene.GetRootNode().GetChild(index)
    mesh = node.GetMesh()

    #Create the new node
    if nodeName == "":
        nodeName = node.GetName()
    newNode = FbxNode.Create(manager, nodeName)
    newNode.LclTranslation.Set(FbxDouble3(0, 0, 0))
    newNode.LclScaling.Set(node.LclScaling.Get())
    newNode.LclRotation.Set(node.LclRotation.Get())

    #Create the new mesh
    if meshName == "":
        meshName = mesh.GetName()
    newMesh = FbxMesh.Create(manager, meshName)

    #Copy the vertices in the mesh
    newMesh.InitControlPoints(mesh.GetControlPointsCount())
    for i in range(mesh.GetControlPointsCount()):
        newMesh.SetControlPointAt(mesh.GetControlPointAt(i), i)

    #Copy the polygons in the mesh
    for i in range(mesh.GetPolygonCount()):
        newMesh.BeginPolygon()
        for j in range(mesh.GetPolygonSize(i)):
            newMesh.AddPolygon(mesh.GetPolygonVertex(i, j))
        newMesh.EndPolygon()
    
    #Add the mesh to the node
    newNode.SetNodeAttribute(newMesh)

    return newNode


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

def generateTile(index, transform, manager, kitScene, scene):
    tile = copyTile(tiles[index][0], manager, kitScene)
    scene2.GetRootNode().AddChild(tile)
    tile.LclRotation.Set(FbxDouble3(tile.LclRotation.Get()[0],
                                    tile.LclRotation.Get()[1] + transform[3] - tiles[index][1][3],
                                    tile.LclRotation.Get()[2]))
    x = tiles[index][1][0] * math.cos(math.radians(tiles[index][1][3])) + tiles[index][1][2] * math.sin(math.radians(tiles[index][1][3]))
    z = tiles[index][1][2] * math.cos(math.radians(tiles[index][1][3])) + tiles[index][1][0] * math.sin(math.radians(tiles[index][1][3]))
    tile.LclTranslation.Set(FbxDouble3(transform[0] + x * math.cos(math.radians(transform[3])) - z * math.sin(math.radians(transform[3])),
                                       transform[1] - tiles[index][1][1],
                                       transform[2] - z * math.cos(math.radians(transform[3])) + x * math.sin(math.radians(transform[3]))))
    return [[transform[0] + exit[0] * math.cos(math.radians(transform[3])) + exit[2] * math.sin(math.radians(transform[3])),
            transform[1] + exit[1],
            transform[2] + exit[2] * math.cos(math.radians(transform[3])) - exit[0] * math.sin(math.radians(transform[3])),
            transform[3] + exit[3]]
            for exit in tiles[index][2]]

def buildGraph(numIter):
    g = "O_"
    prevExpansions = 0
    for i in range(numIter):
        g_ = ""
        numNewExpansions = 0
        for c in g:
            if c == "_":
                #Apply rules
                branches = random.randint(0 if prevExpansions > 1 else 1, 3)
                prevExpansions -= 1
                numNewExpansions += branches
                if branches == 1:
                    g_ += "X_"
                elif branches > 1:
                    g_ += "[X_"
                    for j in range(branches-1):
                        g_ += ",X_"
                    g_ += "]"
            else:
                g_ += c
        g = g_
        prevExpansions = numNewExpansions

    #Remove the expanding characters ('_')
    g_ = ""
    for c in g:
        if c != "_":
            g_ += c
    return g_

# Splits a graph into its immediate branches
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

def buildDungeon(graph, transform, manager, kitScene, scene):
    if len(graph) == 0:
        return

    if graph[0] != "O":
        transform = buildPath(transform, manager, kitScene, scene)

    graphs = split(graph[1:]) if len(graph) > 1 else [] 

    properties = {
        "isSpawnRoom": graph[0] == "O",
        "numExits": len(graphs)
        }
    transform = buildRoom(properties, transform, manager, kitScene, scene)

    for i in range(len(graphs)):
        buildDungeon(graphs[i], transform[i], manager, kitScene, scene)

def buildRoom(properties, transform, manager, kitScene, scene):
    transform = generateTile(20 if not properties["isSpawnRoom"] else 19, transform, manager, kitScene, scene)[0]
    transform = generateTile({
            0: 12,
            1: 12,
            2: 15,
            3: 18
        }[properties["numExits"]], transform, manager, kitScene, scene)
    for i in range(len(transform)):
        transform[i] = generateTile(20 if properties["numExits"] > 0 else 21, transform[i], manager, kitScene, scene)[0]
    return transform

def buildPath(transform, manager, kitScene, scene):
    transform = generateTile(0, transform, manager, kitScene, scene)[0]
    return transform

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

    #Create the graph for the dungeon
    graph = buildGraph(3)
    print graph

    #Make a scene with a composite mesh
    scene2 = FbxScene.Create(manager, '')
    buildDungeon(graph, [0, 0, 0, 0], manager, scene, scene2)

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