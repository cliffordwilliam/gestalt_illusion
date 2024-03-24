# Room editor

Motivation, I think tiled and other room editor has too much feature that I do not need for my games. So I created this for a super easy json generator that has all the instance data, position and so on for you to read in your game rooms / level and have the game read it as an instruction on where it should instance the objects / entities on the level.

This manual readme is poorly written but should have all the data you need to start working with it.

This is a python project:

pygame-ce 2.4.1 (SDL 2.28.5, Python 3.12.2)

Install the package yourself before running the room_editor file.

## Room editor naming legend

| Name    | Meaning                                        |
| ------- | ---------------------------------------------- |
| TILE_S  | Tile size -> all in px unless otherwise stated |
| h       | Height                                         |
| w       | Width                                          |
| tu      | Tile unit                                      |
| w       | Width                                          |
| SPD     | Speed in px/ms                                 |
| Plurals | List                                           |
| REGIONS | Tuples[] -> [(x,y,w,h)]                        |
| I       | Index                                          |
| Len     | Lenght -> len()                                |
| I_LEN   | Lenght count from 0                            |
| APPLE_D | Dict with apple as the main importance         |
| Surf    | Surface                                        |
| Rect    | Rect / Frect                                   |
| RU      | Room unit                                      |

## Game logic

Things that moves are Frect, things that are static are Rect / Or moves in int distances

Anything that exists, enemies, cutscene trigger, trees are all either Rect / Frect

Their images are rendered with camera offset, it is rendered somewhere else

If you need debug draw just use draw lines

Fonts can be rendered on surfaces

UI exists but their images are always drawn on where their rects are

This is because UI is always on global coordinate, aka outside camera

## Game structure

4 stages

Each stage has one sprite sheet

You draw the same sprite sheet over and over again but with different region

## Stage 1 layers

| Index | Element     | OK  | Type |
| ----- | ----------- | --- | ---- |
| 0     | bg_rocks    | OK  | BG   |
| 1     | tall_bush   | OK  | BG   |
| 2     | short_bush  | OK  | BG   |
| 3     | boulders    | OK  | BG   |
| 4     | small_trees | OK  | BG   |
| 5     | wall        | OK  | BG   |
| 6     | pillar      | OK  | BG   |
| 7     | curtain     | OK  | BG   |
| 8     | furnace     | OK  | BG   |
| 9     | furniture   | OK  | BG   |
| 10    | scones      | OK  | BG   |
| 11    | thin body   | OK  | BG   |
| 12    | floor       | OK  | COL  |
| 13    | rail        | OK  | FG   |
| 14    | grass       | OK  | FG   |

Draw player between BG and FG transition later in game

Remove all the zeroes from the BG (we do not need to know collision checks for bg)

Only keep the zeroes in the COL type layer, this is the layer where actors check for collision

## Note

Room

Set item in room - region + position

Render each item in room based on their position in room index

## Working with Collision list

Collisions []

index to position tu

```py
pos_tu_x = i % ROOM_W_TU
pos_tu_y = i // ROOM_W_TU
```

position to index

```py
i = pos_tu_y * ROOM_W_TU + pos_tu_x
```

## Note

### Setup

Set the sprite sheet you want to use

Set the roop top left position in room units, down is + and right is +

Set the room scale, 1:1 or 1:2 anything

Set the total layers, 1 layer for 1 type of thing

This editor creates rooms, rooms are multiple of the screen native size

So the smallest room cannot be smaller than the native size screen

Room sizes are fully divisible by 1 room, there cannot be decimal scaling

You can set the tile size too

Tile size determine the screen native size, screen size is always 20 by 11 tiles. You can change this but I think this is a good aspect ratio

Game resolution scalling can also be set at the start

### Room unit

1 Room unit, 1 x_ru = 20 x_tu

Where 1 tu is 16

1 y_ru = 11 y_tu

### xds

The x coordinate, in draw position, snapped to tile

So the values are where the tile is on screen not in the real world

Snapped means it is always snapped to the grid

### Sprite classes

These are instanced when you draw

They have the following properties that will be saved to json

```py
self.name = "floor"
self.xds = 0
self.yds = 0
self.layer_i = 13
self.regions = {}
self.region = self.regions[0]
self.icon_region = (368, 48, 16, 16)
```

Things that have bitmask autotiling feature will have their regions be a dict of the bits keys and regions values like so:

This is a blob style bitmask, from top left to the right ordered

```py
self.regions = {
    208: (320, 0, 16, 16),
    248: (336, 0, 16, 16),
    104: (352, 0, 16, 16),
    64: (368, 0, 16, 16),
    80: (384, 0, 16, 16),
    120: (400, 0, 16, 16),
    216: (416, 0, 16, 16),
    72: (432, 0, 16, 16),
    88: (448, 0, 16, 16),
    219: (464, 0, 16, 16),

    214: (320, 16, 16, 16),
    255: (336, 16, 16, 16),
    107: (352, 16, 16, 16),
    66: (368, 16, 16, 16),
    86: (384, 16, 16, 16),
    127: (400, 16, 16, 16),
    223: (416, 16, 16, 16),
    75: (432, 16, 16, 16),
    95: (448, 16, 16, 16),
    126: (464, 16, 16, 16),

    22: (320, 32, 16, 16),
    31: (336, 32, 16, 16),
    11: (352, 32, 16, 16),
    2: (368, 32, 16, 16),
    210: (384, 32, 16, 16),
    251: (400, 32, 16, 16),
    254: (416, 32, 16, 16),
    106: (432, 32, 16, 16),
    250: (448, 32, 16, 16),
    218: (464, 32, 16, 16),
    122: (480, 32, 16, 16),

    16: (320, 48, 16, 16),
    24: (336, 48, 16, 16),
    8: (352, 48, 16, 16),
    0: (368, 48, 16, 16),
    18: (384, 48, 16, 16),
    27: (400, 48, 16, 16),
    30: (416, 48, 16, 16),
    10: (432, 48, 16, 16),
    26: (448, 48, 16, 16),
    94: (464, 48, 16, 16),
    91: (480, 48, 16, 16),

    82: (384, 64, 16, 16),
    123: (400, 64, 16, 16),
    222: (416, 64, 16, 16),
    74: (432, 64, 16, 16),
    90: (448, 64, 16, 16),
}
```

Otherwise they look like this:

```py
self.region = (320, 240, 176, 32)

# or this

self.regions = [(320, 240, 176, 32), (320, 240, 176, 32)]
```

This is because if it is not a bitmask then I will use the list index as the frame index, there is no need to create a dict with numbered keys, a list does that already

Names are used to indicate in json later what obj this is to instance

Also for the editor to check if it is an autotile or not. I could have added another property to all of the class to check if it is a bitmask or not but since most tiles are not autotile I'll just create a list to store the names of the autotile tiles instead.

Layer is the layer index, determine which layer this will be in, higher layer are drawn on top

Finally there is the icon region, this is the region where the editor will display it as icon on the menu screen

The xds and yds are where the tiles are in the real world, used for instancing later

Why is it called xds and yds? I got confused keeping track of unit transitions and I ended up with a naming convention that leads to that. There must be an error in how I think because that is supposed to be just x and y

Each sprite class has a duplicate function, this is used when the user draw. Drawing means duplicating the instance that you have selected and adding it to the layer list

To render the added tiles, the editor will loop over all of the layers and draw the instances. It is not efficient as of now as it loops over all of the layer items even if it has nothing in there. But then how big is your game room anyways it should be okay. A solution is to store the tiles in another list. So the editor will only have to loop over this, loop over the list of tiles that exist. But then deleting should be slow then? Need to delete certain item in a list in certain position is not the fastest thing. But then you draw more often than deleting anyways so I'll think about this.

Each loop calls the sprite instance update method. This is so that each class can have a unique update method. Maybe play animation or offset image to create a hover effect.

Each sprite draw themselves with the camera offset taken into consideration

## Maths cheatsheet

### Legends

Here are the naming convention that I came with

tu - 1 2 3 -> these are refering to tiles, so 1 is 16px and 2 is 32px

Based on tile sizes

x and y -> These are global positions on the screen, so top left is always 0, 0 and so on

xs -> this is the global but snapped, meaning the numbers are always be like this 0 16 32

xd_tu -> d means it has a drawing offset, the the tu is explained above, so you can combine the names

xds -> means that the position is on drawing offset but is snapped to 0 16 32

Thats all I think

### Turn i from collision list to real coords?

Say you have an index, but you want it to be turned into coordinate? Knowing that the index comes from a list that represents the room coordinates

```py
for i in range(SPRITES_LEN):
    sprite = SPRITES[i]
    x_tu = i % NATIVE_W_TU
    y_tu = i // NATIVE_W_TU
    x = x_tu * TILE_S
    y = y_tu * TILE_S
    MENU_COLLISIONS[i] = sprite
    MENU_SURF.blit(SPRITE_SHEET_SURF, (x, y), (sprite.icon_region))
```

You get 1 index, then:

```py
    x_tu = i % NATIVE_W_TU
    y_tu = i // NATIVE_W_TU
```

Then there you have the x and y in tile units
From where you can get the x and y in the real world

### Real coord to draw pos?

```py
    xs = xds - CAM_RECT.x
    ys = yds - CAM_RECT.y
    NATIVE_SURF.blit(LIGHT_SURF, (xs, ys), (0, 0, TILE_S, TILE_S))
```

### Interacting with collision list?

use x_tu and y_tu

Check something is inside the room and get item

```py
if (0 <= neighbour_x_tu < ROOM_W_TU) and (0 <= neighbour_y_tu < ROOM_H_TU):
            neighbour = selected_layer[neighbour_y_tu *
                                       ROOM_W_TU + neighbour_x_tu]
```

Always use the tu to get or set the collision list

```py
sprite = selected_layer[y_tu * ROOM_W_TU + x_tu]
```

### Turning tu into xd_tu and then xds

Meaning you have to turn it to draw pos, then to real pos

```py
neighbour_xd_tu = neighbour_x_tu + ROOM_X_TU
neighbour_yd_tu = neighbour_y_tu + ROOM_Y_TU
neighbour_xds = neighbour_xd_tu * TILE_S
neighbour_yds = neighbour_yd_tu * TILE_S

new_sprite = selected_sprite.duplicate()
new_sprite.xds = neighbour_xds
new_sprite.yds = neighbour_yds
selected_layer[neighbour_y_tu *
                ROOM_W_TU + neighbour_x_tu] = new_sprite
```

### Real global position to tu?

```py
pos = pg.mouse.get_pos()
x = pos[0] // RESOLUTION
y = pos[1] // RESOLUTION
x_tu = x // TILE_S
y_tu = y // TILE_S
xs = x_tu * TILE_S
ys = y_tu * TILE_S
cell = MENU_COLLISIONS[y_tu * NATIVE_W_TU + x_tu]
if cell != 0:
    NATIVE_SURF.blit(LIGHT_SURF, (xs, ys), (0, 0, TILE_S, TILE_S))
```

Get the scaled pos first, then make it into a snapped real position and tile unit real position

Use x_tu to get something or xs to draw to screen

## Drawing grids

Loop over a range of lines

Then just modulo it to make it loop over a range of number

```py
for i in range(NATIVE_W_TU):
    offset = TILE_S * i
    xd = (offset - CAM_RECT.x) % NATIVE_W
    yd = (offset - CAM_RECT.y) % NATIVE_H
    pg.draw.line(NATIVE_SURF, "grey4", (xd, 0), (xd, NATIVE_H))
    pg.draw.line(NATIVE_SURF, "grey4", (0, yd), (NATIVE_W, yd))
xd = -CAM_RECT.x % NATIVE_W
yd = -CAM_RECT.y % NATIVE_H
pg.draw.line(NATIVE_SURF, "grey8", (xd, 0), (xd, NATIVE_H))
pg.draw.line(NATIVE_SURF, "grey8", (0, yd), (NATIVE_W, yd))
```

### Render cursor on grid

```py
pos = pg.mouse.get_pos()
x = pos[0] // RESOLUTION
y = pos[1] // RESOLUTION
xd = x + CAM_RECT.x
yd = y + CAM_RECT.y
xd_tu = xd // TILE_S
yd_tu = yd // TILE_S
xds = xd_tu * TILE_S
yds = yd_tu * TILE_S
# Remove room offset to be collision index
x_tu = xd_tu - ROOM_X_TU
y_tu = yd_tu - ROOM_Y_TU
# Cursor position global pos
xs = xds - CAM_RECT.x
ys = yds - CAM_RECT.y
r = xs + TILE_S
b = ys + TILE_S
pg.draw.lines(NATIVE_SURF, "grey12", True, [
                (xs, ys), (r, ys), (r, ys), (r, b), (r, b), (xs, b)], 1)
```

This is quire confusing but it goes something like this

Get the global mouse pos first

Then turn it into draw offset position (if its a mouse then I want to add cam offset? why though)

Then turn that draw position into tile units, 1 2 and so on

Multiply that to get the snap draw positon to the grid, 16 32 and so on

You can turn the tile unit into index, by removing the room topleft offset

Use the snap draw position to draw the cursor, add the camera offset too

## Render room number

```py
FONT.render_to(
    NATIVE_SURF, (xd + FONT_W, yd + FONT_H), f"{
        (CAM_RECT.x - 1) // NATIVE_W + 1}{
        (CAM_RECT.y - 1) // NATIVE_H + 1}", "grey100"
)
```

I am not sure why but I have to and and minus the number like so in order for them to display the room num correctly. Otherwise when the camera is flushed to the most left of the room, it will show the prev room number to its other left and not the one right now.

## Turning xs to xds to xd_tu and then x_tu

This is when you have a snap real position 16 32

And you want to turn it to draw, draw tu and then just tu

```py
tl_xs = top_left[0]
tl_xds = tl_xs + CAM_RECT.x
tl_xd_tu = tl_xds // TILE_S
# Remove room offset to be collision index
tl_x_tu = tl_xd_tu - ROOM_X_TU
```

Use tu to talk with collision list

```py
item = selected_layer[y_tu * ROOM_W_TU + x_tu]
```
