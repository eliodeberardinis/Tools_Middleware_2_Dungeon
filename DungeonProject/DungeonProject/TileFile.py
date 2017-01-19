'''
Naming Convention for tiles

Index X : Type_Width_Name_Orientation

TYPE: Room/Door/Corridor/Wall/Stair/Floor/Column
WIDTH: EW (extra wide) / W (wide) / N (narrow) / X (nothing)
NAME: whatever the piece is
ORIENTATION: L (left) / R (right) / T (t form) / Z (nothing)
TRANSITION: from narrow to wide or extrawide
            N-W / W-N / W-EW / EW-W / W-W / EW-EW / NOT

When you are trying to find a specific piece you look for the parameters in the legend above
enclosed between _WHATEVER_

Index 0: DOOR_EW_SQUARE_Z_
Index 1: DOOR_EW_HOUSE_Z_
Index 2: DOOR_EW_COMBI_Z_
Index 3: ROOM_EW_4WAY_Z_
Index 4: ROOM_EW_3WAY_L_
Index 4: ROOM_EW_3WAY_R_
Index 4: ROOM_EW_3WAY_T_
Index 5: ROOM_EW_2WAY_L_
Index 5: ROOM_EW_2WAY_R_
Index 6: ROOM_EW_1WAY_Z_
Index 7: WALL_X_LFORM_Z_
Index 8: STEP_X_INNER_Z_
Index 9: STEP_X_OUTER_Z_
Index 10: FLOOR_X_SUNKSTEP_Z_
Index 11: FLOOR_X_PLAIN_Z_
Index 12: STEP_X_INNERCURVED_Z_
Index 13: STEP_X_OUTERCURVED_Z_
Index 14: STEP_X_PLAIN_Z_
Index 15: COLUMN_X_LARGE_Z_
Index 16: FLOOR_EW_SUNKCURVED_Z_
Index 17: CORRIDOR_W_1WAY_Z_
Index 18: CORRIDOR_W_UP_Z_
Index 18: CORRIDOR_W_DOWN_Z_
Index 19: COLUMN_X_SMALL_Z_
Index 20: FLOOR_X_SUNKL_Z_
Index 21: WALL_X_CURVED_Z_
Index 22: WALL_X_END_Z_
Index 23: WALL_X_STEP_Z_
Index 24: DOOR_N_RECTANGLE_Z_
Index 25: DOOR_W_COMBI_Z_
Index 26: DOOR_W_SQUARE_Z_
Index 27: DOOR_N_SQUARE_Z_
Index 28: DOOR_N_HOUSE_Z_
Index 29: DOOR_W_HOUSE_Z_
Index 30: CORRIDOR_W_2WAY_L_
Index 30: CORRIDOR_W_2WAY_R_
Index 31: CORRIDOR_W_3WAY_L_
Index 31: CORRIDOR_W_3WAY_R_
Index 31: CORRIDOR_W_3WAY_T_
Index 32: CORRIDOR_W_4WAY_Z_
Index 33: CORRIDOR_N_4WAY_Z_
Index 34: CORRIDOR_N_3WAY_L_
Index 34: CORRIDOR_N_3WAY_R_
Index 34: CORRIDOR_N_3WAY_T_
Index 35: CORRIDOR_N_UP_Z_
Index 35: CORRIDOR_N_DOWN_Z_
Index 36: CORRIDOR_N_1WAY_Z_
Index 37: CORRIDOR_N_2WAY_L_
Index 37: CORRIDOR_N_2WAY_R_
'''

'''
Structure with information about the tiles

First element is the index to the actual tile
    Note that the same tile can be used in several ways (the same corner tile can be used to
    turn right or left), so it will need several entries, one for each configuration.

Second element is the "in point", that is the offset from the origin/centre of the tile to the point
    of the tile that should match the final point of the previously placed tile.

Third element is the "out point", that is the offset from the tile's "in point" that would be the point
    where to place the next tile.

Fourth element is the dimensions of the tile (two values for each axis)

Note that offsets are expressed as 4-dimensional vectorr.
The three first values are the x, y and z coordinate values.
The fourth value is the rotation around the Y axis.
The fifth element is the width of the corridor
'''

tiles = [
    [36, [0, 0, 400, 0, 400], [[0, 0, -800, 0, 400]], [[-200, 200], [0, 600], [-400, 400]]], #narrow hallway                        # 0
    [37, [0, 0, 200, 0, 400], [[200, 0, -200, -90, 400]], [[-200, 200], [0, 600], [-200, 200]]], #narrow corner right               # 1
    [37, [200, 0, 0, 90, 400], [[-200, 0, -200, 90, 400]], [[-200, 200], [0, 600], [-200, 200]]], #narrow corner left               # 2
    [34, [200, 0, 0, 90, 400], [[-200, 0, -200, 90, 400], [200, 0, -200, -90, 400]], [[-200, 200], [0, 600], [-200, 200]]], #narrow corner 3 T
    [34, [0, 0, 200, 0, 400], [[0, 0, -400, 0, 400], [200, 0, -200, -90, 400]], [[-200, 200], [0, 600], [-200, 200]]], #narrow corner 3 right
    [34, [0, 0, -200, 180, 400], [[-200, 0, -200, 90, 400], [0, 0, -400, 0, 400]], [[-200, 200], [0, 600], [-200, 200]]], #narrow corner 3 left
    [33, [0, 0, 200, 0, 400], [[-200, 0, -200, 90, 400], [0, 0, -400, 0, 400], [200, 0, -200, -90, 400]], [[-200, 200], [0, 600], [-200, 200]]], #narrow corner 4
    [24, [0, 0, 0, 0, 400], [[0, 0, 0, 0, 400]], [[-200, 200], [0, 600], [0, 0]]], #narrow door square-wide (narrow-to-narrow)
    [28, [0, 0, 0, 0, 400], [[0, 0, 0, 0, 400]], [[-200, 200], [0, 600], [0, 0]]], #narrow door angle (narrow-to-narrow)                    # 8
    [27, [0, 0, 0, 0, 400], [[0, 0, 0, 0, 400]], [[-200, 200], [0, 600], [0, 0]]], #narrow door square (narrow-to-narrow)                   # 9
    [35, [0, 0, -400, 180, 400], [[0, -400, -1600, 0, 400]], [[-200, 200], [-400, 600], [-400, 1200]]], #narrow ramp down                   # 10
    [35, [0, -400, 1200, 0, 400], [[0, 400, -1600, 0, 400]], [[-200, 200], [-400, 600], [-400, 1200]]], #narrow ramp up
    [17, [0, 0, 400, 0, 800], [[0, 0, -800, 0, 800]], [[-400, 400], [0, 600], [-400, 400]]], #wide hallway                                  # 12
    [30, [0, 0, 400, 0, 800], [[400, 0, -400, -90, 800]], [[-400, 400], [0, 600], [-400, 400]]], #wide corner right                         # 13
    [30, [400, 0, 0, 90, 800], [[-400, 0, -400, 90, 800]], [[-400, 400], [0, 600], [-400, 400]]], #wide corner left
    [31, [400, 0, 0, 90, 800], [[-400, 0, -400, 90, 800], [400, 0, -400, -90, 800]], [[-400, 400], [0, 600], [-400, 400]]], #wide corner 3 T            # 15
    [31, [0, 0, 400, 0, 800], [[0, 0, -800, 0, 800], [400, 0, -400, -90, 800]], [[-400, 400], [0, 600], [-400, 400]]], #wide corner 3 right
    [31, [0, 0, -400, 180, 800], [[-400, 0, -400, 90, 800], [0, 0, -800, 0, 800]], [[-400, 400], [0, 600], [-400, 400]]], #wide corner 3 left
    [32, [0, 0, 400, 0, 800], [[-400, 0, -400, 90, 800], [0, 0, -800, 0, 800], [400, 0, -400, -90, 800]], [[-400, 400], [0, 600], [-400, 400]]], #wide corner 4     # 18
    [25, [0, 0, 0, 0, 400], [[0, 0, 0, 0, 800]], [[-400, 400], [0, 600], [0, 0]]], #wide door angle-wide (narrow-to-wide)                       # 19
    [25, [0, 0, 0, 0, 800], [[0, 0, 0, 0, 400]], [[-400, 400], [0, 600], [0, 0]]], #wide door angle-wide (wide-to-narrow)
    [25, [0, 0, 0, 0, 800], [[0, 0, 0, 0, 800]], [[-400, 400], [0, 600], [0, 0]]], #wide door angle-wide (wide-to-wide)
    [29, [0, 0, 0, 0, 400], [[0, 0, 0, 0, 800]], [[-400, 400], [0, 600], [0, 0]]], #wide door angle (narrow-to-wide)                # 22
    [29, [0, 0, 0, 0, 800], [[0, 0, 0, 0, 400]], [[-400, 400], [0, 600], [0, 0]]], #wide door angle (wide-to-narrow)                # 23
    [29, [0, 0, 0, 0, 800], [[0, 0, 0, 0, 800]], [[-400, 400], [0, 600], [0, 0]]], #wide door angle (wide-to-wide)
    [26, [0, 0, 0, 0, 400], [[0, 0, 0, 0, 800]], [[-400, 400], [0, 600], [0, 0]]], #wide door square (narrow-to-wide)
    [26, [0, 0, 0, 0, 800], [[0, 0, 0, 0, 400]], [[-400, 400], [0, 600], [0, 0]]], #wide door square (wide-to-narrow)               # 26
    [26, [0, 0, 0, 0, 800], [[0, 0, 0, 0, 800]], [[-400, 400], [0, 600], [0, 0]]], #wide door square (wide-to-wide)
    [18, [0, 0, -400, 180, 800], [[0, -400, -1600, 0, 800]], [[-400, 400], [-400, 600], [-400, 1200]]], #wide ramp down             # 28
    [18, [0, -400, 1200, 0, 800], [[0, 400, -1600, 0, 800]], [[-400, 400], [-400, 600], [-400, 1200]]], #wide ramp up
    [6, [0, 0, 800, 0, 1600], [[0, 0, -1600, 0, 1600]], [[-800, 800], [0, 600], [-800, 800]]], #extrawide hallway                           # 30
    [5, [0, 0, 800, 0, 1600], [[800, 0, -800, -90, 1600]], [[-800, 800], [0, 600], [-800, 800]]], #extrawide corner right
    [5, [800, 0, 0, 90, 1600], [[-800, 0, -800, 90, 1600]], [[-800, 800], [0, 600], [-800, 800]]], #extrawide corner left
    [4, [800, 0, 0, 90, 1600], [[-800, 0, -800, 90, 1600], [800, 0, -800, -90, 1600]], [[-800, 800], [0, 600], [-800, 800]]], #extrawide corner 3 T     # 33
    [4, [0, 0, 800, 0, 1600], [[0, 0, -800, 0, 1600], [800, 0, -800, -90, 1600]], [[-800, 800], [0, 600], [-800, 800]]], #extrawide corner 3 right
    [4, [0, 0, -800, 180, 1600], [[-800, 0, -800, 90, 1600], [0, 0, -1600, 0, 1600]], [[-800, 800], [0, 600], [-800, 800]]], #extrawide corner 3 left
    [3, [0, 0, 800, 0, 1600], [[-800, 0, -800, 90, 1600], [0, 0, -1600, 0, 1600], [800, 0, -800, -90, 1600]], [[-800, 800], [0, 600], [-800, 800]]], #extrawide corner 4        # 36
    [2, [0, 0, 0, 0, 800], [[0, 0, 0, 0, 1600]], [[-800, 800], [0, 600], [0, 0]]], #extrawide door angle-wide (wide-to-extrawide)                   # 37
    [2, [0, 0, 0, 0, 1600], [[0, 0, 0, 0, 800]], [[-800, 800], [0, 600], [0, 0]]], #extrawide door angle-wide (extrawide-to-wide)
    [2, [0, 0, 0, 0, 1600], [[0, 0, 0, 0, 1600]], [[-800, 800], [0, 600], [0, 0]]], #extrawide door angle-wide (extrawide-to-extrawide)             # 39
    [0, [0, 0, 0, 0, 800], [[0, 0, 0, 0, 1600]], [[-800, 800], [0, 600], [0, 0]]], #extrawide door angle (wide-to-extrawide)                        # 40
    [0, [0, 0, 0, 0, 1600], [[0, 0, 0, 0, 800]], [[-800, 800], [0, 600], [0, 0]]], #extrawide door angle (extrawide-to-wide)                        # 41
    [0, [0, 0, 0, 0, 1600], [[0, 0, 0, 0, 1600]], [[-800, 800], [0, 600], [0, 0]]], #extrawide door angle (extrawide-to-extrawide)                  # 42
    [1, [0, 0, 0, 0, 800], [[0, 0, 0, 0, 1600]], [[-800, 800], [0, 600], [0, 0]]], #extrawide door square (wide-to-extrawide)
    [1, [0, 0, 0, 0, 1600], [[0, 0, 0, 0, 800]], [[-800, 800], [0, 600], [0, 0]]], #extrawide door square (extrawide-to-wide)                       # 44
    [1, [0, 0, 0, 0, 1600], [[0, 0, 0, 0, 1600]], [[-800, 800], [0, 600], [0, 0]]], #extrawide door square (extrawide-to-extrawide)
    [19, [0, 0, 0, 0, 0], [[0, 0, 0, 0, 0]], [[-50, 50], [0, 600], [-50, 50]]], #small-column (46)
    [15, [0, 0, 0, 0, 0], [[0, 0, 0, 0, 0]], [[-200, 200], [0, 600], [-200, 200]]], #large-column (47)
    [13, [0, 0, 0, 0, 0], [[0, 0, 0, 0, 0]], [[-200, 200], [0, 600], [-200, 200]]], #roundsteps no rotation (48)
    [21, [0, 0, 0, 0, 0], [[0, 0, 0, 0, 0]], [[-200, 200], [0, 600], [-200, 200]]], #Round wall no rotation (49)
    [20, [0, 0, 0, 0, 0], [[0, 0, 0, 0, 0]], [[-200, 200], [0, 600], [-200, 200]]], #square wall no rotation (50)
    [9, [0, 0, 0, 0, 0], [[0, 0, 0, 0, 0]], [[-200, 200], [0, 600], [-200, 200]]], #square steps no rotation (51)
    [7, [0, 0, 0, 0, 0], [[0, 0, 0, 0, 0]], [[-200, 200], [0, 600], [-200, 200]]], #square wallTall no rotation (52)
]

# DUNGEON TILES HASH ARRAY
# Similar to the previous one but with the new name convention list like KEY
dungeon_tiles = {
    "DOOR_EW_SQUARE_Z_W-EW_"   : [0, [0, 0, 0, 0, 800], [[0, 0, 0, 0, 1600]], [[-800, 800], [0, 600], [0, 0]]], #extrawide door angle (wide-to-extrawide)
    "DOOR_EW_SQUARE_Z_EW-W_"   : [0, [0, 0, 0, 0, 1600], [[0, 0, 0, 0, 800]], [[-800, 800], [0, 600], [0, 0]]], #extrawide door angle (extrawide-to-wide)
    "DOOR_EW_SQUARE_Z_EW-EW_"  : [0, [0, 0, 0, 0, 1600], [[0, 0, 0, 0, 1600]], [[-800, 800], [0, 600], [0, 0]]], #extrawide door angle (extrawide-to-extrawide)
    "DOOR_EW_HOUSE_Z_W-EW_"    : [1, [0, 0, 0, 0, 800], [[0, 0, 0, 0, 1600]], [[-800, 800], [0, 600], [0, 0]]], #extrawide door square (wide-to-extrawide)
    "DOOR_EW_HOUSE_Z_EW-W_"    : [1, [0, 0, 0, 0, 1600], [[0, 0, 0, 0, 800]], [[-800, 800], [0, 600], [0, 0]]], #extrawide door square (extrawide-to-wide)
    "DOOR_EW_HOUSE_Z_EW-EW_"   : [1, [0, 0, 0, 0, 1600], [[0, 0, 0, 0, 1600]], [[-800, 800], [0, 600], [0, 0]]], #extrawide door square (extrawide-to-extrawide)
    "DOOR_EW_COMBI_Z_W-EW_"    : [2, [0, 0, 0, 0, 800], [[0, 0, 0, 0, 1600]], [[-800, 800], [0, 600], [0, 0]]], #extrawide door angle-wide (wide-to-extrawide)
    "DOOR_EW_COMBI_Z_EW-W_"    : [2, [0, 0, 0, 0, 1600], [[0, 0, 0, 0, 800]], [[-800, 800], [0, 600], [0, 0]]], #extrawide door angle-wide (extrawide-to-wide)
    "DOOR_EW_COMBI_Z_EW-EW_"   : [2, [0, 0, 0, 0, 1600], [[0, 0, 0, 0, 1600]], [[-800, 800], [0, 600], [0, 0]]], #extrawide door angle-wide (extrawide-to-extrawide)
    "ROOM_EW_4WAY_Z_NOT_"      : [3, [0, 0, 800, 0, 1600], [[-800, 0, -800, 90, 1600], [0, 0, -1600, 0, 1600], [800, 0, -800, -90, 1600]], [[-800, 800], [0, 600], [-800, 800]]], #extrawide corner 4
    "ROOM_EW_3WAY_L_NOT_"      : [4, [0, 0, -800, 180, 1600], [[-800, 0, -800, 90, 1600], [0, 0, -1600, 0, 1600]], [[-800, 800], [0, 600], [-800, 800]]], #extrawide corner 3 left
    "ROOM_EW_3WAY_R_NOT_"      : [4, [0, 0, 800, 0, 1600], [[0, 0, -800, 0, 1600], [800, 0, -800, -90, 1600]], [[-800, 800], [0, 600], [-800, 800]]], #extrawide corner 3 right
    "ROOM_EW_3WAY_T_NOT_"      : [4, [800, 0, 0, 90, 1600], [[-800, 0, -800, 90, 1600], [800, 0, -800, -90, 1600]], [[-800, 800], [0, 600], [-800, 800]]], #extrawide corner 3 T
    "ROOM_EW_2WAY_L_NOT_"      : [5, [800, 0, 0, 90, 1600], [[-800, 0, -800, 90, 1600]], [[-800, 800], [0, 600], [-800, 800]]], #extrawide corner left
    "ROOM_EW_2WAY_R_NOT_"      : [5, [0, 0, 800, 0, 1600], [[800, 0, -800, -90, 1600]], [[-800, 800], [0, 600], [-800, 800]]], #extrawide corner right
    "CORRIDOR_EW_1WAY_Z_NOT_"  : [6, [0, 0, 800, 0, 1600], [[0, 0, -1600, 0, 1600]], [[-800, 800], [0, 600], [-800, 800]]], #extrawide hallway
    "CORRIDOR_W_1WAY_Z_NOT_"   : [17, [0, 0, 400, 0, 800], [[0, 0, -800, 0, 800]], [[-400, 400], [0, 600], [-400, 400]]], #wide hallway
    "CORRIDOR_W_DOWN_Z_NOT_"   : [18, [0, 0, -400, 180, 800], [[0, -400, -1600, 0, 800]], [[-400, 400], [-400, 600], [-400, 1200]]], #wide ramp down
    "CORRIDOR_W_UP_Z_NOT_"     : [18, [0, -400, 1200, 0, 800], [[0, 400, -1600, 0, 800]], [[-400, 400], [-400, 600], [-400, 1200]]], #wide ramp up
    "DOOR_N_RECTANGLE_Z_NOT_"  : [24, [0, 0, 0, 0, 400], [[0, 0, 0, 0, 400]], [[-200, 200], [0, 600], [0, 0]]], #narrow door square-wide (narrow-to-narrow) 
    "DOOR_W_COMBI_Z_N-W_"      : [25, [0, 0, 0, 0, 400], [[0, 0, 0, 0, 800]], [[-400, 400], [0, 600], [0, 0]]], #wide door angle-wide (narrow-to-wide)
    "DOOR_W_COMBI_Z_W-N_"      : [25, [0, 0, 0, 0, 800], [[0, 0, 0, 0, 400]], [[-400, 400], [0, 600], [0, 0]]], #wide door angle-wide (wide-to-narrow)
    "DOOR_W_COMBI_Z_W-W_"      : [25, [0, 0, 0, 0, 800], [[0, 0, 0, 0, 800]], [[-400, 400], [0, 600], [0, 0]]], #wide door angle-wide (wide-to-wide)
    "DOOR_W_SQUARE_Z_N-W_"     : [26, [0, 0, 0, 0, 400], [[0, 0, 0, 0, 800]], [[-400, 400], [0, 600], [0, 0]]], #wide door square (narrow-to-wide)
    "DOOR_W_SQUARE_Z_W-N_"     : [26, [0, 0, 0, 0, 800], [[0, 0, 0, 0, 400]], [[-400, 400], [0, 600], [0, 0]]], #wide door square (wide-to-narrow)
    "DOOR_W_SQUARE_Z_W-W_"     : [26, [0, 0, 0, 0, 800], [[0, 0, 0, 0, 800]], [[-400, 400], [0, 600], [0, 0]]], #wide door square (wide-to-wide)
    "DOOR_N_SQUARE_Z_NOT_"     : [27, [0, 0, 0, 0, 400], [[0, 0, 0, 0, 400]], [[-200, 200], [0, 600], [0, 0]]], #narrow door square (narrow-to-narrow)
    "DOOR_N_HOUSE_Z_NOT_"      : [28, [0, 0, 0, 0, 400], [[0, 0, 0, 0, 400]], [[-200, 200], [0, 600], [0, 0]]], #narrow door angle (narrow-to-narrow)
    "DOOR_W_HOUSE_Z_N-W_"      : [29, [0, 0, 0, 0, 400], [[0, 0, 0, 0, 800]], [[-400, 400], [0, 600], [0, 0]]], #wide door angle (narrow-to-wide)
    "DOOR_W_HOUSE_Z_W-N_"      : [29, [0, 0, 0, 0, 800], [[0, 0, 0, 0, 400]], [[-400, 400], [0, 600], [0, 0]]], #wide door angle (wide-to-narrow)
    "DOOR_W_HOUSE_Z_W-W_"      : [29, [0, 0, 0, 0, 800], [[0, 0, 0, 0, 800]], [[-400, 400], [0, 600], [0, 0]]], #wide door angle (wide-to-wide)
    "CORRIDOR_W_2WAY_L_NOT_"   : [30, [400, 0, 0, 90, 800], [[-400, 0, -400, 90, 800]], [[-400, 400], [0, 600], [-400, 400]]], #wide corner left
    "CORRIDOR_W_2WAY_R_NOT_"   : [30, [0, 0, 400, 0, 800], [[400, 0, -400, -90, 800]], [[-400, 400], [0, 600], [-400, 400]]], #wide corner right
    "CORRIDOR_W_3WAY_L_NOT_"   : [31, [0, 0, -400, 180, 800], [[-400, 0, -400, 90, 800], [0, 0, -800, 0, 800]], [[-400, 400], [0, 600], [-400, 400]]], #wide corner 3 left
    "CORRIDOR_W_2WAY_R_NOT_"   : [31, [0, 0, 400, 0, 800], [[0, 0, -800, 0, 800], [400, 0, -400, -90, 800]], [[-400, 400], [0, 600], [-400, 400]]], #wide corner 3 right
    "CORRIDOR_W_3WAY_T_NOT_"   : [31, [400, 0, 0, 90, 800], [[-400, 0, -400, 90, 800], [400, 0, -400, -90, 800]], [[-400, 400], [0, 600], [-400, 400]]], #wide corner 3 T
    "CORRIDOR_W_4WAY_Z_NOT_"   : [32, [0, 0, 400, 0, 800], [[-400, 0, -400, 90, 800], [0, 0, -800, 0, 800], [400, 0, -400, -90, 800]], [[-400, 400], [0, 600], [-400, 400]]], #wide corner 4
    "CORRIDOR_N_4WAY_Z_NOT_"   : [33, [0, 0, 200, 0, 400], [[-200, 0, -200, 90, 400], [0, 0, -400, 0, 400], [200, 0, -200, -90, 400]], [[-200, 200], [0, 600], [-200, 200]]], #narrow corner 4
    "CORRIDOR_N_3WAY_L_NOT_"   : [34, [0, 0, -200, 180, 400], [[-200, 0, -200, 90, 400], [0, 0, -400, 0, 400]], [[-200, 200], [0, 600], [-200, 200]]], #narrow corner 3 left
    "CORRIDOR_N_3WAY_R_NOT_"   : [34, [0, 0, 200, 0, 400], [[0, 0, -400, 0, 400], [200, 0, -200, -90, 400]], [[-200, 200], [0, 600], [-200, 200]]], #narrow corner 3 right
    "CORRIDOR_N_3WAY_T_NOT_"   : [34, [200, 0, 0, 90, 400], [[-200, 0, -200, 90, 400], [200, 0, -200, -90, 400]], [[-200, 200], [0, 600], [-200, 200]]], #narrow corner 3 T
    "CORRIDOR_N_DOWN_Z_NOT_"   : [35, [0, 0, -400, 180, 400], [[0, -400, -1600, 0, 400]], [[-200, 200], [-400, 600], [-400, 1200]]], #narrow ramp down
    "CORRIDOR_N_UP_Z_NOT_"     : [35, [0, -400, 1200, 0, 400], [[0, 400, -1600, 0, 400]], [[-200, 200], [-400, 600], [-400, 1200]]], #narrow ramp up
    "CORRIDOR_N_1WAY_Z_NOT_"   : [36, [0, 0, 400, 0, 400], [[0, 0, -800, 0, 400]], [[-200, 200], [0, 600], [-400, 400]]], #narrow hallway
    "CORRIDOR_N_2WAY_R_NOT_"   : [37, [0, 0, 200, 0, 400], [[200, 0, -200, -90, 400]], [[-200, 200], [0, 600], [-200, 200]]], #narrow corner right
    "CORRIDOR_N_2WAY_L_NOT_"   : [37, [200, 0, 0, 90, 400], [[-200, 0, -200, 90, 400]], [[-200, 200], [0, 600], [-200, 200]]] #narrow corner left
    }




