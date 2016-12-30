from fbx import *
import sys

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