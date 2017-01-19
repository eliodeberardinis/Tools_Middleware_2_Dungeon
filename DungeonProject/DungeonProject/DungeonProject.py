from fbx import *
import sys
from DungeonBuilder import *

# Function to limit the input of difficulty from 1 to 5
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

    #Input the difficulty of the dungeon from 1 to 5
    difficulty = inputDifficulty()
    print("DIFFICULTY: '%s'." % difficulty)

    #Create the graph for the dungeon
    graph = buildGraph(int(numIteration), difficulty)
    print graph

    #Make a scene with a composite mesh
    scene2 = FbxScene.Create(manager, '')
    # buildDungeon(graph, [0, 0, 0, 0, 0], manager, scene, scene2, CollisionSystem(True), difficulty)
    buildDungeonHash(graph, [0, 0, 0, 0, 0], manager, scene, scene2, CollisionSystem(True), difficulty)

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