# Dungeon Generator (Tools and Middleware)

Requires the [NumPy](http://www.numpy.org/) library (python library for numeric computing):
- Update / install pip: `python -m pip install --upgrade pip`
- Install numpy via pip: `pip install --user numpy`

##Tile management

In order to position and concatenate tiles correctly, they system uses a data structure which holds information about the transforms of different points of the tile that need to match each other. Every register the data structure contains:
- A reference to the tile in the original FBX file
- The transform of the 'in-point'. When placing the tile in the scene, it will be rotated so that this point matches the 'out-point' of the previously placed tile.
- The list of 'out-points' originated from this tile. Notice that a tile can have several out-points, for example, for tiles used in crossings and such.

Note that a tile can be used in several configurations, and so each of them will need its own register in the data structure (for instance, a tile used in a corner might be used for a turn right or left).

Note also that each transform is described as a 5-dimensional vector:
- First 3 coordinates represent the X, Y and Z positions.
- 4th coordinate represents the rotation around the vertical axis. This parameter is not limited to square angle values, so in theory, the system could support management of tiles that are not fixed to a grid. However, notice there is also information on the vertical axis, so the system doesn't support any orientation, as this would need the use of quaternions which would make that calculations a bit more complicated. Hence, all the tiles have to be stick to the horizontal plane. This, however, doesn't mean that tiles cannot be positioned at different levels. It just means this has to be done with tiles that are placed horizontally by default (for example, a tile for a piece of stairs, where the in-point is at height 0, and the out-point is at height 1).
- Finally, the 5h coordinate contains the 'width' of the union, which is used to match corridors' sizes (so only corridors of the same size can match, and not abruptly change in width withouth the use of a door).

##Collision system

In order to ensure that corridors are crossing through one another, or in general that a tile is overlapping a previously placed one, a collision system is used. Since the tile management allows for any orientation in the horizontal plane, the collision system has been designed to allow for tiles to not necessarily be placed on a grid. Hence, the system uses bounding-box collisions using the Separating Axis Theorem.

However, even if simple, this is a slightly intensive computation, specially for a tool run in Python. For that reason, the systems allows for a flag to be turned on to true in case all the tiles used in the generation are going to stick to a grid (they only use square angles). With this flag turned on, the system uses AABB (Axis-Aligned Bounding Box) collisions, which are much more efficiently. Furthermore, these computations have been optimized with the use of matrix operations using the NumPy library, which allows for all the collision computations to be performed as a whole chunk in a matrix, which furtherly increases performance, specially for big and complex dungeons.

##Graph generation

The first element that is generated is a high-level graph of the dungeon, which basically represents what rooms will exist in the dungeon, and what paths will exist between them. For simplicity purposes, the graph is limited to a grammar-generated tree.

The generation can be controlled with two paramaters:
- Number of iterations. This is equivalent to the maximum depth of the tree, and directly relates to the size of the dungeon.
- Level of difficulty. This value controls several aspects of the generation of the graph, such as the amount of child nodes another node can have, the frequency of these splits, or from how early on in the dungeon can they appear. The difficulty ranges from "Very Easy" to "Very Hard" offering 5 levels of customization. A Detailed Description of these rules can be found in the "RULES for Dungeon Generator.docx" file.

##Dungeon generation

Using this high-level graph, the dungeon is then generated recursively from the root node, traversing the tree in depth. Each node will generate a room in the dungeon, and the edges will be corridors between the rooms.

Rooms are generated with one tile thar can be of 2 different sizes and then populated with random decorative elements such as columns, walls, stairs and combination of thereof. This random combination of decorative elements helps adding variety to the dungeon and a more unique feeling for each new instance.

Note that a very simplistic backtracking mechanism exists, where the dungeon will keep trying to place a room if its generation failed, by repeatedly removing the last tile of the corridor that leads to that room. For simplicity purposes, backtracking in this aspect can only performed through the last corridor, and it will finally failed if it reaches the previous room.

####Corridor generation

The generation of corridors is run by the concatenation of tiles one after another. The selection of which tiles to use each time is done via weighted probablities, which are also dependant on the global level of difficulty of the dungeon generation (this also influences the actual length of the corridors). For instance, an easy dungeon will only contain mostly-straight corridors with few turns, but a difficult dungeon will feature corridors with multitude of turns, changes of height level and changes in the width of the corridor.

Furthermore, another slightly more complex backtracking mechanism exists in the generation of a corridor, where, upon failing to place a tile, the system will try with the alternative tiles that are available for that difficulty. Also, if all alternatives have been explored, the last tile will be removed and generation will be resumed from that point (meaning that it will not try already explored alternatives).


#Team

From very early on the team worked in a well organized schedule meeting in person or via skype twice a week in the beggining and once a week towards the end of the project. Tasks were given to each member during these meetings and updates/collaborations on the progress of each task was discussed between the team members on a regular basis.
Pablo took the role of the project manager setting up, among other things, the main framework of the generator. Specifically this is a summary of the main tasks each memeber had within the project:

1. Pablo:

- Tile management system & edge points data structure.
- Collision system and its optimizations.
- Room and corridor generation, including backtracking mechanisms.
- Created some Examples from previous experience with the FBX SDK, in order to allow for other team members to gain familiarity and understand how to perform basic operations in the API.

2. Javier:

- Input parameters from command line
- Modularization of the project creating separate class depending on functionality
- Hash Array to store tiles as alternative to the common Array

3. Elio: 

- Catalogue of all the tile types with measurements.
- Design and code implementation of Difficulty Rules.
- Design and code implementation of Room Decorations.

##Future work

Finally, it would be possible to expand the work done in several ways that couldn't be done due to the limited time, as other aspects of the generator were set to yield more attractive results, or were simply higher priority:

1. Room generation could be explored in more detail, by being able to generate more intricate customizations (Labyrinths, lava pits) and different types of rules using the available decorative tiles instead of leaving them completely random (e.g. counting the appearance of a specific decoration and making sure it's not repeating too often).
2. Graph generation could be expanded to other that trees, allowing cycles in the graph, which add complexity and depth to the results.
3. Full backtracking could be explored in more detailed, although it has been tested, but the execution times were growing drastically. This, however, would solve some problems with part of the generations stopping prematurely due to a certain subpart of the tree not being able to be generated.
