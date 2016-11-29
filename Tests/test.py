from fbx import *
import sys

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

    #Print number of elements in the kit
    for i in range(scene.GetRootNode().GetChildCount()):
        print("%s: %s" % (i, scene.GetRootNode().GetChild(i).GetName()))

    #Save the scene in a new file
    if len(sys.argv) > 2:
        print("Saving the scene into '%s'." % sys.argv[2])
        exporter = FbxExporter.Create(manager, '')
        if not exporter.Initialize(sys.argv[2]):
            print("Error: failed to save the scene into '%s'." % sys.argv[2])
            sys.exit(-1)
        exporter.Export(scene)
        exporter.Destroy()

    manager.Destroy()
    del scene
    del manager