import pygame as pg
import pygame.freetype as font
from sys import exit
from json import load
from os.path import join

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
CAM_SPD = 2

# region Dummy player
PLAYER_SURF = pg.Surface((16, 16))
PLAYER_SURF.fill("red")
PLAYER_RECT = PLAYER_SURF.get_rect()
PLAYER_RECT.x = tile_s * 3
PLAYER_FUTURE_RECT = PLAYER_SURF.get_rect()
PLAYER_FUTURE_RECT.center = PLAYER_RECT.center
# endregion

# Player collision
player_min_bottom = None

# Main loop
while 1:
    # Dt
    dt = CLOCK.tick(FPS)

    # Clear native
    NATIVE_SURF.fill("grey0")

    # region Move camera to follow target
    CAM_RECT.center = PLAYER_RECT.center
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
    xd = PLAYER_RECT.x - CAM_RECT.x
    yd = PLAYER_RECT.y - CAM_RECT.y
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

    # region Move player
    pressed = pg.key.get_pressed()
    direction_x = pressed[pg.K_d] - pressed[pg.K_a]
    direction_y = pressed[pg.K_s] - pressed[pg.K_w]
    PLAYER_FUTURE_RECT.center = PLAYER_RECT.center
    x_tu = PLAYER_RECT.centerx // tile_s
    y_tu = PLAYER_RECT.centery // tile_s

    # Possible positions
    player_tl_tu = (x_tu - 1, y_tu - 1)
    player_tt_tu = (x_tu, y_tu - 1)
    player_tr_tu = (x_tu + 1, y_tu - 1)
    player_ml_tu = (x_tu - 1, y_tu - 0)
    player_mr_tu = (x_tu + 1, y_tu - 0)
    player_bl_tu = (x_tu - 1, y_tu + 1)
    player_bm_tu = (x_tu, y_tu + 1)
    player_br_tu = (x_tu + 1, y_tu + 1)

    # Filter the ones needed with direction
    direction_to_locations_tu = {
        # No movement
        (0, 0): [],
        # Up
        (0, -1): [player_tl_tu, player_tt_tu, player_tr_tu],
        # Up-Right
        (1, -1): [player_tl_tu, player_tt_tu, player_tr_tu, player_mr_tu, player_br_tu],
        # Right
        (1, 0): [player_tr_tu, player_mr_tu, player_br_tu],
        # Down-Right
        (1, 1): [player_bl_tu, player_bm_tu, player_br_tu, player_mr_tu, player_tr_tu],
        # Down
        (0, 1): [player_bl_tu, player_bm_tu, player_br_tu],
        # Down-Left
        (-1, 1): [player_tl_tu, player_ml_tu, player_bl_tu, player_bm_tu, player_br_tu],
        # Left
        (-1, 0): [player_tl_tu, player_ml_tu, player_bl_tu],
        # Up-Left
        (-1, -1): [player_bl_tu, player_ml_tu, player_tl_tu, player_tt_tu, player_tr_tu]
    }

    # Get the possible locations based on direction
    filtered_possible_locations_tu = direction_to_locations_tu.get(
        (direction_x, direction_y), [])

    # Check filtered_possible_locations_tu
    possible_collision_tiles_rects_list = []
    for location_tu in filtered_possible_locations_tu:
        possible_location_x_tu = location_tu[0]
        possible_location_y_tu = location_tu[1]

        # Clamp withing room
        possible_location_x_tu = max(
            min(possible_location_x_tu, room_w_tu - 1), room_x_tu)
        possible_location_y_tu = max(
            min(possible_location_y_tu, room_h_tu - 1), room_y_tu)
        cell = collision_layer[possible_location_y_tu *
                               room_w_tu + possible_location_x_tu]

        # region debug possible player collision
        # pg.draw.rect(
        #     NATIVE_SURF,
        #     "yellow",
        #     pg.Rect(
        #         (possible_location_x_tu * tile_s) - CAM_RECT.x,
        #         (possible_location_y_tu * tile_s) - CAM_RECT.y,
        #         tile_s,
        #         tile_s
        #     ),
        #     1
        # )

        # No obj nearby, move
        if cell == 0:
            continue

        # Found rect?
        possible_collision_tiles_rects_list.append(cell)

        # debug draw found rect
        # x1 = cell["xds"]
        # y1 = cell["yds"]
        # w1 = x1 + tile_s
        # h1 = y1 + tile_s
        # pg.draw.rect(
        #     NATIVE_SURF,
        #     "red",
        #     pg.Rect(
        #         (cell["xds"]) - CAM_RECT.x,
        #         (cell["yds"]) - CAM_RECT.y,
        #         tile_s,
        #         tile_s
        #     ),
        #     1
        # )

    # Check horizontal
    displacement_x = abs(direction_x * CAM_SPD)
    while displacement_x > 0:
        PLAYER_FUTURE_RECT.x += direction_x
        displacement_x -= 1
        # Collide?
        for cell in possible_collision_tiles_rects_list:
            x1 = cell["xds"]
            y1 = cell["yds"]
            x2 = PLAYER_FUTURE_RECT.x
            y2 = PLAYER_FUTURE_RECT.y
            right1, bottom1 = x1 + tile_s, y1 + tile_s
            right2, bottom2 = x2 + tile_s, y2 + tile_s
            if right1 > x2 and x1 < right2 and bottom1 > y2 and y1 < bottom2:
                # Reset check
                PLAYER_FUTURE_RECT.x -= direction_x
                displacement_x = 0
                direction_x = 0
                break

    # Collide?
    displacement_y = abs(direction_y * CAM_SPD)
    while displacement_y > 0:
        PLAYER_FUTURE_RECT.y += direction_y
        displacement_y -= 1
        # Collide?
        for cell in possible_collision_tiles_rects_list:
            x1 = cell["xds"]
            y1 = cell["yds"]
            x2 = PLAYER_FUTURE_RECT.x
            y2 = PLAYER_FUTURE_RECT.y
            right1, bottom1 = x1 + tile_s, y1 + tile_s
            right2, bottom2 = x2 + tile_s, y2 + tile_s
            if right1 > x2 and x1 < right2 and bottom1 > y2 and y1 < bottom2:
                # Reset check
                PLAYER_FUTURE_RECT.y -= direction_y
                displacement_y = 0
                direction_y = 0
                break

    PLAYER_RECT.x += direction_x * CAM_SPD
    PLAYER_RECT.y += direction_y * CAM_SPD
    PLAYER_RECT.clamp_ip(CAM_RECT)
    # endregion

    # debug render player rect and future rect
    # xd = PLAYER_RECT.x - CAM_RECT.x
    # yd = PLAYER_RECT.y - CAM_RECT.y
    # pg.draw.rect(NATIVE_SURF, "blue", (xd, yd, tile_s, tile_s), 1)

    # Get event
    for event in pg.event.get(EVENTS):
        # region Window quit
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        # endregion

    # region Debug draw
    FONT.render_to(NATIVE_SURF, (FONT_W, 32 * FONT_H),
                   f"fps: {int(CLOCK.get_fps())}", "grey100", "black")
    # endregion

    # region Native to window and update window
    pg.transform.scale(NATIVE_SURF, (window_w, window_h), window_surf)
    pg.display.update()
    # endregion
