from fbx import *
import sys

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

    #Make another scene with a composite mesh
    scene2 = FbxScene.Create(manager, '')
    door = copyTile(29, manager, scene)
    hallway1 = copyTile(17, manager, scene)
    hallway2 = copyTile(17, manager, scene)
    hallway3 = copyTile(17, manager, scene)
    stairs = copyTile(18, manager, scene)
    scene2.GetRootNode().AddChild(door)
    scene2.GetRootNode().AddChild(hallway1)
    scene2.GetRootNode().AddChild(hallway2)
    scene2.GetRootNode().AddChild(hallway3)
    scene2.GetRootNode().AddChild(stairs)
    door.LclTranslation.Set(FbxDouble3(door.LclTranslation.Get()[0],
                                       door.LclTranslation.Get()[1],
                                       door.LclTranslation.Get()[2] - 1125))
    hallway1.LclTranslation.Set(FbxDouble3(hallway1.LclTranslation.Get()[0],
                                        hallway1.LclTranslation.Get()[1],
                                        hallway1.LclTranslation.Get()[2] - 750))
    #node2.LclTranslation.Set(FbxDouble3(node2.LclTranslation.Get()[0],
                                        #node2.LclTranslation.Get()[1],
                                        #node2.LclTranslation.Get()[2]))
    hallway3.LclTranslation.Set(FbxDouble3(hallway3.LclTranslation.Get()[0],
                                        hallway3.LclTranslation.Get()[1],
                                        hallway3.LclTranslation.Get()[2] + 750))
    stairs.LclTranslation.Set(FbxDouble3(stairs.LclTranslation.Get()[0],
                                        stairs.LclTranslation.Get()[1],
                                        stairs.LclTranslation.Get()[2] + 1500))

    box = makeBox(32, 128, 32, manager, "Player", "PlayerMesh")
    scene2.GetRootNode().AddChild(box)
    box.LclTranslation.Set(FbxDouble3(box.LclTranslation.Get()[0],
                                      box.LclTranslation.Get()[1],
                                      box.LclTranslation.Get()[2] - 1125))
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