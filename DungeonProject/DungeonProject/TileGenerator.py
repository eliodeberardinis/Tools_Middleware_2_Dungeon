# This module contains methods related to the use of the FBX API for tile generation and management

from fbx import *
from TileFile import *
from MathModule import *
from CollisionDetection import *

# Makes a copy of the tile specified by index and returns a node that contains the new mesh
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

# Places a the tile specified by index to match with the point specified by transform, and adds it to the scene.
# Returns the new transform points where to place the next tiles
# If the tile to be generated would overlap any of the previously placed tiles, returns false.
def generateTile(index, transform, manager, kitScene, scene, collisions):
    # Calculates the x and z coordinates of the tile (these depend on the rotation of the "in point" of the tile)
    x = tiles[index][1][0] * cos(tiles[index][1][3]) + tiles[index][1][2] * sin(tiles[index][1][3])
    z = tiles[index][1][2] * cos(tiles[index][1][3]) + tiles[index][1][0] * sin(tiles[index][1][3])

    # Sets the final coordinates of the tile to match the coordinates of the given transform
    newTransform = [transform[0] + x * cos(transform[3]) - z * sin(transform[3]),
                    transform[1] - tiles[index][1][1],
                    transform[2] - z * cos(transform[3]) + x * sin(transform[3]),
                    transform[3] - tiles[index][1][3], 
                    tiles[index][1][4]]

    # Check if the tile would overlap any of the previously place
    bb = [newTransform, tiles[index][3]]
    if not collisions.checkAndAddCollision(bb):
        return False

    # Create the node with the tile's mesh and adds it to the scene
    tile = copyTile(tiles[index][0], manager, kitScene)
    scene.GetRootNode().AddChild(tile)

    # Set the transform of the tile
    tile.LclRotation.Set(FbxDouble3(tile.LclRotation.Get()[0], tile.LclRotation.Get()[1] + newTransform[3], tile.LclRotation.Get()[2]))
    tile.LclTranslation.Set(FbxDouble3(newTransform[0], newTransform[1], newTransform[2]))

    # Returns a list of the new points (transforms) where the next tiles will be placed
    return [[transform[0] + exit[0] * cos(transform[3]) + exit[2] * sin(transform[3]),
            transform[1] + exit[1],
            transform[2] + exit[2] * cos(transform[3]) - exit[0] * sin(transform[3]),
            transform[3] + exit[3],
            exit[4]]
            for exit in tiles[index][2]]

def checkTileCompatibility(index1, index2):
    return next((t for t in tiles[index1][4:6][1] if t in tiles[index2][4:6][0]), None) is None