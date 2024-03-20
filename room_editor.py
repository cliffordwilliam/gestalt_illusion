import pygame as pg
import pygame.freetype as font
from sys import exit

pg.init()

# Constants
TILE_S = 16
FONT_H = 5
FONT_W = 3
FONT = font.Font("cg_pixel_3x5_mono.ttf", FONT_H)
EVENTS = [pg.KEYDOWN, pg.KEYUP, pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.QUIT]
FPS = 30
CLOCK = pg.time.Clock()
NATIVE_W = 320
NATIVE_H = 176
NATIVE_W_TILE_UNIT = NATIVE_W // TILE_S
NATIVE_H_TILE_UNIT = NATIVE_H // TILE_S
NATIVE_SURF = pg.Surface((NATIVE_W, NATIVE_H))
RESOLUTION = 5
WINDOW_W = NATIVE_W * RESOLUTION
WINDOW_H = NATIVE_H * RESOLUTION
WINDOW_SURF = pg.display.set_mode((WINDOW_W, WINDOW_H))
ORIGIN_SURF = pg.Surface((1, 1))
ORIGIN_SURF.fill("red")
V_SURF = pg.Surface((1, NATIVE_H))
V_SURF.fill("grey12")
H_SURF = pg.Surface((NATIVE_W, 1))
H_SURF.fill("grey12")
S_V_SURF = pg.Surface((1, NATIVE_H))
S_V_SURF.fill("grey16")
S_H_SURF = pg.Surface((NATIVE_W, 1))
S_H_SURF.fill("grey16")
CAM_RECT = pg.FRect(0, 0, NATIVE_W, NATIVE_H)
CAM_SPD = 0.09
CAM_LERP_FACTOR = 0.2
HIGHLIGHT_TILE_SURFACE = pg.Surface((TILE_S, TILE_S))
HIGHLIGHT_TILE_SURFACE.fill("grey100")
HIGHLIGHT_TILE_SURFACE.set_alpha(122)
CURSOR_RECT = pg.FRect(0, 0, TILE_S, TILE_S)

# Bitmasks
BITMASK_REGION_DICT = {
    "floor": {
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
    },
    "rock": {
        208: (320, 80, 16, 16),
        248: (336, 80, 16, 16),
        104: (352, 80, 16, 16),
        64: (368, 80, 16, 16),
        80: (384, 80, 16, 16),
        120: (400, 80, 16, 16),
        216: (416, 80, 16, 16),
        72: (432, 80, 16, 16),
        88: (448, 80, 16, 16),
        219: (464, 80, 16, 16),

        214: (320, 96, 16, 16),
        255: (336, 96, 16, 16),
        107: (352, 96, 16, 16),
        66: (368, 96, 16, 16),
        86: (384, 96, 16, 16),
        127: (400, 96, 16, 16),
        223: (416, 96, 16, 16),
        75: (432, 96, 16, 16),
        95: (448, 96, 16, 16),
        126: (464, 96, 16, 16),

        22: (320, 112, 16, 16),
        31: (336, 112, 16, 16),
        11: (352, 112, 16, 16),
        2: (368, 112, 16, 16),
        210: (384, 112, 16, 16),
        251: (400, 112, 16, 16),
        254: (416, 112, 16, 16),
        106: (432, 112, 16, 16),
        250: (448, 112, 16, 16),
        218: (464, 112, 16, 16),
        122: (480, 112, 16, 16),

        16: (320, 128, 16, 16),
        24: (336, 128, 16, 16),
        8: (352, 128, 16, 16),
        0: (368, 128, 16, 16),
        18: (384, 128, 16, 16),
        27: (400, 128, 16, 16),
        30: (416, 128, 16, 16),
        10: (432, 128, 16, 16),
        26: (448, 128, 16, 16),
        94: (464, 128, 16, 16),
        91: (480, 128, 16, 16),

        82: (384, 144, 16, 16),
        123: (400, 144, 16, 16),
        222: (416, 144, 16, 16),
        74: (432, 144, 16, 16),
        90: (448, 144, 16, 16),
    },
    "bg_rock": {
        208: (320, 160, 16, 16),
        248: (336, 160, 16, 16),
        104: (352, 160, 16, 16),
        64: (368, 160, 16, 16),
        80: (384, 160, 16, 16),
        120: (400, 160, 16, 16),
        216: (416, 160, 16, 16),
        72: (432, 160, 16, 16),
        88: (448, 160, 16, 16),
        219: (464, 160, 16, 16),

        214: (320, 176, 16, 16),
        255: (336, 176, 16, 16),
        107: (352, 176, 16, 16),
        66: (368, 176, 16, 16),
        86: (384, 176, 16, 16),
        127: (400, 176, 16, 16),
        223: (416, 176, 16, 16),
        75: (432, 176, 16, 16),
        95: (448, 176, 16, 16),
        126: (464, 176, 16, 16),

        22: (320, 192, 16, 16),
        31: (336, 192, 16, 16),
        11: (352, 192, 16, 16),
        2: (368, 192, 16, 16),
        210: (384, 192, 16, 16),
        251: (400, 192, 16, 16),
        254: (416, 192, 16, 16),
        106: (432, 192, 16, 16),
        250: (448, 192, 16, 16),
        218: (464, 192, 16, 16),
        122: (480, 192, 16, 16),

        16: (320, 208, 16, 16),
        24: (336, 208, 16, 16),
        8: (352, 208, 16, 16),
        0: (368, 208, 16, 16),
        18: (384, 208, 16, 16),
        27: (400, 208, 16, 16),
        30: (416, 208, 16, 16),
        10: (432, 208, 16, 16),
        26: (448, 208, 16, 16),
        94: (464, 208, 16, 16),
        91: (480, 208, 16, 16),

        82: (384, 224, 16, 16),
        123: (400, 224, 16, 16),
        222: (416, 224, 16, 16),
        74: (432, 224, 16, 16),
        90: (448, 224, 16, 16),
    }
}

# Sprite sheet setting
SPRITE_SHEET_PNG_NAME = "stage_1_sprite_sheet.png"
SPRITE_SHEET_SURF = pg.image.load(SPRITE_SHEET_PNG_NAME).convert_alpha()
CURSOR_SPRITE_SHEET_SURF = pg.image.load(SPRITE_SHEET_PNG_NAME).convert_alpha()
CURSOR_SPRITE_SHEET_SURF.set_alpha(122)
collision = [0 for _ in range(NATIVE_W_TILE_UNIT * NATIVE_H_TILE_UNIT)]

# Page 1
PAGE_1_SURF = pg.Surface((NATIVE_W, NATIVE_H))
PAGE_1_SURF.blits([
    (SPRITE_SHEET_SURF, (TILE_S, TILE_S), (368, 48, TILE_S, TILE_S)),
    (SPRITE_SHEET_SURF, (2 * TILE_S, TILE_S), (368, 128, TILE_S, TILE_S)),
])
PAGE_1_COLLISION = collision.copy()
PAGE_1_COLLISION[1 * NATIVE_W_TILE_UNIT +
                 1] = {"name": "floor", "region": (368, 48, TILE_S, TILE_S), "room": 11}
PAGE_1_COLLISION[1 * NATIVE_W_TILE_UNIT +
                 2] = {"name": "rock", "region": (368, 128, TILE_S, TILE_S), "room": 11}

# Page 2
PAGE_2_SURF = pg.Surface((NATIVE_W, NATIVE_H))
PAGE_2_SURF.blits([
    (SPRITE_SHEET_SURF, (TILE_S, TILE_S), (368, 208, TILE_S, TILE_S)),
    (SPRITE_SHEET_SURF, (2 * TILE_S, TILE_S), (320, 240, TILE_S, TILE_S)),
])
PAGE_2_COLLISION = collision.copy()
PAGE_2_COLLISION[1 * NATIVE_W_TILE_UNIT +
                 1] = {"name": "bg_rock", "region": (368, 208, TILE_S, TILE_S), "room": 0}
PAGE_2_COLLISION[1 * NATIVE_W_TILE_UNIT +
                 2] = {"name": "tall_bush", "region": (320, 240, 11 * TILE_S, 2 * TILE_S), "room": 1}

# Pages
PAGE_SURFS = [
    PAGE_1_SURF,
    PAGE_2_SURF
]
PAGES_INDEX_LEN = len(PAGE_SURFS) - 1
PAGE_COLLISIONS = [
    PAGE_1_COLLISION,
    PAGE_2_COLLISION
]

# Room setting
ROOM_TL_ROOM_UNIT = (0, 0)
ROOM_SCALE = (1, 1)
ROOM_W_TILE_UNIT = NATIVE_W_TILE_UNIT * ROOM_SCALE[0]
ROOM_H_TILE_UNIT = NATIVE_H_TILE_UNIT * ROOM_SCALE[1]
ROOM_X_TILE_UNIT = ROOM_TL_ROOM_UNIT[0] * NATIVE_W_TILE_UNIT
ROOM_Y_TILE_UNIT = ROOM_TL_ROOM_UNIT[1] * NATIVE_H_TILE_UNIT
ROOM_X = ROOM_X_TILE_UNIT * TILE_S
ROOM_Y = ROOM_Y_TILE_UNIT * TILE_S
ROOM_W = ROOM_W_TILE_UNIT * TILE_S
ROOM_H = ROOM_H_TILE_UNIT * TILE_S
ROOM_RECT = pg.FRect(
    ROOM_X,
    ROOM_Y,
    ROOM_W,
    ROOM_H
)
ROOM_SURF = pg.Surface((ROOM_W, ROOM_H))
ROOM_SURF.fill("grey4")
CAM_RECT.topleft = (ROOM_X, ROOM_Y)
room = [0 for _ in range(ROOM_W_TILE_UNIT * ROOM_H_TILE_UNIT)]
ROOMS_LIST = [
    room.copy(),  # 0 - bg_rocks
    room.copy(),  # 1 - tall_bush
    room.copy(),  # 2 - short_bush
    room.copy(),  # 3 - boulders
    room.copy(),  # 4 - small_trees
    room.copy(),  # 5 - wall
    room.copy(),  # 6 - pillar
    room.copy(),  # 7 - blinder
    room.copy(),  # 8 - scones
    room.copy(),  # 9 - thin
    room.copy(),  # 10 - balcony
    room.copy(),  # 11 - floor
    room.copy(),  # 12 - grass
    room.copy(),  # 13 - water
]
selected_room = ROOMS_LIST[11]

# Menu
is_menu = False
selected_name = "floor"
selected_region = (368, 48, TILE_S, TILE_S)
page_index = 0
selected_page_surface = PAGE_SURFS[page_index]
selected_page_collision = PAGE_COLLISIONS[page_index]
selected_bitmask_region = BITMASK_REGION_DICT[selected_name]

# Input
is_w_pressed = 0
is_a_pressed = 0
is_s_pressed = 0
is_d_pressed = 0
is_lmb_pressed = False
is_rmb_pressed = False
is_mmb_pressed = False
is_shift_pressed = False

# Draw rect
start_pos = (0, 0)
end_pos = (0, 0)

# Cam
cam_dir = pg.math.Vector2(0, 0)
cam_vel = pg.math.Vector2(0, 0)


def fill(position_tile_unit, draw_position, l=0, t=0, r=ROOM_W_TILE_UNIT, b=ROOM_H_TILE_UNIT):
    # Create a blink effect on tile that mask about to change
    NATIVE_SURF.blit(HIGHLIGHT_TILE_SURFACE,
                     (draw_position[0] - CAM_RECT.x, draw_position[1] - CAM_RECT.y))

    x = position_tile_unit[0]
    y = position_tile_unit[1]
    neighbour_pos_tile_units = [
        (x - 0, y - 1),
        (x - 1, y - 0),                 (x + 1, y - 0), (x - 0, y + 1)
    ]
    for pos in neighbour_pos_tile_units:
        # Get tile from map
        neighbour_pos_tile_unit_x = pos[0]
        neighbour_pos_tile_unit_y = pos[1]
        if (l <= neighbour_pos_tile_unit_x < r) and (t <= neighbour_pos_tile_unit_y < b):
            neighbour = selected_room[
                neighbour_pos_tile_unit_y * ROOM_W_TILE_UNIT + neighbour_pos_tile_unit_x]

            # Air?
            if neighbour == 0:
                # Fill
                neighbour_draw_pos_x = (
                    neighbour_pos_tile_unit_x + ROOM_X_TILE_UNIT) * TILE_S
                neighbour_draw_pos_y = (
                    neighbour_pos_tile_unit_y + ROOM_Y_TILE_UNIT) * TILE_S
                selected_room[neighbour_pos_tile_unit_y * NATIVE_W_TILE_UNIT + neighbour_pos_tile_unit_x] = {"pos": (
                    neighbour_draw_pos_x, neighbour_draw_pos_y), "region": selected_region, "name": selected_name}
                fill(
                    (neighbour_pos_tile_unit_x, neighbour_pos_tile_unit_y),
                    (neighbour_draw_pos_x, neighbour_draw_pos_y), l, t, r, b
                )
                if selected_name in ["floor", "rock", "bg_rock"]:
                    update_bitmasks(
                        (neighbour_pos_tile_unit_x, neighbour_pos_tile_unit_y), (neighbour_draw_pos_x, neighbour_draw_pos_y))


def update_bitmasks(position_tile_unit, draw_position, last=False):
    # Create a blink effect on tile that mask about to change
    NATIVE_SURF.blit(HIGHLIGHT_TILE_SURFACE,
                     (draw_position[0] - CAM_RECT.x, draw_position[1] - CAM_RECT.y))

    # Raw bits
    br, b, bl, r, l, tr, t, tl = 0, 0, 0, 0, 0, 0, 0, 0

    x = position_tile_unit[0]
    y = position_tile_unit[1]
    neighbour_pos_tile_units = [
        (x - 1, y - 1), (x - 0, y - 1), (x + 1, y - 1),
        (x - 1, y - 0),                 (x + 1, y - 0),
        (x - 1, y + 1), (x - 0, y + 1), (x + 1, y + 1)
    ]
    for pos in neighbour_pos_tile_units:
        # Get tile from map
        neighbour_pos_tile_unit_x = pos[0]
        neighbour_pos_tile_unit_y = pos[1]
        if (0 <= neighbour_pos_tile_unit_x < ROOM_W_TILE_UNIT) and (0 <= neighbour_pos_tile_unit_y < ROOM_H_TILE_UNIT):
            neighbour = selected_room[
                neighbour_pos_tile_unit_y * ROOM_W_TILE_UNIT + neighbour_pos_tile_unit_x]

            # Air? check other position
            if neighbour == 0:
                continue

            # Found neighbour
            neighbour_draw_pos = neighbour["pos"]

            # Tell my neighbour to update their frame index
            if last == False:
                update_bitmasks(
                    (neighbour_pos_tile_unit_x, neighbour_pos_tile_unit_y),
                    (neighbour_draw_pos[0], neighbour_draw_pos[1]),
                    last=True
                )

            dx = neighbour_pos_tile_unit_x - x
            dy = neighbour_pos_tile_unit_y - y
            t += dx == 0 and dy == -1
            r += dx == 1 and dy == 0
            b += dx == 0 and dy == 1
            l += dx == -1 and dy == 0
            br += dx == 1 and dy == 1
            bl += dx == -1 and dy == 1
            tr += dx == 1 and dy == -1
            tl += dx == -1 and dy == -1
    tr = tr and t and r
    tl = tl and t and l
    br = br and b and r
    bl = bl and b and l
    mask_id = (br << 7) | (b << 6) | (bl << 5) | (
        r << 4) | (l << 3) | (tr << 2) | (t << 1) | tl

    # Update region of this tile position with cooked bitmask
    tile = selected_room[y * ROOM_W_TILE_UNIT + x]

    # In case this tile is from deleted
    if tile != 0:
        new_region = BITMASK_REGION_DICT[tile["name"]][mask_id]
        selected_room[y * NATIVE_W_TILE_UNIT +
                      x] = {"pos": draw_position, "region": new_region, "name": tile["name"]}


# Main loop
while 1:
    # Dt
    dt = CLOCK.tick(FPS)

    # Get event
    for event in pg.event.get(EVENTS):
        # Window quit
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        # Key down
        if event.type == pg.KEYDOWN:
            # Normal state
            if not is_menu:
                # For cam movement input
                if event.key == pg.K_w:
                    is_w_pressed = 1
                if event.key == pg.K_a:
                    is_a_pressed = 1
                if event.key == pg.K_s:
                    is_s_pressed = 1
                if event.key == pg.K_d:
                    is_d_pressed = 1
                # Open menu
                if event.key == pg.K_SPACE:
                    is_menu = True
                # Rect draw mode
                if event.key == pg.K_LSHIFT:
                    is_shift_pressed = True
                    pos = pg.mouse.get_pos()
                    pos_x = pos[0] // RESOLUTION
                    pos_y = pos[1] // RESOLUTION
                    draw_pos_tile_x = (pos_x + int(CAM_RECT.x)) // TILE_S
                    draw_pos_tile_y = (pos_y + int(CAM_RECT.y)) // TILE_S
                    draw_pos_x = draw_pos_tile_x * TILE_S
                    draw_pos_y = draw_pos_tile_y * TILE_S
                    x = draw_pos_tile_x - ROOM_X_TILE_UNIT
                    y = draw_pos_tile_y - ROOM_Y_TILE_UNIT
                    # Only render when it is in room
                    if (0 <= x < ROOM_W_TILE_UNIT) and (0 <= y < ROOM_H_TILE_UNIT):
                        start_pos = (draw_pos_x, draw_pos_y)

            # Menu state
            else:
                # Cycle pages
                direction = int(event.key == pg.K_d) - int(event.key == pg.K_a)
                page_index += direction
                page_index = max(0, min(page_index, PAGES_INDEX_LEN))
                selected_page_surface = PAGE_SURFS[page_index]
                selected_page_collision = PAGE_COLLISIONS[page_index]
                # Close menu
                if event.key == pg.K_SPACE:
                    is_menu = False

        # Key up
        elif event.type == pg.KEYUP:
            # Normal state
            if not is_menu:
                # For cam movement input
                if event.key == pg.K_w:
                    is_w_pressed = 0
                if event.key == pg.K_a:
                    is_a_pressed = 0
                if event.key == pg.K_s:
                    is_s_pressed = 0
                if event.key == pg.K_d:
                    is_d_pressed = 0
                # Draw rect
                if event.key == pg.K_LSHIFT:
                    is_shift_pressed = False
                    start_draw_pos_tile_x, start_draw_pos_tile_y = start_pos[
                        0] // TILE_S, start_pos[1] // TILE_S
                    end_draw_pos_tile_x, end_draw_pos_tile_y = end_pos[0] // TILE_S, end_pos[1] // TILE_S
                    x, y = start_draw_pos_tile_x - \
                        ROOM_X_TILE_UNIT, start_draw_pos_tile_y - ROOM_Y_TILE_UNIT
                    x2, y2 = end_draw_pos_tile_x - \
                        ROOM_X_TILE_UNIT, end_draw_pos_tile_y - ROOM_Y_TILE_UNIT
                    l, t = min(x, x2), min(y, y2)
                    r, b = max(x, x2), max(y, y2)
                    selected_room[y * NATIVE_W_TILE_UNIT + x] = {
                        "pos": (start_draw_pos_tile_x * TILE_S, start_draw_pos_tile_y * TILE_S),
                        "region": selected_region,
                        "name": selected_name
                    }
                    fill((start_draw_pos_tile_x, start_draw_pos_tile_y),
                         (start_pos[0], start_pos[1]), l, t, r + 1, b + 1)
                    start_pos = end_pos = (0, 0)

        # Mouse down
        if event.type == pg.MOUSEBUTTONDOWN:
            # Normal state
            if not is_menu:
                # For drawing
                if event.button == 1:
                    is_lmb_pressed = True
                if event.button == 2:
                    is_mmb_pressed = True
                if event.button == 3:
                    is_rmb_pressed = True

        # Mouse up
        elif event.type == pg.MOUSEBUTTONUP:
            # Normal state
            if not is_menu:
                # For drawing
                if event.button == 1:
                    is_lmb_pressed = False
                if event.button == 2:
                    is_mmb_pressed = False
                if event.button == 3:
                    is_rmb_pressed = False

            # Menu state
            else:
                # Select menu item
                pos = pg.mouse.get_pos()
                pos_x = pos[0] // RESOLUTION
                pos_y = pos[1] // RESOLUTION
                pos_tile_x = pos_x // TILE_S
                pos_tile_y = pos_y // TILE_S
                item = selected_page_collision[pos_tile_y *
                                               NATIVE_W_TILE_UNIT + pos_tile_x]
                if item != 0:
                    selected_name = item["name"]
                    selected_region = item["region"]
                    selected_room = ROOMS_LIST[item["room"]]
                    if selected_name in ["floor", "rock", "bg_rock"]:
                        selected_bitmask_region = BITMASK_REGION_DICT[selected_name]
                    is_menu = False

    # Menu state
    if is_menu:
        # Clear
        NATIVE_SURF.fill("grey0")

        # Draw selected page
        NATIVE_SURF.blit(selected_page_surface, (0, 0))

        # Draw hover cursor
        pos = pg.mouse.get_pos()
        pos_x = pos[0] // RESOLUTION
        pos_y = pos[1] // RESOLUTION
        pos_tile_x = pos_x // TILE_S
        pos_tile_y = pos_y // TILE_S
        pos_tile_snap_x = pos_tile_x * TILE_S
        pos_tile_snap_y = pos_tile_y * TILE_S
        item = selected_page_collision[pos_tile_y *
                                       NATIVE_W_TILE_UNIT + pos_tile_x]
        if item != 0:
            NATIVE_SURF.blit(HIGHLIGHT_TILE_SURFACE,
                             (pos_tile_snap_x, pos_tile_snap_y))

    # Normal state
    else:
        # Clear
        NATIVE_SURF.fill("grey12")

        # Draw room
        room_draw_pos_x = ROOM_RECT.x - CAM_RECT.x
        room_draw_pos_y = ROOM_RECT.y - CAM_RECT.y
        NATIVE_SURF.blit(ROOM_SURF, (room_draw_pos_x, room_draw_pos_y))

        # Draw grid
        for i in range(NATIVE_W_TILE_UNIT):
            offset = TILE_S * i
            x = (-CAM_RECT.x + (offset)) % NATIVE_W
            y = (-CAM_RECT.y + (offset)) % NATIVE_H
            NATIVE_SURF.blits([(V_SURF, (x, 0)), (H_SURF, (0, y))])
        x = -CAM_RECT.x % NATIVE_W
        y = -CAM_RECT.y % NATIVE_H
        NATIVE_SURF.blits([(S_V_SURF, (x, 0)), (S_H_SURF, (0, y))])
        FONT.render_to(
            NATIVE_SURF, (x, FONT_H), f"{
                CAM_RECT.x // NATIVE_W + 1}", "grey100"
        )
        FONT.render_to(
            NATIVE_SURF, (FONT_W, y), f"{
                CAM_RECT.y // NATIVE_H + 1}", "grey100"
        )
        NATIVE_SURF.blit(
            ORIGIN_SURF, (-CAM_RECT.x, -CAM_RECT.y)
        )

        # Draw sprite
        for room in ROOMS_LIST:
            for item in room:
                if item != 0:
                    pos = item["pos"]
                    region = item["region"]
                    w, h = region[2], region[3]
                    x, y = pos
                    # Only render when it is in camera
                    if (CAM_RECT.x - w <= x < CAM_RECT.right) and (CAM_RECT.y - h <= y < CAM_RECT.bottom):
                        tile_draw_pos_x = x - CAM_RECT.x
                        tile_draw_pos_y = y - CAM_RECT.y
                        NATIVE_SURF.blit(
                            SPRITE_SHEET_SURF, (tile_draw_pos_x, tile_draw_pos_y), region)

        # Rect draw mode
        if is_shift_pressed:
            pos = pg.mouse.get_pos()
            pos_x = pos[0] // RESOLUTION
            pos_y = pos[1] // RESOLUTION
            draw_pos_tile_x = (pos_x + int(CAM_RECT.x)) // TILE_S
            draw_pos_tile_y = (pos_y + int(CAM_RECT.y)) // TILE_S
            draw_pos_x = draw_pos_tile_x * TILE_S
            draw_pos_y = draw_pos_tile_y * TILE_S
            x = draw_pos_tile_x - ROOM_X_TILE_UNIT
            y = draw_pos_tile_y - ROOM_Y_TILE_UNIT
            # Only render when it is in room
            if (0 <= x < ROOM_W_TILE_UNIT) and (0 <= y < ROOM_H_TILE_UNIT):
                start_draw_pos_x = start_pos[0] - CAM_RECT.x
                start_draw_pos_y = start_pos[1] - CAM_RECT.y
                end_pos = (draw_pos_x, draw_pos_y)
                end_draw_pos_x = draw_pos_x - CAM_RECT.x
                end_draw_pos_y = draw_pos_y - CAM_RECT.y
                if start_draw_pos_x < end_draw_pos_x:
                    end_draw_pos_x += TILE_S
                else:
                    start_draw_pos_x += TILE_S
                if start_draw_pos_y < end_draw_pos_y:
                    end_draw_pos_y += TILE_S
                else:
                    start_draw_pos_y += TILE_S
                pg.draw.line(NATIVE_SURF, "red", (start_draw_pos_x,
                             start_draw_pos_y), (end_draw_pos_x, start_draw_pos_y))
                pg.draw.line(NATIVE_SURF, "red", (start_draw_pos_x,
                             start_draw_pos_y), (start_draw_pos_x, end_draw_pos_y))
                pg.draw.line(NATIVE_SURF, "red", (end_draw_pos_x,
                             end_draw_pos_y), (start_draw_pos_x, end_draw_pos_y))
                pg.draw.line(NATIVE_SURF, "red", (end_draw_pos_x,
                             end_draw_pos_y), (end_draw_pos_x, start_draw_pos_y))

        # Normal draw mode
        else:
            # Draw cursor
            pos = pg.mouse.get_pos()
            pos_x = pos[0] // RESOLUTION
            pos_y = pos[1] // RESOLUTION
            draw_pos_tile_x = (pos_x + int(CAM_RECT.x)) // TILE_S
            draw_pos_tile_y = (pos_y + int(CAM_RECT.y)) // TILE_S
            draw_pos_x = draw_pos_tile_x * TILE_S
            draw_pos_y = draw_pos_tile_y * TILE_S
            x = draw_pos_tile_x - ROOM_X_TILE_UNIT
            y = draw_pos_tile_y - ROOM_Y_TILE_UNIT
            # Only render when it is in room
            if (0 <= x < ROOM_W_TILE_UNIT) and (0 <= y < ROOM_H_TILE_UNIT):
                cursor_draw_pos_x = draw_pos_x - CAM_RECT.x
                cursor_draw_pos_y = draw_pos_y - CAM_RECT.y
                NATIVE_SURF.blit(CURSOR_SPRITE_SHEET_SURF,
                                 (cursor_draw_pos_x, cursor_draw_pos_y), selected_region)

            # Draw
            if is_lmb_pressed:
                if (0 <= x < ROOM_W_TILE_UNIT) and (0 <= y < ROOM_H_TILE_UNIT):
                    item = selected_room[y * NATIVE_W_TILE_UNIT + x]
                    if item == 0:
                        selected_room[y * NATIVE_W_TILE_UNIT + x] = {"pos": (
                            draw_pos_x, draw_pos_y), "region": selected_region, "name": selected_name}
                        if selected_name in ["floor", "rock", "bg_rock"]:
                            update_bitmasks((x, y), (draw_pos_x, draw_pos_y))

            # Erase
            elif is_rmb_pressed:
                if (0 <= x < ROOM_W_TILE_UNIT) and (0 <= y < ROOM_H_TILE_UNIT):
                    item = selected_room[y * NATIVE_W_TILE_UNIT + x]
                    if item != 0:
                        selected_room[y * NATIVE_W_TILE_UNIT + x] = 0
                        if selected_name in ["floor", "rock", "bg_rock"]:
                            update_bitmasks((x, y), (draw_pos_x, draw_pos_y))

            # Fill
            elif is_mmb_pressed:
                if (0 <= x < ROOM_W_TILE_UNIT) and (0 <= y < ROOM_H_TILE_UNIT):
                    item = selected_room[y * NATIVE_W_TILE_UNIT + x]
                    if item == 0:
                        selected_room[y * NATIVE_W_TILE_UNIT + x] = {"pos": (
                            draw_pos_x, draw_pos_y), "region": selected_region, "name": selected_name}
                        fill((x, y), (draw_pos_x, draw_pos_y))

        # Move camera
        cam_dir.x = is_d_pressed - is_a_pressed
        cam_dir.y = is_s_pressed - is_w_pressed
        if cam_dir.length_squared() > 0:
            cam_dir.normalize_ip()
        cam_vel = cam_vel.lerp(cam_dir * CAM_SPD, CAM_LERP_FACTOR)
        cam_vel.x = 0 if abs(cam_vel.x) < 0.001 else cam_vel.x
        cam_vel.y = 0 if abs(cam_vel.y) < 0.001 else cam_vel.y
        CAM_RECT.x += cam_vel.x * dt
        CAM_RECT.y += cam_vel.y * dt

    # Draw fps
    FONT.render_to(
        NATIVE_SURF, (FONT_W, FONT_H), f"FPS: {CLOCK.get_fps()}", "grey100"
    )

    # Native to window
    pg.transform.scale(NATIVE_SURF, (WINDOW_W, WINDOW_H), WINDOW_SURF)

    # Update window
    pg.display.update()
