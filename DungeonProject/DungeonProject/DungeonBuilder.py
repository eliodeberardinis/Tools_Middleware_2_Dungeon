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
                    if numSubIter in mylist[:3] and prevSplits < 3: 
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
                    if numSubIter in mylist[:4] and prevSplits < 4:
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
# Builds a path followed by the first room in the graph, the recursively does so for the continuing branches
def buildDungeon(graph, transform, manager, kitScene, scene, collisions, difficultyLevel):
    if len(graph) == 0:
        return

    #If the spawn room is to be built, don't build a path first
    path = [transform]
    if graph[0] != "O":
        scene.GetRootNode().AddChild(makeBox(32, 128, 32, manager))
        path = buildPath(transform, manager, kitScene, scene, collisions, difficultyLevel)

    #Obtain the branches after the room to be built
    graphs = split(graph[1:]) if len(graph) > 1 else [] 

    #Build the room
    properties = {
        "isSpawnRoom": graph[0] == "O",
        "numExits": len(graphs)
        }
    transform = buildRoom(properties, path[-1], manager, kitScene, scene, collisions)

    #If failed to place room, retry
    if not transform:
        for back in range(len(path)-1): # Backtrack until no more path is available
            #Remove last tile
            node = scene.GetRootNode().GetChild(scene.GetRootNode().GetChildCount() - 1)
            scene.GetRootNode().RemoveChild(node)
            node.Destroy()
            path.pop()
            collisions.removeLast()

            #Retry without adding anything
            transform = buildRoom(properties, path[-1], manager, kitScene, scene, collisions)
            #Break when successfully placed the room
            if transform:
                break

        #If still failed to place the room, stop this branch's generation
        if not transform:
            return

    #Recursively build the next part of the dungeon
    for i in range(len(graphs)):
        buildDungeon(graphs[i], transform[i], manager, kitScene, scene, collisions, difficultyLevel)

# Build a dungeon according to the given branch from the given transform point
# Builds a path followed by the first room in the graph, the recursively does so for the continuing branches
def buildDungeonHash(graph, transform, manager, kitScene, scene, collisions, difficultyLevel):
    if len(graph) == 0:
        return

    #If the spawn room is to be built, don't build a path first
    path = [transform]
    if graph[0] != "O":
        scene.GetRootNode().AddChild(makeBox(32, 128, 32, manager))
        path = buildPathHash(transform, manager, kitScene, scene, collisions, difficultyLevel)

    #Obtain the branches after the room to be built
    graphs = split(graph[1:]) if len(graph) > 1 else [] 

    #Build the room
    properties = {
        "isSpawnRoom": graph[0] == "O",
        "numExits": len(graphs)
        }
    transform = buildRoomHash(properties, path[-1], manager, kitScene, scene, collisions)

    #If failed to place room, retry
    if not transform:
        for back in range(len(path)-1): # Backtrack until no more path is available
            #Remove last tile
            node = scene.GetRootNode().GetChild(scene.GetRootNode().GetChildCount() - 1)
            scene.GetRootNode().RemoveChild(node)
            node.Destroy()
            path.pop()
            collisions.removeLast()

            #Retry without adding anything
            transform = buildRoomHash(properties, path[-1], manager, kitScene, scene, collisions)
            #Break when successfully placed the room
            if transform:
                break

        #If still failed to place the room, stop this branch's generation
        if not transform:
            return

    #Recursively build the next part of the dungeon
    for i in range(len(graphs)):
        buildDungeonHash(graphs[i], transform[i], manager, kitScene, scene, collisions, difficultyLevel)

# Builds a path from the given transform point
# Returns the sequence of path transforms (allowing for simple backtracking)
# Path transform: end point of the path, from where to build the next part of the dungeon
# For now, paths should only return one path, since they are built between one room and another
def buildPath(transform, manager, kitScene, scene, collisions, difficultyLevel):
    transforms = [transform]
    weights = []

    # Choose the length of the corridor depending on the chosen difficulty
    numTiles = random.randint(*[[5, 10], [5, 15], [10, 20], [15, 25], [20, 30]][difficultyLevel-1])

    # Repeat the generation until the number of tiles to place has been reached
    i = 0
    while i < numTiles: 
        ret = False
        # If the generator comes from backtracking, use the remaining weights that 
        #   were not explored when generating this tile
        if len(weights) <= i:
            weights.append({
                    400: [
                        {0: 10, 1: 1, 2: 1, 8: 1},
                        {0: 10, 1: 2.5, 2: 2.5, 8: 1},
                        {0: 10, 1: 2.5, 2: 2.5, 10: 1, 11: 1, 8: 1, 22: 0.5},
                        {0: 10, 1: 3.33, 2: 3.33, 10: 2.5, 11: 2.5, 8: 1, 22: 1},
                        {0: 10, 1: 5, 2: 5, 10: 3.33, 11: 3.33, 8: 1, 22: 1.5}
                    ],
                    800: [
                        {12: 10, 13: 1, 14: 1, 24: 1},
                        {12: 10, 13: 2.5, 14: 2.5, 24: 1},
                        {12: 10, 13: 2.5, 14: 2.5, 28: 1, 29: 1, 24: 1, 23: 0.25, 40: 0.25},
                        {12: 10, 13: 3.33, 14: 3.33, 28: 2.5, 29: 2.5, 24: 1, 23: 0.25, 40: 0.25},
                        {12: 10, 13: 5, 14: 5, 28: 3.33, 29: 3.33, 24: 1, 23: 0.25, 40: 0.25}
                    ],
                    1600: [
                        {30: 10, 31: 1, 32: 1, 42: 1},
                        {30: 10, 31: 2.5, 32: 2.5, 42: 1},
                        {30: 10, 31: 2.5, 32: 2.5, 42: 1, 41: 2.5},
                        {30: 10, 31: 3.33, 32: 3.33, 42: 1, 41: 6},
                        {30: 10, 31: 5, 32: 5, 42: 1, 41: 8.16}
                    ],
                }[transforms[-1][4]][difficultyLevel-1])

        # Try with all alternatives
        while not ret and len(weights[-1]) > 0:
            tile = randomWeightedChoice(weights[-1])
            ret = generateTile(tile, transforms[-1], manager, kitScene, scene, collisions)
            del weights[-1][tile]

        if ret:
            transforms += [ret[0]]
            i += 1
        # If all alternatives failed, backtrack and continue generation
        else: 
            if i == 0: # Do not backtrack if no more elements available
                break
            node = scene.GetRootNode().GetChild(scene.GetRootNode().GetChildCount() - 1)
            scene.GetRootNode().RemoveChild(node)
            node.Destroy()
            collisions.removeLast()
            weights.pop()
            transforms.pop()
            i -= 1

    return transforms

# Builds a path from the given transform point
# Returns the sequence of path transforms (allowing for simple backtracking)
# Path transform: end point of the path, from where to build the next part of the dungeon
# For now, paths should only return one path, since they are built between one room and another
def buildPathHash(transform, manager, kitScene, scene, collisions, difficultyLevel):
    transforms = [transform]
    weights = []

    # Choose the length of the corridor depending on the chosen difficulty
    numTiles = random.randint(*[[5, 10], [5, 15], [10, 20], [15, 25], [20, 30]][difficultyLevel-1])

    # Repeat the generation until the number of tiles to place has been reached
    i = 0
    while i < numTiles: 
        ret = False
        # If the generator comes from backtracking, use the remaining weights that 
        #   were not explored when generating this tile
        if len(weights) <= i:
            weights.append({
                    400: [
                        {"CORRIDOR_N_1WAY_Z_NOT_": 10, "CORRIDOR_N_2WAY_R_NOT_": 1, "CORRIDOR_N_2WAY_L_NOT_": 1, "DOOR_N_HOUSE_Z_NOT_": 1},
                        {"CORRIDOR_N_1WAY_Z_NOT_": 10, "CORRIDOR_N_2WAY_R_NOT_": 2.5, "CORRIDOR_N_2WAY_L_NOT_": 2.5, "DOOR_N_HOUSE_Z_NOT_": 1},
                        {"CORRIDOR_N_1WAY_Z_NOT_": 10, "CORRIDOR_N_2WAY_R_NOT_": 2.5, "CORRIDOR_N_2WAY_L_NOT_": 2.5, "CORRIDOR_N_DOWN_Z_NOT_": 1, "CORRIDOR_N_UP_Z_NOT_": 1, "DOOR_N_HOUSE_Z_NOT_": 1, "DOOR_W_HOUSE_Z_N-W_": 0.5},
                        {"CORRIDOR_N_1WAY_Z_NOT_": 10, "CORRIDOR_N_2WAY_R_NOT_": 3.33, "CORRIDOR_N_2WAY_L_NOT_": 3.33, "CORRIDOR_N_DOWN_Z_NOT_": 2.5, "CORRIDOR_N_UP_Z_NOT_": 2.5, "DOOR_N_HOUSE_Z_NOT_": 1, "DOOR_W_HOUSE_Z_N-W_": 1},
                        {"CORRIDOR_N_1WAY_Z_NOT_": 10, "CORRIDOR_N_2WAY_R_NOT_": 5, "CORRIDOR_N_2WAY_L_NOT_": 5, "CORRIDOR_N_DOWN_Z_NOT_": 3.33, "CORRIDOR_N_UP_Z_NOT_": 3.33, "DOOR_N_HOUSE_Z_NOT_": 1, "DOOR_W_HOUSE_Z_N-W_": 1.5}
                    ],
                    800: [
                        {"CORRIDOR_W_1WAY_Z_NOT_": 10, "CORRIDOR_W_2WAY_R_NOT_": 1, "CORRIDOR_W_2WAY_L_NOT_": 1, "DOOR_W_HOUSE_Z_W-W_": 1},
                        {"CORRIDOR_W_1WAY_Z_NOT_": 10, "CORRIDOR_W_2WAY_R_NOT_": 2.5, "CORRIDOR_W_2WAY_L_NOT_": 2.5, "DOOR_W_HOUSE_Z_W-W_": 1},
                        {"CORRIDOR_W_1WAY_Z_NOT_": 10, "CORRIDOR_W_2WAY_R_NOT_": 2.5, "CORRIDOR_W_2WAY_L_NOT_": 2.5, "CORRIDOR_W_DOWN_Z_NOT_": 1, "CORRIDOR_W_UP_Z_NOT_": 1, "DOOR_W_HOUSE_Z_W-W_": 1, "DOOR_W_HOUSE_Z_W-N_": 0.25, "DOOR_EW_SQUARE_Z_W-EW_": 0.25},
                        {"CORRIDOR_W_1WAY_Z_NOT_": 10, "CORRIDOR_W_2WAY_R_NOT_": 3.33, "CORRIDOR_W_2WAY_L_NOT_": 3.33, "CORRIDOR_W_DOWN_Z_NOT_": 2.5, "CORRIDOR_W_UP_Z_NOT_": 2.5, "DOOR_W_HOUSE_Z_W-W_": 1, "DOOR_W_HOUSE_Z_W-N_": 0.25, "DOOR_EW_SQUARE_Z_W-EW_": 0.25},
                        {"CORRIDOR_W_1WAY_Z_NOT_": 10, "CORRIDOR_W_2WAY_R_NOT_": 5, "CORRIDOR_W_2WAY_L_NOT_": 5, "CORRIDOR_W_DOWN_Z_NOT_": 3.33, "CORRIDOR_W_UP_Z_NOT_": 3.33, "DOOR_W_HOUSE_Z_W-W_": 1, "DOOR_W_HOUSE_Z_W-N_": 0.25, "DOOR_EW_SQUARE_Z_W-EW_": 0.25}
                    ],
                    1600: [
                        {"CORRIDOR_EW_1WAY_Z_NOT_": 10, "ROOM_EW_2WAY_R_NOT_": 1, "ROOM_EW_2WAY_L_NOT_": 1, "DOOR_EW_SQUARE_Z_EW-EW_": 1},
                        {"CORRIDOR_EW_1WAY_Z_NOT_": 10, "ROOM_EW_2WAY_R_NOT_": 2.5, "ROOM_EW_2WAY_L_NOT_": 2.5, "DOOR_EW_SQUARE_Z_EW-EW_": 1},
                        {"CORRIDOR_EW_1WAY_Z_NOT_": 10, "ROOM_EW_2WAY_R_NOT_": 2.5, "ROOM_EW_2WAY_L_NOT_": 2.5, "DOOR_EW_SQUARE_Z_EW-EW_": 1, "DOOR_EW_SQUARE_Z_EW-W_": 2.5},
                        {"CORRIDOR_EW_1WAY_Z_NOT_": 10, "ROOM_EW_2WAY_R_NOT_": 3.33, "ROOM_EW_2WAY_L_NOT_": 3.33, "DOOR_EW_SQUARE_Z_EW-EW_": 1, "DOOR_EW_SQUARE_Z_EW-W_": 6},
                        {"CORRIDOR_EW_1WAY_Z_NOT_": 10, "ROOM_EW_2WAY_R_NOT_": 5, "ROOM_EW_2WAY_L_NOT_": 5, "DOOR_EW_SQUARE_Z_EW-EW_": 1, "DOOR_EW_SQUARE_Z_EW-W_": 8.16}
                    ],
                }[transforms[-1][4]][difficultyLevel-1])

        # Try with all alternatives
        while not ret and len(weights[-1]) > 0:
            tile = randomWeightedChoice(weights[-1])
            ret = generateTileHash(tile, transforms[-1], manager, kitScene, scene, collisions)
            del weights[-1][tile]

        if ret:
            transforms += [ret[0]]
            i += 1
        # If all alternatives failed, backtrack and continue generation
        else: 
            if i == 0: # Do not backtrack if no more elements available
                break
            node = scene.GetRootNode().GetChild(scene.GetRootNode().GetChildCount() - 1)
            scene.GetRootNode().RemoveChild(node)
            node.Destroy()
            collisions.removeLast()
            weights.pop()
            transforms.pop()
            i -= 1

    return transforms

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

    # Build the room decorations
    size = transform[0][4] / 2
    centreTransform = translate(originalTransform, [0, 0, -size])
    centreTransform[4] = 0
    DecorateRoom(centreTransform, [size, 600, size], manager, kitScene, scene, collisions)

    #Build doors on each exit
    for i in range(len(transform)):
        transform[i] = generateTile({
                400: 8 if properties["numExits"] > 0 else 9,
                800: 23 if properties["numExits"] > 0 else 26,
                1600: 41 if properties["numExits"] > 0 else 44
            }[transform[i][4]], transform[i], manager, kitScene, scene, collisions)[0]

    return transform

# Builds a room from the given transform point according to the given properties
# Returns the list of points from where build the next paths of the dungeon
def buildRoomHash(properties, transform, manager, kitScene, scene, collisions):
    #Save original transform to place a door if room succeeds to be placed
    originalTransform = [i for i in transform]

    #Build the room with one tile according to the number of exits needed for the room
    transform = generateTileHash({
            0: "CORRIDOR_W_1WAY_Z_NOT_" if originalTransform[4] == 400 or properties["isSpawnRoom"] else "CORRIDOR_EW_1WAY_Z_NOT_",
            1: "CORRIDOR_W_1WAY_Z_NOT_" if originalTransform[4] == 400 or properties["isSpawnRoom"] else "CORRIDOR_EW_1WAY_Z_NOT_",
            2: "CORRIDOR_W_3WAY_T_NOT_" if originalTransform[4] == 400 or properties["isSpawnRoom"] else "ROOM_EW_3WAY_T_NOT_",
            3: "CORRIDOR_W_4WAY_Z_NOT_" if originalTransform[4] == 400 or properties["isSpawnRoom"] else "ROOM_EW_4WAY_Z_NOT_"
        }[properties["numExits"]], transform, manager, kitScene, scene, collisions)

    #If room collided, remove added tiles and return error
    if not transform:
        return False

    #Build entry door
    generateTileHash({
            400: "DOOR_W_HOUSE_Z_N-W_" if not properties["isSpawnRoom"] else "DOOR_W_COMBI_Z_N-W_",
            800: "DOOR_EW_SQUARE_Z_W-EW_" if not properties["isSpawnRoom"] else "DOOR_EW_COMBI_Z_W-EW_",
            1600: "DOOR_EW_SQUARE_Z_EW-EW_" if not properties["isSpawnRoom"] else "DOOR_EW_COMBI_Z_EW-EW_"
        }[originalTransform[4] if not properties["isSpawnRoom"] else 400], originalTransform, manager, kitScene, scene, collisions)

     # Build the room decorations
    size = transform[0][4] / 2
    centreTransform = translate(originalTransform, [0, 0, -size])
    centreTransform[4] = 0
    DecorateRoomHash(centreTransform, [size, 600, size], manager, kitScene, scene, collisions)

    #Build doors on each exit
    for i in range(len(transform)):
        transform[i] = generateTileHash({
                400: "DOOR_N_HOUSE_Z_NOT_" if properties["numExits"] > 0 else "DOOR_N_SQUARE_Z_NOT_",
                800: "DOOR_W_HOUSE_Z_W-N_" if properties["numExits"] > 0 else "DOOR_W_SQUARE_Z_W-N_",
                1600: "DOOR_EW_SQUARE_Z_EW-W_" if properties["numExits"] > 0 else "DOOR_EW_HOUSE_Z_EW-W_"
            }[transform[i][4]], transform[i], manager, kitScene, scene, collisions)[0]

    return transform

# Builds decoration for a room, given by its centre point and its dimensions in each axis calling pre-defined decoration Methods
def DecorateRoom(centre, size, manager, kitScene, scene, collisions):
    # Save the tile Original Center
    originalCentre = centre
    # Translate the point where the tile is going to be placed
    if size[0] == 400:
        #Small Room
        type = random.randint(0,4)
        #Single Small Column in the Center
        if type == 0:
            CreateColumnInCenter(originalCentre, manager, kitScene, scene,46) #SmallColumn Tile 46
        
        #4 Small Columns at every angle
        elif type == 1:
            CreateFourSmallColumns(originalCentre, manager, kitScene, scene, 250)

        #4 Small Columns at every angle + one in the centre
        elif type == 2:
            CreateColumnInCenter(originalCentre, manager, kitScene, scene, 46)
            CreateFourSmallColumns(originalCentre, manager, kitScene, scene, 250)  

        elif type == 3:
            CreateColumnInCenter(originalCentre, manager, kitScene, scene,47)  #Big Column

        elif type == 4:
            CreateTwoColumnsOppositeOnX(originalCentre, manager, kitScene, scene, 46) #2 small columns opposite
             
    else:
        #Bigger Rooms
        type = random.randint(43,52)

        #4 small columns in every corner
        if type == 43:
            CreateColumnInCenter(originalCentre, manager, kitScene, scene,47)
            AddSmallColumns = random.randint(0,2)
            if AddSmallColumns == 1:
                CreateFourSmallColumns(originalCentre, manager, kitScene, scene, 550)
            elif AddSmallColumns == 2:
                CreateFourSmallColumns(originalCentre, manager, kitScene, scene, 250)

        elif type == 44:
            CreateFourSmallColumns(originalCentre, manager, kitScene, scene, 550)
        
        #4 Squared walls in the middle creating an H structure with 2 small columns
        elif type == 45:
            CreateHStructureInMiddle(originalCentre, manager, kitScene, scene, 50)     
            CreateTwoColumnsOppositeOnX(originalCentre, manager, kitScene, scene, 46)  
    
        #4 Squared walls in the middle creating a pool
        elif type == 46:
            CreateSquareFenceInMiddle(originalCentre, manager, kitScene, scene, 50)   
            additions =  random.randint(0,6)
            if additions == 1:
                CreateColumnInCenter(originalCentre, manager, kitScene, scene, 46)
            elif additions == 2:
                CreateColumnInCenter(originalCentre, manager, kitScene, scene, 47)
            elif additions == 3:
                CreateFourSmallColumns(originalCentre, manager, kitScene, scene,550)
            elif additions == 4:
                CreateColumnInCenter(originalCentre, manager, kitScene, scene, 46)
                CreateFourSmallColumns(originalCentre, manager, kitScene, scene,550)
            elif additions == 5:
                CreateColumnInCenter(originalCentre, manager, kitScene, scene, 47)
                CreateFourSmallColumns(originalCentre, manager, kitScene, scene,550)
            elif additions == 6:
                CreateColumnInCenter(originalCentre, manager, kitScene, scene, 47)
                CreateFourSmallColumns(originalCentre, manager, kitScene, scene,250)

        #4 Random Object In The Middle with or without columns close or far
        elif type >= 47:
            RandObjInMiddle = random.randint(47,52)
            CreateObjectInMiddle(originalCentre, manager, kitScene, scene, RandObjInMiddle)
            additions =  random.randint(0,2)
            if additions == 1:
                CreateFourSmallColumns(originalCentre, manager, kitScene, scene,550)
            elif additions == 2:
                CreateFourSmallColumns(originalCentre, manager, kitScene, scene, 250)

# Builds decoration for a room, given by its centre point and its dimensions in each axis calling pre-defined decoration Methods
def DecorateRoomHash(centre, size, manager, kitScene, scene, collisions):
    # Save the tile Original Center
    originalCentre = centre
    # Translate the point where the tile is going to be placed
    if size[0] == 400:
        #Small Room
        type = random.randint(0,4)
        #Single Small Column in the Center
        if type == 0:
            CreateColumnInCenterHash(originalCentre, manager, kitScene, scene, "COLUMN_N_SMALL_Z_NOT_") #SmallColumn Tile 46
        
        #4 Small Columns at every angle
        elif type == 1:
            CreateFourSmallColumnsHash(originalCentre, manager, kitScene, scene, 250)

        #4 Small Columns at every angle + one in the centre
        elif type == 2:
            CreateColumnInCenterHash(originalCentre, manager, kitScene, scene, "COLUMN_N_SMALL_Z_NOT_")
            CreateFourSmallColumnsHash(originalCentre, manager, kitScene, scene, 250)  

        elif type == 3:
            CreateColumnInCenterHash(originalCentre, manager, kitScene, scene, "COLUMN_N_LARGE_Z_NOT_")  #Big Column

        elif type == 4:
            CreateTwoColumnsOppositeOnXHash(originalCentre, manager, kitScene, scene, "COLUMN_N_SMALL_Z_NOT_") #2 small columns opposite
             
    else:
        #Bigger Rooms
        type = random.randint(43,52)

        #4 small columns in every corner
        if type == 43:
            CreateColumnInCenterHash(originalCentre, manager, kitScene, scene, "COLUMN_N_LARGE_Z_NOT_")
            AddSmallColumns = random.randint(0,2)
            if AddSmallColumns == 1:
                CreateFourSmallColumnsHash(originalCentre, manager, kitScene, scene, 550)
            elif AddSmallColumns == 2:
                CreateFourSmallColumnsHash(originalCentre, manager, kitScene, scene, 250)

        elif type == 44:
            CreateFourSmallColumnsHash(originalCentre, manager, kitScene, scene, 550)
        
        #4 Squared walls in the middle creating an H structure with 2 small columns
        elif type == 45:
            CreateHStructureInMiddleHash(originalCentre, manager, kitScene, scene, "WALL_N_SQUARE_Z_NOT_")     
            CreateTwoColumnsOppositeOnXHash(originalCentre, manager, kitScene, scene, "COLUMN_N_SMALL_Z_NOT_")  
    
        #4 Squared walls in the middle creating a pool
        elif type == 46:
            CreateSquareFenceInMiddleHash(originalCentre, manager, kitScene, scene, "WALL_N_SQUARE_Z_NOT_")   
            additions =  random.randint(0,6)
            if additions == 1:
                CreateColumnInCenterHash(originalCentre, manager, kitScene, scene, "COLUMN_N_SMALL_Z_NOT_")
            elif additions == 2:
                CreateColumnInCenterHash(originalCentre, manager, kitScene, scene, "COLUMN_N_LARGE_Z_NOT_")
            elif additions == 3:
                CreateFourSmallColumnsHash(originalCentre, manager, kitScene, scene,550)
            elif additions == 4:
                CreateColumnInCenterHash(originalCentre, manager, kitScene, scene, "COLUMN_N_SMALL_Z_NOT_")
                CreateFourSmallColumnsHash(originalCentre, manager, kitScene, scene,550)
            elif additions == 5:
                CreateColumnInCenterHash(originalCentre, manager, kitScene, scene, "COLUMN_N_LARGE_Z_NOT_")
                CreateFourSmallColumnsHash(originalCentre, manager, kitScene, scene,550)
            elif additions == 6:
                CreateColumnInCenterHash(originalCentre, manager, kitScene, scene, "COLUMN_N_LARGE_Z_NOT_")
                CreateFourSmallColumnsHash(originalCentre, manager, kitScene, scene,250)

        #4 Random Object In The Middle with or without columns close or far
        elif type >= 47:
            # Change that to names
            RandObjInMiddle = random.choice(["COLUMN_N_LARGE_Z_NOT_", "STEP_N_ROUND_Z_NOT_", "WALL_N_ROUND_Z_NOT_", "WALL_N_SQUARE_Z_NOT_", "STEP_N_SQUARE_Z_NOT_", "WALL_N_TALLSQUARE_Z_NOT_"]);
            CreateObjectInMiddleHash(originalCentre, manager, kitScene, scene, RandObjInMiddle)
            additions =  random.randint(0,2)
            if additions == 1:
                CreateFourSmallColumnsHash(originalCentre, manager, kitScene, scene,550)
            elif additions == 2:
                CreateFourSmallColumnsHash(originalCentre, manager, kitScene, scene, 250)

#Methods Creating some decorations
def CreateColumnInCenter(Originalcentre,manager, kitScene, scene, ColumnTile): #Big Column Tile 47, Small Column tile 46
    centre = Originalcentre
    if ColumnTile > 47:
        centre = translate(Originalcentre, [0, 0, 0])
        RandomRotation = random.randint(0,3)
        if RandomRotation == 1:
            centre[3] += 90
        elif RandomRotation == 2:
            centre[3] += 180
        elif RandomRotation == 3:
            centre[3] -= 90
    generateTile(ColumnTile, centre, manager, kitScene, scene, None)

#Methods Creating some decorations
def CreateColumnInCenterHash(Originalcentre,manager, kitScene, scene, ColumnTile): #Big Column Tile 47, Small Column tile 46
    centre = Originalcentre
    if ColumnTile > 47:
        centre = translate(Originalcentre, [0, 0, 0])
        RandomRotation = random.randint(0,3)
        if RandomRotation == 1:
            centre[3] += 90
        elif RandomRotation == 2:
            centre[3] += 180
        elif RandomRotation == 3:
            centre[3] -= 90
    generateTileHash(ColumnTile, centre, manager, kitScene, scene, None)

def CreateFourSmallColumns(Originalcentre, manager, kitScene, scene, distance):
    for i in range(4):
                if i == 0:
                    a = distance
                    b = distance
                elif i == 1:
                    a = - distance
                    b = distance
                elif i == 2:
                    a = distance
                    b = - distance
                elif i == 3:
                    a = - distance
                    b = - distance
                centre = translate(Originalcentre, [a, 0, b])
                generateTile(46, centre, manager, kitScene, scene, None)

def CreateFourSmallColumnsHash(Originalcentre, manager, kitScene, scene, distance):
    for i in range(4):
                if i == 0:
                    a = distance
                    b = distance
                elif i == 1:
                    a = - distance
                    b = distance
                elif i == 2:
                    a = distance
                    b = - distance
                elif i == 3:
                    a = - distance
                    b = - distance
                centre = translate(Originalcentre, [a, 0, b])
                generateTileHash("COLUMN_N_SMALL_Z_NOT_", centre, manager, kitScene, scene, None)

def CreateTwoColumnsOppositeOnX(Originalcentre, manager, kitScene, scene, ColumnTile):
    for i in range(2):
                if i == 0:
                    centre = translate(Originalcentre, [250, 0, 0])
                elif i == 1:
                    centre = translate(Originalcentre, [-250, 0, 0])
                generateTile(ColumnTile, centre, manager, kitScene, scene, None)

def CreateTwoColumnsOppositeOnXHash(Originalcentre, manager, kitScene, scene, ColumnTile):
    for i in range(2):
                if i == 0:
                    centre = translate(Originalcentre, [250, 0, 0])
                elif i == 1:
                    centre = translate(Originalcentre, [-250, 0, 0])
                generateTileHash(ColumnTile, centre, manager, kitScene, scene, None) 

def CreateObjectInMiddle(Originalcentre, manager, kitScene, scene, StartTileNumber): #StartTile 48 round steps, 49 round walls , 50 square wall, 51 square steps, 52 square wall tall
    for i in range(4):
                if i == 0:
                    centre = translate(Originalcentre, [180, 0, 180])
                elif i == 1:
                    centre = translate(Originalcentre, [-180, 0, 180])
                    centre[3] -= 90
                elif i == 2:
                    centre = translate(Originalcentre, [180, 0, -180])
                    centre[3] += 90
                elif i == 3:
                    centre = translate(Originalcentre, [-180, 0, -180])
                    centre[3] += 180
                generateTile(StartTileNumber, centre, manager, kitScene, scene, None)

def CreateObjectInMiddleHash(Originalcentre, manager, kitScene, scene, StartTileNumber): #StartTile 48 round steps, 49 round walls , 50 square wall, 51 square steps, 52 square wall tall
    for i in range(4):
                if i == 0:
                    centre = translate(Originalcentre, [180, 0, 180])
                elif i == 1:
                    centre = translate(Originalcentre, [-180, 0, 180])
                    centre[3] -= 90
                elif i == 2:
                    centre = translate(Originalcentre, [180, 0, -180])
                    centre[3] += 90
                elif i == 3:
                    centre = translate(Originalcentre, [-180, 0, -180])
                    centre[3] += 180
                generateTileHash(StartTileNumber, centre, manager, kitScene, scene, None)

def CreateHStructureInMiddle(Originalcentre, manager, kitScene, scene, StartTileNumber): #50 for squared wall
    for i in range(4):
                if i == 0:
                    centre = translate(Originalcentre, [180, 0, -180])           
                elif i == 1:
                    centre = translate(Originalcentre, [-180, 0, -180])
                    centre[3] -= 90
                elif i == 2:
                    centre = translate(Originalcentre, [180, 0, 180])
                    centre[3] += 90
                elif i == 3:
                    centre = translate(Originalcentre, [-180, 0, 180])
                    centre[3] -= 180                 
                generateTile(StartTileNumber, centre, manager, kitScene, scene, None)

def CreateHStructureInMiddleHash(Originalcentre, manager, kitScene, scene, StartTileNumber): #50 for squared wall
    for i in range(4):
                if i == 0:
                    centre = translate(Originalcentre, [180, 0, -180])           
                elif i == 1:
                    centre = translate(Originalcentre, [-180, 0, -180])
                    centre[3] -= 90
                elif i == 2:
                    centre = translate(Originalcentre, [180, 0, 180])
                    centre[3] += 90
                elif i == 3:
                    centre = translate(Originalcentre, [-180, 0, 180])
                    centre[3] -= 180                 
                generateTileHash(StartTileNumber, centre, manager, kitScene, scene, None)

def CreateSquareFenceInMiddle(Originalcentre, manager, kitScene, scene, StartTileNumber):  #50 for squared wall
     for i in range(4):
                if i == 0:
                    centre = translate(Originalcentre, [-180, 0, -180])
                elif i == 1:
                    centre = translate(Originalcentre, [180, 0, -180])
                    centre[3] -= 90
                elif i == 2:
                    centre = translate(Originalcentre, [-180, 0, 180])
                    centre[3] += 90
                elif i == 3:
                    centre = translate(Originalcentre, [180, 0, 180])
                    centre[3] += 180
                generateTile(StartTileNumber, centre, manager, kitScene, scene, None)

def CreateSquareFenceInMiddleHash(Originalcentre, manager, kitScene, scene, StartTileNumber):  #50 for squared wall
     for i in range(4):
                if i == 0:
                    centre = translate(Originalcentre, [-180, 0, -180])
                elif i == 1:
                    centre = translate(Originalcentre, [180, 0, -180])
                    centre[3] -= 90
                elif i == 2:
                    centre = translate(Originalcentre, [-180, 0, 180])
                    centre[3] += 90
                elif i == 3:
                    centre = translate(Originalcentre, [180, 0, 180])
                    centre[3] += 180
                generateTileHash(StartTileNumber, centre, manager, kitScene, scene, None)