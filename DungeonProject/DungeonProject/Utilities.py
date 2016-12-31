from fbx import *
import sys
import random

class Utilities:

    # Splits a graph into its immediate branches
    # Examples:
    # split("XXXX") = ["XXXX"]
    # split("[X,XXX]") = ["X","XXX"]
    @staticmethod
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

    # Returns a random key using the given weights
    # Data must be inputed as a dictionary, with choices as keys and weights as values.
    @staticmethod
    def randomWeightedChoice(data):
        cumulative = [sum(data.values()[:i+1]) for i in range(len(data.values()))]
        value = random.uniform(0, cumulative[-1])
        index = next(i for i in range(len(cumulative)) if cumulative[i] > value)
        return data.keys()[index]

    # Creates a box mesh with the specified dimensions and returns a node that contains it
    @staticmethod
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