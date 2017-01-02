import random
from TileGenerator import *
from Utilities import *

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

# Build a dungeon according to the given branch from the given transform point
# Builds a corridor followed by the first room in the graph, the recursively does so for the continuing branches
def buildDungeon(graph, transform, manager, kitScene, scene, collisions, difficultyLevel):
    if len(graph) == 0:
        return

    #If the spawn room is to be built, don't build a path first
    corridorTransform = transform
    if graph[0] != "O":
        corridorBuilder = CorridorBuilder(manager, kitScene, scene, collisions, transform, difficultyLevel)
        corridorTransform = corridorBuilder.run()

    #Obtain the branches after the room to be built
    graphs = split(graph[1:]) if len(graph) > 1 else [] 

    #Build the room
    properties = {
        "isSpawnRoom": graph[0] == "O",
        "numExits": len(graphs)
        }
    roomTransforms = buildRoom(properties, corridorTransform, manager, kitScene, scene, collisions)

    #If failed to place room, retry
    while not roomTransforms and transform != corridorTransform: # Backtrack until no more corridor alternatives can be generated
        print "--------------"
        corridorTransform = corridorBuilder.run()
        roomTransforms = buildRoom(properties, corridorTransform, manager, kitScene, scene, collisions)

    #Recursively build the next part of the dungeon
    for i in range(len(graphs)):
        buildDungeon(graphs[i], roomTransforms[i], manager, kitScene, scene, collisions, difficultyLevel)

# Builds a path from the given transform point and according to the given difficulty level
# For now, paths should only return one path, since they are built between one room and another
class CorridorBuilder:

    def __init__(self, manager, kitScene, scene, collisions, transform, difficultyLevel):
        self.manager = manager
        self.kitScene = kitScene
        self.scene = scene
        self.collisions = collisions
        self.difficultyLevel = difficultyLevel
        self.transforms = [transform]
        self.weights = []

        # Choose the length of the corridor depending on the chosen difficulty
        self.length = random.randint(*[[5, 10], [5, 15], [10, 20], [15, 25], [20, 30]][difficultyLevel-1])

        # Select the tile weights to be used
        self.tileWeights = [
            {
                400: {0: 10, 1: 1, 2: 1, 8: 1},
                800: {12: 10, 13: 1, 14: 1, 24: 1},
                1600: {30: 10, 31: 1, 32: 1, 42: 1}
            },
            {
                400: {0: 10, 1: 2.5, 2: 2.5, 8: 1},
                800: {12: 10, 13: 2.5, 14: 2.5, 24: 1},
                1600: {30: 10, 31: 2.5, 32: 2.5, 42: 1}
            },
            {
                400: {0: 10, 1: 2.5, 2: 2.5, 10: 1, 11: 1, 8: 1, 22: 0.5},
                800: {12: 10, 13: 2.5, 14: 2.5, 28: 1, 29: 1, 24: 1, 23: 0.25, 40: 0.25},
                1600: {30: 10, 31: 2.5, 32: 2.5, 42: 1, 41: 2.5}
            },
            {
                400: {0: 10, 1: 3.33, 2: 3.33, 10: 2.5, 11: 2.5, 8: 1, 22: 1},
                800: {12: 10, 13: 3.33, 14: 3.33, 28: 2.5, 29: 2.5, 24: 1, 23: 0.25, 40: 0.25},
                1600: {30: 10, 31: 3.33, 32: 3.33, 42: 1, 41: 6}
            },
            {
                400: {0: 10, 1: 5, 2: 5, 10: 3.33, 11: 3.33, 8: 1, 22: 1.5},
                800: {12: 10, 13: 5, 14: 5, 28: 3.33, 29: 3.33, 24: 1, 23: 0.25, 40: 0.25},
                1600: {30: 10, 31: 5, 32: 5, 42: 1, 41: 8.16}
            }][difficultyLevel-1]

    # Runs the generation of the corridor
    # Can be run more than once, and it will keep building corridor alternatives
    # Returns the transform of the end of the corridor (from where to keep generating the dungeon)
    def run(self):
        # If this is not the first run, backtrack and start generation
        if len(self.transforms) > 1:
            self.backtrack()

        # Repeat the generation until the number of tiles to place has been reached
        i = len(self.transforms) - 1
        while len(self.transforms) - 1 < self.length: 
            ret = False
            # If the generator comes from backtracking, use the remaining weights that 
            #   were not explored when generating this tile
            if len(self.weights) <= i:
                tileWeights = self.tileWeights[self.transforms[-1][4]]
                self.weights.append({key:tileWeights[key] for key in tileWeights})

            # Try with all alternatives
            while not ret and len(self.weights[-1]) > 0:
                tile = randomWeightedChoice(self.weights[-1])
                print i, tile
                ret = generateTile(tile, self.transforms[-1], self.manager, self.kitScene, self.scene, self.collisions)
                del self.weights[-1][tile]

            # If successed, continue iterating
            if ret:
                self.transforms += [ret[0]]
                i += 1
            # If all alternatives failed, backtrack and continue generation
            else: 
                if i == 0: # Do not backtrack if no more elements available
                    break
                self.backtrack()
                i -= 1

        return self.transforms[-1]

    # Removes the last tile that was placed
    def backtrack(self):
        print "<--"
        # Remove the last mesh placed in the scene
        node = self.scene.GetRootNode().GetChild(self.scene.GetRootNode().GetChildCount() - 1)
        self.scene.GetRootNode().RemoveChild(node)
        node.Destroy()

        # Remove the collision data for the removed mesh
        self.collisions.removeLast()

        self.transforms.pop()
        if len(self.weights[-1]) == 0:
            self.weights.pop()
            self.transforms.pop()


# Builds a room from the given transform point according to the given properties
# Returns the list of points from where build the next paths of the dungeon
def buildRoom(properties, transform, manager, kitScene, scene, collisions):
    #Save original transform to place a door if room succeeds to be placed
    originalTransform = [i for i in transform]

    #Build the room with one tile according to the number of exits needed for the room
    transform = generateTile({
            0: 12 if originalTransform[4] == 400 or properties["isSpawnRoom"] else 30,
            1: 12 if originalTransform[4] == 400 or properties["isSpawnRoom"] else 30,
            2: 15 if originalTransform[4] == 400 or properties["isSpawnRoom"] else 33,
            3: 18 if originalTransform[4] == 400 or properties["isSpawnRoom"] else 36
        }[properties["numExits"]], transform, manager, kitScene, scene, collisions)

    #If room collided, remove added tiles and return error
    if not transform:
        return False

    #Build entry door
    generateTile({
            400: 22 if not properties["isSpawnRoom"] else 19,
            800: 40 if not properties["isSpawnRoom"] else 37,
            1600: 42 if not properties["isSpawnRoom"] else 39
        }[originalTransform[4] if not properties["isSpawnRoom"] else 400], originalTransform, manager, kitScene, scene, collisions)

    #Build doors on each exit
    for i in range(len(transform)):
        transform[i] = generateTile({
                400: 8 if properties["numExits"] > 0 else 9,
                800: 23 if properties["numExits"] > 0 else 26,
                1600: 41 if properties["numExits"] > 0 else 44
            }[transform[i][4]], transform[i], manager, kitScene, scene, collisions)[0]

    return transform
