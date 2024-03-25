import pygame as pg
import pygame.freetype as font
from sys import exit
from json import load
from os.path import join
import time

pg.init()


ROOM_PATHS = {
    "bedroom": join("room_json_data", "stage_1", "bedroom.json")
}

# TODO: Check save data to determine which room to load at start
room_path = ROOM_PATHS["bedroom"]

with open(room_path, 'r') as json_file:
    room_dict = load(json_file)

bg_layers = room_dict["BG_LAYERS"]
collision_layer = room_dict["COLLISION_LAYER"]
collision_draw_layer = [x for x in collision_layer if x != 0]
fg_layers = room_dict["FG_LAYERS"]
tile_s = room_dict["TILE_S"]
room_rect = room_dict["ROOM_RECT"]
room_x_tu = room_rect[0] // tile_s
room_y_tu = room_rect[1] // tile_s
room_w_tu = room_rect[2] // tile_s
room_h_tu = room_rect[3] // tile_s
sprite_sheet_png_name = room_dict["SPRITE_SHEET_PNG_NAME"]
bg1 = room_dict["BG1"]
bg2 = room_dict["BG2"]
bg3 = room_dict["BG3"]

# TODO: Settings page surface / state to change this -> in turn set display again
resolution = 4

FONT_H = 5
FONT_W = 3
FPS = 60
NATIVE_W_TU = 20
NATIVE_H_TU = 11
NATIVE_W = tile_s * NATIVE_W_TU
NATIVE_H = tile_s * NATIVE_H_TU

window_w = NATIVE_W * resolution
window_h = NATIVE_H * resolution
window_surf = pg.display.set_mode((window_w, window_h))
NATIVE_SURF = pg.Surface((NATIVE_W, NATIVE_H))
CLOCK = pg.time.Clock()
FONT = font.Font("cg_pixel_3x5_mono.ttf", FONT_H)
EVENTS = [pg.KEYDOWN, pg.KEYUP, pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.QUIT]
CAM_RECT = pg.Rect(0, 0, NATIVE_W, NATIVE_H)
SPRITE_SHEET_SURF = pg.image.load(sprite_sheet_png_name).convert_alpha()
PLAYER_SPD = 2

# region Player
PLAYER_SURF = pg.Surface((6, 31))
PLAYER_SURF.fill("red")

is_left_pressed = 0
is_right_pressed = 0
is_down_pressed = False
PLAYER_FRECT = pg.FRect(32, 0, 6, 31)
MAX_RUN = 0.09
RUN_LERP_WEIGHT = 0.2
MAX_FALL = 0.27
NORMAL_GRAVITY = 0.533
HEAVY_GRAVITY = 1.066
GRAVITY = NORMAL_GRAVITY
JUMP_SPD = -0.23
remainder_x = 0
remainder_y = 0
velocity = pg.math.Vector2()
direction = 0
facing_direction = 1
old_facing_direction = facing_direction
# endregion

# Main loop
while 1:
    # Dt
    dt = CLOCK.tick(FPS)

    # Clear native
    NATIVE_SURF.fill("grey0")

    # region Move camera to follow target
    CAM_RECT.center = PLAYER_FRECT.center
    CAM_RECT.clamp_ip(room_rect)
    # endregion

    # region Backgrounds
    # TODO: save the bg constants up there
    if bg1 == "sky":
        x = (-CAM_RECT.x * 0.05) % NATIVE_W
        NATIVE_SURF.blit(SPRITE_SHEET_SURF, (x, 0), (0, 0, 320, 179))
        NATIVE_SURF.blit(SPRITE_SHEET_SURF,
                         (x - NATIVE_W, 0), (0, 0, 320, 179))
    if bg2 == "clouds":
        x = (-CAM_RECT.x * 0.1) % NATIVE_W
        NATIVE_SURF.blit(SPRITE_SHEET_SURF, (x, 0), (0, 176, 320, 160))
        NATIVE_SURF.blit(SPRITE_SHEET_SURF,
                         (x - NATIVE_W, 0), (0, 176, 320, 160))
    if bg3 == "trees":
        x = (-CAM_RECT.x * 0.5) % NATIVE_W
        # 1
        NATIVE_SURF.blit(SPRITE_SHEET_SURF, (x, 32), (320, 448, 80, 160))
        NATIVE_SURF.blit(SPRITE_SHEET_SURF,
                         (x - NATIVE_W, 32), (320, 448, 80, 160))
        # 2
        NATIVE_SURF.blit(SPRITE_SHEET_SURF, (x + 96, 64), (320, 448, 80, 160))
        NATIVE_SURF.blit(SPRITE_SHEET_SURF,
                         (x + 96 - NATIVE_W, 64), (320, 448, 80, 160))
        # 3
        NATIVE_SURF.blit(SPRITE_SHEET_SURF, (x + 160, 32), (320, 448, 80, 160))
        NATIVE_SURF.blit(SPRITE_SHEET_SURF,
                         (x + 160 - NATIVE_W, 32), (320, 448, 80, 160))
        # 4
        NATIVE_SURF.blit(SPRITE_SHEET_SURF, (x + 224, 16), (320, 448, 80, 160))
        NATIVE_SURF.blit(SPRITE_SHEET_SURF,
                         (x + 224 - NATIVE_W, 16), (320, 448, 80, 160))
    # endregion

    # region Draw all bg sprites
    for room in bg_layers:
        for item in room:
            # Only update sprites that are in view
            if (CAM_RECT.x - item["region"][2] <= item["xds"] < CAM_RECT.right) and (CAM_RECT.y - item["region"][3] <= item["yds"] < CAM_RECT.bottom):
                xd = item["xds"] - CAM_RECT.x
                yd = item["yds"] - CAM_RECT.y
                NATIVE_SURF.blit(SPRITE_SHEET_SURF, (xd, yd), item["region"])
    # endregion

    # region Draw all collision sprites
    for item in collision_draw_layer:
        # Only update sprites that are in view
        if (CAM_RECT.x - item["region"][2] <= item["xds"] < CAM_RECT.right) and (CAM_RECT.y - item["region"][3] <= item["yds"] < CAM_RECT.bottom):
            xd = item["xds"] - CAM_RECT.x
            yd = item["yds"] - CAM_RECT.y
            NATIVE_SURF.blit(SPRITE_SHEET_SURF, (xd, yd), item["region"])
    # endregion

    # region Draw player
    xd = PLAYER_FRECT.x - CAM_RECT.x
    yd = PLAYER_FRECT.y - CAM_RECT.y
    NATIVE_SURF.blit(PLAYER_SURF, (xd, yd))
    # endregion

    # region Draw all fg sprites
    for room in fg_layers:
        for item in room:
            # Only update sprites that are in view
            if (CAM_RECT.x - item["region"][2] <= item["xds"] < CAM_RECT.right) and (CAM_RECT.y - item["region"][3] <= item["yds"] < CAM_RECT.bottom):
                xd = item["xds"] - CAM_RECT.x
                yd = item["yds"] - CAM_RECT.y
                NATIVE_SURF.blit(SPRITE_SHEET_SURF, (xd, yd), item["region"])
    # endregion

    # region Player update
    # Update velocity with gravity
    velocity.y += GRAVITY * dt
    velocity.y = min(velocity.y, MAX_FALL)

    # Update x velocity with direction
    velocity.x = pg.math.smoothstep(
        velocity.x,
        direction * MAX_RUN,
        RUN_LERP_WEIGHT
    )
    if abs(velocity.x) < 0.001:
        velocity.x = 0

    direction_x = 0
    if velocity.x > 0:
        direction_x = 1
    if velocity.x < 0:
        direction_x = -1

    direction_y = 0
    if velocity.y > 0:
        direction_y = 1
    if velocity.y < 0:
        direction_y = -1

    # Distance to cover horizontally
    amount = velocity.x * dt
    remainder_x += amount
    displacement_x = round(remainder_x)

    if direction_x != 0:
        remainder_x -= displacement_x
        displacement_x = abs(displacement_x)
        # Check 1px at a time
        while displacement_x > 0:
            # Player currrent pos to tu
            possible_x_tu = PLAYER_FRECT.centerx // tile_s
            possible_y_tu = PLAYER_FRECT.centery // tile_s

            # Debug draw player real rect
            xd = PLAYER_FRECT.x - CAM_RECT.x
            yd = PLAYER_FRECT.y - CAM_RECT.y
            pg.draw.rect(NATIVE_SURF, "green",
                         (xd, yd, PLAYER_FRECT.width, PLAYER_FRECT.height), 1)

            # Possible positions
            player_tl_tu = (possible_x_tu - 1, possible_y_tu - 1)
            player_tt_tu = (possible_x_tu, possible_y_tu - 1)
            player_tr_tu = (possible_x_tu + 1, possible_y_tu - 1)
            player_ml_tu = (possible_x_tu - 1, possible_y_tu - 0)
            player_mr_tu = (possible_x_tu + 1, possible_y_tu - 0)
            player_bl_tu = (possible_x_tu - 1, possible_y_tu + 1)
            player_bm_tu = (possible_x_tu, possible_y_tu + 1)
            player_br_tu = (possible_x_tu + 1, possible_y_tu + 1)

            # Select the ones needed with direction
            possible_pos_tus = []
            if direction_x == 0 and direction_y == 0:
                possible_pos_tus = []
            elif direction_x == 0 and direction_y == -1:
                possible_pos_tus = [player_tl_tu, player_tt_tu, player_tr_tu]
            elif direction_x == 1 and direction_y == -1:
                possible_pos_tus = [
                    player_tl_tu, player_tt_tu, player_tr_tu, player_mr_tu, player_br_tu]
            elif direction_x == 1 and direction_y == 0:
                possible_pos_tus = [player_tr_tu, player_mr_tu, player_br_tu]
            elif direction_x == 1 and direction_y == 1:
                possible_pos_tus = [
                    player_bl_tu, player_bm_tu, player_br_tu, player_mr_tu, player_tr_tu]
            elif direction_x == 0 and direction_y == 1:
                possible_pos_tus = [
                    player_bl_tu, player_bm_tu, player_br_tu]
            elif direction_x == -1 and direction_y == 1:
                possible_pos_tus = [
                    player_tl_tu, player_ml_tu, player_bl_tu, player_bm_tu, player_br_tu]
            elif direction_x == -1 and direction_y == 0:
                possible_pos_tus = [
                    player_tl_tu, player_ml_tu, player_bl_tu]
            elif direction_x == -1 and direction_y == -1:
                possible_pos_tus = [
                    player_bl_tu, player_ml_tu, player_tl_tu, player_tt_tu, player_tr_tu]

            # Check filtered_possible_locations_tu
            possible_cells = []
            for possible_pos_tu in possible_pos_tus:
                possible_x_tu = possible_pos_tu[0]
                possible_y_tu = possible_pos_tu[1]

                # Clamp withing room
                possible_x_tu = max(
                    min(possible_x_tu, room_w_tu - 1), room_x_tu)
                possible_y_tu = max(
                    min(possible_y_tu, room_h_tu - 1), room_y_tu)
                possible_x_tu = int(possible_x_tu)
                possible_y_tu = int(possible_y_tu)

                # Tu -> cell
                cell = collision_layer[possible_y_tu *
                                       room_w_tu + possible_x_tu]

                # Debug draw possible cell
                possible_xd = (possible_x_tu * tile_s) - CAM_RECT.x
                possible_yd = (possible_y_tu * tile_s) - CAM_RECT.y
                pg.draw.lines(
                    NATIVE_SURF,
                    "green",
                    True,
                    [
                        (possible_xd, possible_yd),
                        (possible_xd + tile_s, possible_yd),
                        (possible_xd + tile_s, possible_yd + tile_s),
                        (possible_xd, possible_yd + tile_s),
                    ]
                )

                # Air? look somewhere else
                if cell == 0:
                    continue

                # Found rect?
                possible_cells.append(cell)

                # Debug draw possible found cells
                pg.draw.rect(
                    NATIVE_SURF,
                    "yellow",
                    [
                        possible_xd,
                        possible_yd,
                        tile_s,
                        tile_s
                    ]
                )
            # My future position
            xds = PLAYER_FRECT.x
            yds = PLAYER_FRECT.y
            xds += direction_x
            w = xds + PLAYER_FRECT.width
            h = yds + PLAYER_FRECT.height

            # Debug draw my future rect
            pg.draw.rect(
                NATIVE_SURF,
                "blue",
                [xds - CAM_RECT.x, yds - CAM_RECT.y,
                    PLAYER_FRECT.width, PLAYER_FRECT.height],
                1
            )

            # AABB with all possible neighbours
            is_collide = False
            for cell in possible_cells:
                # Cell rect
                c_xds = cell["xds"]
                c_yds = cell["yds"]
                c_w = c_xds + tile_s
                c_h = c_yds + tile_s
                # Future hit something? Break set flag to true
                if (c_xds < w and xds < c_w and c_yds < h and yds < c_h):
                    is_collide = True
                    break

            # Future hit? Break
            if is_collide:
                break

            # Future no hit? Move to next pixel
            displacement_x -= 1
            PLAYER_FRECT.x += direction_x
            PLAYER_FRECT.clamp_ip(CAM_RECT)

    # Distance to cover vertically
    amount = velocity.y * dt
    remainder_y += amount
    displacement_y = round(remainder_y)

    if direction_y != 0:
        remainder_y -= displacement_y
        displacement_y = abs(displacement_y)

        # Check 1px at a time
        while displacement_y > 0:
            # Player currrent pos to tu
            possible_x_tu = PLAYER_FRECT.centerx // tile_s
            possible_y_tu = PLAYER_FRECT.centery // tile_s

            # Debug draw player real rect
            xd = PLAYER_FRECT.x - CAM_RECT.x
            yd = PLAYER_FRECT.y - CAM_RECT.y
            pg.draw.rect(NATIVE_SURF, "green",
                         (xd, yd, PLAYER_FRECT.width, PLAYER_FRECT.height), 1)

            # Possible positions
            player_tl_tu = (possible_x_tu - 1, possible_y_tu - 1)
            player_tt_tu = (possible_x_tu, possible_y_tu - 1)
            player_tr_tu = (possible_x_tu + 1, possible_y_tu - 1)
            player_ml_tu = (possible_x_tu - 1, possible_y_tu - 0)
            player_mr_tu = (possible_x_tu + 1, possible_y_tu - 0)
            player_bl_tu = (possible_x_tu - 1, possible_y_tu + 1)
            player_bm_tu = (possible_x_tu, possible_y_tu + 1)
            player_br_tu = (possible_x_tu + 1, possible_y_tu + 1)

            # Select the ones needed with direction
            possible_pos_tus = []
            if direction_x == 0 and direction_y == 0:
                possible_pos_tus = []
            elif direction_x == 0 and direction_y == -1:
                possible_pos_tus = [player_tl_tu, player_tt_tu, player_tr_tu]
            elif direction_x == 1 and direction_y == -1:
                possible_pos_tus = [
                    player_tl_tu, player_tt_tu, player_tr_tu, player_mr_tu, player_br_tu]
            elif direction_x == 1 and direction_y == 0:
                possible_pos_tus = [player_tr_tu, player_mr_tu, player_br_tu]
            elif direction_x == 1 and direction_y == 1:
                possible_pos_tus = [
                    player_bl_tu, player_bm_tu, player_br_tu, player_mr_tu, player_tr_tu]
            elif direction_x == 0 and direction_y == 1:
                possible_pos_tus = [
                    player_bl_tu, player_bm_tu, player_br_tu]
            elif direction_x == -1 and direction_y == 1:
                possible_pos_tus = [
                    player_tl_tu, player_ml_tu, player_bl_tu, player_bm_tu, player_br_tu]
            elif direction_x == -1 and direction_y == 0:
                possible_pos_tus = [
                    player_tl_tu, player_ml_tu, player_bl_tu]
            elif direction_x == -1 and direction_y == -1:
                possible_pos_tus = [
                    player_bl_tu, player_ml_tu, player_tl_tu, player_tt_tu, player_tr_tu]

            # Check filtered_possible_locations_tu
            possible_cells = []
            for possible_pos_tu in possible_pos_tus:
                possible_x_tu = possible_pos_tu[0]
                possible_y_tu = possible_pos_tu[1]

                # Clamp withing room
                possible_x_tu = max(
                    min(possible_x_tu, room_w_tu - 1), room_x_tu)
                possible_y_tu = max(
                    min(possible_y_tu, room_h_tu - 1), room_y_tu)
                possible_x_tu = int(possible_x_tu)
                possible_y_tu = int(possible_y_tu)

                # Tu -> cell
                cell = collision_layer[possible_y_tu *
                                       room_w_tu + possible_x_tu]

                # Debug draw possible cell
                possible_xd = (possible_x_tu * tile_s) - CAM_RECT.x
                possible_yd = (possible_y_tu * tile_s) - CAM_RECT.y
                pg.draw.lines(
                    NATIVE_SURF,
                    "green",
                    True,
                    [
                        (possible_xd, possible_yd),
                        (possible_xd + tile_s, possible_yd),
                        (possible_xd + tile_s, possible_yd + tile_s),
                        (possible_xd, possible_yd + tile_s),
                    ]
                )

                # Air? look somewhere else
                if cell == 0:
                    continue

                # Found rect?
                possible_cells.append(cell)

                # Debug draw possible found cells
                pg.draw.rect(
                    NATIVE_SURF,
                    "yellow",
                    [
                        possible_xd,
                        possible_yd,
                        tile_s,
                        tile_s
                    ]
                )
            # My future position
            xds = PLAYER_FRECT.x
            yds = PLAYER_FRECT.y
            yds += direction_y
            w = xds + PLAYER_FRECT.width
            h = yds + PLAYER_FRECT.height

            # Debug draw my future rect
            pg.draw.rect(
                NATIVE_SURF,
                "blue",
                [xds - CAM_RECT.x, yds - CAM_RECT.y,
                    PLAYER_FRECT.width, PLAYER_FRECT.height],
                1
            )

            # AABB with all possible neighbours
            is_collide = False
            for cell in possible_cells:
                # Cell rect
                c_xds = cell["xds"]
                c_yds = cell["yds"]
                c_w = c_xds + tile_s
                c_h = c_yds + tile_s
                # Future hit something? Break set flag to true
                if (c_xds < w and xds < c_w and c_yds < h and yds < c_h):
                    is_collide = True
                    break

            # Future hit? Break
            if is_collide:
                break

            # Future no hit? Move to next pixel
            displacement_y -= 1
            PLAYER_FRECT.y += direction_y
            PLAYER_FRECT.clamp_ip(CAM_RECT)
        # endregion

    # Get horizontal input direction
    direction = is_right_pressed - is_left_pressed

    # Get event
    for event in pg.event.get(EVENTS):
        # region Window quit
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        # endregion

        # Key down
        if event.type == pg.KEYDOWN:
            # Just pressed left
            if event.key == pg.K_a:
                # Set is pressed left 1
                is_left_pressed = 1

            # Just pressed right
            elif event.key == pg.K_d:
                # Set is pressed right 1
                is_right_pressed = 1

            # Just pressed down
            elif event.key == pg.K_s:
                # Set is pressed down true
                is_down_pressed = True

            # Just pressed jump
            elif event.key == pg.K_SPACE:
                # Idle, run crouch can jump
                pass

            # Just pressed shoot
            elif event.key == pg.K_j:
                # Idle, run crouch can shoot
                pass

        # Key up
        elif event.type == pg.KEYUP:
            # Just released left
            if event.key == pg.K_a:
                # Set is released left 0
                is_left_pressed = 0

            # Just released right
            elif event.key == pg.K_d:
                # Set is released right 0
                is_right_pressed = 0

            # Just released down
            elif event.key == pg.K_s:
                # Set is released down false
                is_down_pressed = False

            # Just released jump
            elif event.key == pg.K_SPACE:
                # Idle, run crouch can jump
                pass

    # region Debug draw
    FONT.render_to(NATIVE_SURF, (FONT_W, 32 * FONT_H),
                   f"fps: {int(CLOCK.get_fps())}", "grey100", "black")
    # endregion

    # region Native to window and update window
    pg.transform.scale(NATIVE_SURF, (window_w, window_h), window_surf)
    pg.display.update()
    # endregion
