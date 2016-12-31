from fbx import *
import sys
import TileFile
from TileFile import *
import MathModule
from MathModule import *

class TileGenerator:

    # Makes a copy of the tile specified by index and returns a node that contains the new mesh
    @staticmethod
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
    @staticmethod
    def generateTile(index, transform, manager, kitScene, scene, placedTiles):
        # Calculates the x and z coordinates of the tile (these depend on the rotation of the "in point" of the tile)
        x = TileFile.tiles[index][1][0] * MathModule.cos(TileFile.tiles[index][1][3]) + TileFile.tiles[index][1][2] * MathModule.sin(TileFile.tiles[index][1][3])
        z = TileFile.tiles[index][1][2] * MathModule.cos(TileFile.tiles[index][1][3]) + TileFile.tiles[index][1][0] * MathModule.sin(TileFile.tiles[index][1][3])

        # Sets the final coordinates of the tile to match the coordinates of the given transform
        newTransform = [transform[0] + x * MathModule.cos(transform[3]) - z * MathModule.sin(transform[3]),
                        transform[1] - TileFile.tiles[index][1][1],
                        transform[2] - z * MathModule.cos(transform[3]) + x * MathModule.sin(transform[3]),
                        transform[3] - TileFile.tiles[index][1][3], 
                        TileFile.tiles[index][1][4]]

        # Check if the tile would overlap any of the previously place
        bb = [newTransform, TileFile.tiles[index][3]]
        if checkCollision(bb, placedTiles):
            return False

        # Add the tile to the collision system
        placedTiles += [bb]

        # Create the node with the tile's mesh and adds it to the scene
        tile = TileGenerator.copyTile(TileFile.tiles[index][0], manager, kitScene)
        scene2.GetRootNode().AddChild(tile)

        # Set the transform of the tile
        tile.LclRotation.Set(FbxDouble3(tile.LclRotation.Get()[0], tile.LclRotation.Get()[1] + newTransform[3], tile.LclRotation.Get()[2]))
        tile.LclTranslation.Set(FbxDouble3(newTransform[0], newTransform[1], newTransform[2]))

        # Returns a list of the new points (transforms) where the next tiles will be placed
        return [[transform[0] + exit[0] * MathModule.cos(transform[3]) + exit[2] * MathModule.sin(transform[3]),
                transform[1] + exit[1],
                transform[2] + exit[2] * MathModule.cos(transform[3]) - exit[0] * MathModule.sin(transform[3]),
                transform[3] + exit[3],
                exit[4]]
                for exit in TileFile.tiles[index][2]]