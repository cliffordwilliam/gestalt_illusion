import pygame as pg
import pygame.freetype as font
from sys import exit

pg.init()

# Constants
TILE_SIZE = 16
FPS = 60
CLOCK = pg.time.Clock()
NATIVE_RECT = pg.Rect(0, 0, 320, 176)
RESOLUTION_SCALE = 5
DISPLAY_SURFACE = pg.display.set_mode(
    (
        NATIVE_RECT.width * RESOLUTION_SCALE,
        NATIVE_RECT.height * RESOLUTION_SCALE
    )
)
DISPLAY_RECT = DISPLAY_SURFACE.get_rect()
NATIVE_SURFACE = pg.Surface(
    (
        NATIVE_RECT.width,
        NATIVE_RECT.height
    )
)
ORIGIN_RECT = pg.Rect(0, 0, 2, 2)
ORIGIN_RECT.center = (0, 0)
FONT = font.Font(
    "cg_pixel_3x5_mono.ttf",
    5
)
SPRITE_SHEET_SURFACE = pg.image.load(
    "stage_1_sprite_sheet.png"
).convert_alpha()
ALPHA_SPRITE_SHEET_SURFACE = pg.image.load(
    "stage_1_sprite_sheet.png"
).convert_alpha()
ALPHA_SPRITE_SHEET_SURFACE.set_alpha(122)
HORIZONTAL_TILES = 20
TOTAL_TILES = 220
CAM_FRECT = pg.FRect(0, 0, NATIVE_RECT.width, NATIVE_RECT.height)
CAM_SPEED = 0.09
CAM_LERP_WEIGHT = 0.2
TILE_GRID_SURFACE = pg.Surface((320, 176))
TILE_GRID_SURFACE.set_colorkey("red")
TILE_GRID_SURFACE.set_alpha(10)
ROOM_GRID_SURFACE = pg.Surface((320, 176))
ROOM_GRID_SURFACE.set_colorkey("red")
ROOM_GRID_SURFACE.set_alpha(20)

# Cam movement
cam_velocity = pg.math.Vector2()
direction = pg.math.Vector2()

# Menu state
is_menu = False


class Sky():
    def __init__(self, position):
        self.name = "sky"
        self.region = (0, 0, 320, 176)
        self.frect = pg.FRect(
            position[0],
            position[1],
            320,
            176
        )

    def draw(self):
        draw_position_x = (self.frect.x - CAM_FRECT.x) * 0.05
        draw_position_x = draw_position_x % 320
        NATIVE_SURFACE.blit(
            SPRITE_SHEET_SURFACE,
            (
                draw_position_x,
                0
            ),
            self.region
        )
        NATIVE_SURFACE.blit(
            SPRITE_SHEET_SURFACE,
            (
                draw_position_x - 320,
                0
            ),
            self.region
        )


class Cloud():
    def __init__(self, position):
        self.name = "cloud"
        self.region = (0, 176, 320, 160)
        self.frect = pg.FRect(
            position[0],
            position[1],
            320,
            160
        )

    def draw(self):
        draw_position_x = (self.frect.x - CAM_FRECT.x) * 0.1
        draw_position_x = draw_position_x % 320
        NATIVE_SURFACE.blit(
            SPRITE_SHEET_SURFACE,
            (
                draw_position_x,
                0
            ),
            self.region
        )
        NATIVE_SURFACE.blit(
            SPRITE_SHEET_SURFACE,
            (
                draw_position_x - 320,
                0
            ),
            self.region
        )


class Trees():
    def __init__(self, position):
        self.name = "trees"
        self.region = (320, 448, 80, 160)
        self.frect = pg.FRect(
            position[0],
            position[1],
            80,
            160
        )

    def draw(self):
        draw_position_x = (self.frect.x - CAM_FRECT.x) * 0.5
        draw_position_x = draw_position_x % 320
        # 1
        NATIVE_SURFACE.blit(
            SPRITE_SHEET_SURFACE,
            (
                draw_position_x,
                32
            ),
            self.region
        )
        NATIVE_SURFACE.blit(
            SPRITE_SHEET_SURFACE,
            (
                draw_position_x - 320,
                32
            ),
            self.region
        )
        # 2
        NATIVE_SURFACE.blit(
            SPRITE_SHEET_SURFACE,
            (
                draw_position_x + 112,
                64
            ),
            self.region
        )
        NATIVE_SURFACE.blit(
            SPRITE_SHEET_SURFACE,
            (
                draw_position_x - 320 + 112,
                64
            ),
            self.region
        )
        # 3
        NATIVE_SURFACE.blit(
            SPRITE_SHEET_SURFACE,
            (
                draw_position_x + 176,
                32
            ),
            self.region
        )
        NATIVE_SURFACE.blit(
            SPRITE_SHEET_SURFACE,
            (
                draw_position_x - 320 + 176,
                32
            ),
            self.region
        )
        # 4
        NATIVE_SURFACE.blit(
            SPRITE_SHEET_SURFACE,
            (
                draw_position_x + 240,
                16
            ),
            self.region
        )
        NATIVE_SURFACE.blit(
            SPRITE_SHEET_SURFACE,
            (
                draw_position_x - 320 + 240,
                16
            ),
            self.region
        )


class Glow():
    def __init__(self, position):
        self.name = "glow"
        self.region = (0, 512, 320, 128)
        self.frect = pg.FRect(
            position[0],
            position[1],
            320,
            128
        )

    def draw(self):
        NATIVE_SURFACE.blit(
            SPRITE_SHEET_SURFACE,
            (
                0,
                48
            ),
            self.region
        )


class Floor():
    def __init__(self, position):
        self.name = "floor"
        self.frect = pg.FRect(
            position[0],
            position[1],
            16,
            16
        )
        self.preview_frect = pg.FRect(
            position[0],
            position[1],
            16,
            16
        )
        self.highlight_frect = self.frect.inflate(8, 8)
        self.frames_dict = {
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
        self.frame_mask_key = 0

    def global_draw(self, dt):
        NATIVE_SURFACE.blit(
            SPRITE_SHEET_SURFACE,
            (
                self.frect.x,
                self.frect.y
            ),
            self.frames_dict[self.frame_mask_key]
        )
        pg.draw.rect(
            NATIVE_SURFACE,
            "grey20",
            self.highlight_frect,
            1
        )

    def draw_rect(self):
        pg.draw.rect(
            NATIVE_SURFACE,
            "white",
            self.highlight_frect,
            1
        )

    def draw(self, dt):
        draw_position_x = self.frect.x - CAM_FRECT.x
        draw_position_y = self.frect.y - CAM_FRECT.y
        NATIVE_SURFACE.blit(
            SPRITE_SHEET_SURFACE,
            (
                draw_position_x,
                draw_position_y
            ),
            self.frames_dict[self.frame_mask_key]
        )

    def draw_preview(self, dt, position):
        NATIVE_SURFACE.blit(
            ALPHA_SPRITE_SHEET_SURFACE,
            position,
            self.frames_dict[0]
        )
        self.preview_frect.x = position[0]
        self.preview_frect.y = position[1]
        pg.draw.rect(
            NATIVE_SURFACE,
            "red",
            self.preview_frect,
            1
        )


class Stone():
    def __init__(self, position):
        self.name = "stone"
        self.frect = pg.FRect(
            position[0],
            position[1],
            16,
            16
        )
        self.preview_frect = pg.FRect(
            position[0],
            position[1],
            16,
            16
        )
        self.highlight_frect = self.frect.inflate(8, 8)
        self.frames_dict = {
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
        }
        self.frame_mask_key = 0

    def global_draw(self, dt):
        NATIVE_SURFACE.blit(
            SPRITE_SHEET_SURFACE,
            (
                self.frect.x,
                self.frect.y
            ),
            self.frames_dict[self.frame_mask_key]
        )
        pg.draw.rect(
            NATIVE_SURFACE,
            "grey20",
            self.highlight_frect,
            1
        )

    def draw_rect(self):
        pg.draw.rect(
            NATIVE_SURFACE,
            "white",
            self.highlight_frect,
            1
        )

    def draw(self, dt):
        draw_position_x = self.frect.x - CAM_FRECT.x
        draw_position_y = self.frect.y - CAM_FRECT.y
        NATIVE_SURFACE.blit(
            SPRITE_SHEET_SURFACE,
            (
                draw_position_x,
                draw_position_y
            ),
            self.frames_dict[self.frame_mask_key]
        )

    def draw_preview(self, dt, position):
        NATIVE_SURFACE.blit(
            ALPHA_SPRITE_SHEET_SURFACE,
            position,
            self.frames_dict[0]
        )
        self.preview_frect.x = position[0]
        self.preview_frect.y = position[1]
        pg.draw.rect(
            NATIVE_SURFACE,
            "red",
            self.preview_frect,
            1
        )


class Scone():
    def __init__(self, position):
        self.name = "scone"
        self.frect = pg.FRect(
            position[0],
            position[1],
            16,
            16
        )
        self.preview_frect = pg.FRect(
            position[0],
            position[1],
            16,
            48
        )
        self.highlight_frect = self.frect.inflate(8, 8)
        self.body_region = (416, 368, 16, 32)
        self.frames_list = [
            (336, 400, 16, 16),
            (352, 400, 16, 16),
            (368, 400, 16, 16),
            (384, 400, 16, 16),
            (400, 400, 16, 16),
            (416, 400, 16, 16),
            (432, 400, 16, 16),
            (448, 400, 16, 16),
            (464, 400, 16, 16),
            (480, 400, 16, 16),
            (336, 416, 16, 16),
            (352, 416, 16, 16),
            (368, 416, 16, 16),
            (384, 416, 16, 16),
            (400, 416, 16, 16),
            (416, 416, 16, 16),
        ]
        self.frame_mask_key = 0
        self.total_dt = 0
        self.frame_index = 0

    def global_draw(self, dt):
        self.total_dt += dt
        if self.total_dt >= 100:
            self.total_dt = 0
            self.frame_index += 1
            if self.frame_index > len(self.frames_list) - 1:
                self.frame_index = 0
        NATIVE_SURFACE.blit(
            # Flame
            SPRITE_SHEET_SURFACE,
            (
                self.frect.x,
                self.frect.y
            ),
            self.frames_list[self.frame_index]
        )
        pg.draw.rect(
            NATIVE_SURFACE,
            "grey20",
            self.highlight_frect,
            1
        )

    def draw_rect(self):
        pg.draw.rect(
            NATIVE_SURFACE,
            "white",
            self.highlight_frect,
            1
        )

    def draw(self, dt):
        self.total_dt += dt
        if self.total_dt >= 100:
            self.total_dt = 0
            self.frame_index += 1
            if self.frame_index > len(self.frames_list) - 1:
                self.frame_index = 0
        draw_position_x = self.frect.x - CAM_FRECT.x
        draw_position_y = self.frect.y - CAM_FRECT.y
        # Flame
        NATIVE_SURFACE.blit(
            SPRITE_SHEET_SURFACE,
            (
                draw_position_x,
                draw_position_y - 32
            ),
            self.frames_list[self.frame_index]
        )
        # Body
        NATIVE_SURFACE.blit(
            SPRITE_SHEET_SURFACE,
            (
                draw_position_x,
                draw_position_y - 16
            ),
            self.body_region
        )

    def draw_preview(self, dt, position):
        self.total_dt += dt
        if self.total_dt >= 100:
            self.total_dt = 0
            self.frame_index += 1
            if self.frame_index > len(self.frames_list) - 1:
                self.frame_index = 0
        draw_position_x = position[0]
        draw_position_y = position[1]
        # Flame
        NATIVE_SURFACE.blit(
            ALPHA_SPRITE_SHEET_SURFACE,
            (
                draw_position_x,
                draw_position_y - 32
            ),
            self.frames_list[self.frame_index]
        )
        # Body
        NATIVE_SURFACE.blit(
            ALPHA_SPRITE_SHEET_SURFACE,
            (
                draw_position_x,
                draw_position_y - 16
            ),
            self.body_region
        )
        self.preview_frect.x = position[0]
        self.preview_frect.y = position[1] - 32
        pg.draw.rect(
            NATIVE_SURFACE,
            "red",
            self.preview_frect,
            1
        )


# Preview
floor = Floor((0, 0))
stone = Stone((0, 0))
scone = Scone((0, 0))

# Sky sprite
sky = Sky((0, 0))

# Cloud sprite
cloud = Cloud((0, 0))

# Trees sprite
trees = Trees((0, 0))

# Glow sprite
glow = Glow((0, 0))


# Menu page 1
menu_collisions_list_1 = []
for _ in range(TOTAL_TILES):
    menu_collisions_list_1.append(0)

# Add floor
x = 1
y = 1
sprite = Floor(
    (
        x * TILE_SIZE,
        y * TILE_SIZE
    )
)
menu_collisions_list_1[y * HORIZONTAL_TILES + x] = sprite

# Add stone
x = 3
y = 1
sprite = Stone(
    (
        x * TILE_SIZE,
        y * TILE_SIZE
    )
)
menu_collisions_list_1[y * HORIZONTAL_TILES + x] = sprite

# Menu page 2
menu_collisions_list_2 = []
for _ in range(TOTAL_TILES):
    menu_collisions_list_2.append(0)

# Add scone
x = 1
y = 1
sprite = Scone(
    (
        x * TILE_SIZE,
        y * TILE_SIZE
    )
)
menu_collisions_list_2[y * HORIZONTAL_TILES + x] = sprite

#  Menu pages
menu_pages_list = [
    menu_collisions_list_1,
    menu_collisions_list_2
]
menu_page_index = 0

# Room settings
ROOM_TL_ROOM_UNIT = (0, 0)
ROOM_SCALE = (1, 1)
ROOM_W_TILE_UNIT = 20 * ROOM_SCALE[0]
ROOM_H_TILE_UNIT = 11 * ROOM_SCALE[1]
ROOM_TL_TILE_UNIT = (
    ROOM_TL_ROOM_UNIT[0] * 20,
    ROOM_TL_ROOM_UNIT[1] * 11
)
ROOM_TL = (
    ROOM_TL_ROOM_UNIT[0] * 320,
    ROOM_TL_ROOM_UNIT[1] * 176
)
ROOM_W = ROOM_W_TILE_UNIT * TILE_SIZE
ROOM_H = ROOM_H_TILE_UNIT * TILE_SIZE
ROOM_FRECT = pg.FRect(
    ROOM_TL[0],
    ROOM_TL[1],
    ROOM_W,
    ROOM_H
)
CAM_FRECT.topleft = ROOM_TL
room = []
total = ROOM_W_TILE_UNIT * ROOM_H_TILE_UNIT
for _ in range(total):
    room.append(0)
ROOMS_LIST = [
    room.copy(),  # 0 - tall_bush
    room.copy(),  # 1 - short_bush
    room.copy(),  # 2 - rocks
    room.copy(),  # 3 - wall
    room.copy(),  # 4 - furniture
    room.copy(),  # 5 - small_trees
    room.copy(),  # 6 - pillar
    room.copy(),  # 7 - thin
    room.copy(),  # 8 - scones
    room.copy(),  # 9 - balcony
    room.copy(),  # 10 - floor
    room.copy(),  # 11 - grass
    room.copy(),  # 12 - water
]

selected_sprite = "floor"


def draw_grid():
    # Clear tile grid surface
    TILE_GRID_SURFACE.fill("red")

    # Horizontal tile grid lines
    for i in range(20):
        line_position_x = -1 - CAM_FRECT.x + (TILE_SIZE * i)
        line_position_x = line_position_x % NATIVE_RECT.width
        pg.draw.line(
            TILE_GRID_SURFACE,
            "grey96",
            (line_position_x, NATIVE_RECT.top),
            (line_position_x, NATIVE_RECT.bottom),
            2
        )

    # Vertical tile grid lines
    for i in range(20):
        line_position_y = -1 - CAM_FRECT.y + (TILE_SIZE * i)
        line_position_y = line_position_y % NATIVE_RECT.height
        pg.draw.line(
            TILE_GRID_SURFACE,
            "grey96",
            (NATIVE_RECT.left, line_position_y),
            (NATIVE_RECT.right, line_position_y),
            2
        )

    # Draw tile grid surface to native
    NATIVE_SURFACE.blit(
        TILE_GRID_SURFACE,
        (0, 0)
    )

    # Clear room grid surface
    ROOM_GRID_SURFACE.fill("red")

    # Horizontal room grid lines
    line_position_x = -1 - CAM_FRECT.x
    line_position_x = line_position_x % NATIVE_RECT.width
    pg.draw.line(
        ROOM_GRID_SURFACE,
        "grey92",
        (line_position_x, NATIVE_RECT.top),
        (line_position_x, NATIVE_RECT.bottom),
        2
    )

    # Vertical room grid lines
    line_position_y = -1 - CAM_FRECT.y
    line_position_y = line_position_y % NATIVE_RECT.height
    pg.draw.line(
        ROOM_GRID_SURFACE,
        "grey92",
        (NATIVE_RECT.left, line_position_y),
        (NATIVE_RECT.right, line_position_y),
        2
    )

    # Draw room grid surface to native
    NATIVE_SURFACE.blit(
        ROOM_GRID_SURFACE,
        (0, 0)
    )

    # Draw origin
    ORIGIN_RECT.x = -1 - CAM_FRECT.x
    ORIGIN_RECT.y = -1 - CAM_FRECT.y
    pg.draw.rect(
        NATIVE_SURFACE,
        "red",
        ORIGIN_RECT,
        1
    )

    # Room rect draw
    ROOM_FRECT.x = ROOM_TL[0] - CAM_FRECT.x
    ROOM_FRECT.y = ROOM_TL[1] - CAM_FRECT.y
    pg.draw.rect(
        NATIVE_SURFACE,
        "red",
        ROOM_FRECT,
        1
    )

    # Horizontal ruler text
    ruler_x_text = int(CAM_FRECT.x // NATIVE_RECT.width) + 1
    rulex_x_rect = FONT.get_rect(f"{ruler_x_text}")
    rulex_x_rect.midtop = (line_position_x, 5)
    FONT.render_to(
        NATIVE_SURFACE,
        (
            rulex_x_rect.x,
            rulex_x_rect.y
        ),
        f"{ruler_x_text}",
        "white"
    )

    # Vertical ruler text
    ruler_y_text = int(CAM_FRECT.y // NATIVE_RECT.height) + 1
    ruler_y_rect = FONT.get_rect(f"{ruler_y_text}")
    ruler_y_rect.midleft = (3, line_position_y)
    FONT.render_to(
        NATIVE_SURFACE,
        (
            ruler_y_rect.x,
            ruler_y_rect.y
        ),
        f"{ruler_y_text}",
        "white"
    )


def update_camera_position(direction, cam_velocity, CAM_FRECT, dt, CAM_SPEED, CAM_LERP_WEIGHT):
    # Update cam direction
    direction.x = pg.key.get_pressed()[pg.K_d] - pg.key.get_pressed()[pg.K_a]
    direction.y = pg.key.get_pressed()[pg.K_s] - pg.key.get_pressed()[pg.K_w]
    if direction.length() != 0:
        direction = direction.normalize()

    # Update cam velocity with cam direction
    cam_velocity = cam_velocity.smoothstep(
        direction * CAM_SPEED, CAM_LERP_WEIGHT
    )
    if cam_velocity.length() < 0.001:
        cam_velocity.x = 0
        cam_velocity.y = 0

    # Update cam position with cam velocity
    CAM_FRECT.topleft += cam_velocity * dt

    return direction, cam_velocity, CAM_FRECT


def update_bitmasks(tile, position_tile_unit, last=False):
    # Raw bits
    br, b, bl, r, l, tr, t, tl = 0, 0, 0, 0, 0, 0, 0, 0

    x = position_tile_unit[0]
    y = position_tile_unit[1]
    neighbour_tile_units = [
        (x - 1, y - 1), (x - 0, y - 1), (x + 1, y - 1),
        (x - 1, y - 0),                 (x + 1, y - 0),
        (x - 1, y + 1), (x - 0, y + 1), (x + 1, y + 1)
    ]
    for pos in neighbour_tile_units:
        # Get tile from map
        if (0 <= pos[0] < ROOM_W_TILE_UNIT) and (0 <= pos[1] < ROOM_H_TILE_UNIT):
            neighbour = ROOMS_LIST[10][
                pos[1] * ROOM_W_TILE_UNIT + pos[0]]

            # Air? check other position
            if neighbour == 0:
                continue

            # Tell my neighbour to update their frame index
            if last == False:
                update_bitmasks(
                    neighbour,
                    pos,
                    last=True
                )

            dx = neighbour.frect.x - tile.frect.x
            dy = neighbour.frect.y - tile.frect.y
            t += dx == 0 and dy == -TILE_SIZE
            r += dx == TILE_SIZE and dy == 0
            b += dx == 0 and dy == TILE_SIZE
            l += dx == -TILE_SIZE and dy == 0
            br += dx == TILE_SIZE and dy == TILE_SIZE
            bl += dx == -TILE_SIZE and dy == TILE_SIZE
            tr += dx == TILE_SIZE and dy == -TILE_SIZE
            tl += dx == -TILE_SIZE and dy == -TILE_SIZE
    tr = tr and t and r
    tl = tl and t and l
    br = br and b and r
    bl = bl and b and l
    mask_id = (br << 7) | (b << 6) | (bl << 5) | (
        r << 4) | (l << 3) | (tr << 2) | (t << 1) | tl

    # Update frame index with cooked bitmask
    if mask_id != 0:
        tile.frame_mask_key = mask_id


is_lmb_pressed = False

# Main loop
while 1:
    # Dt
    dt = CLOCK.tick(FPS)

    # Get event
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            # Lmb
            if event.button == 1:
                is_lmb_pressed = True

        elif event.type == pg.MOUSEBUTTONUP:
            # Lmb
            if event.button == 1:
                is_lmb_pressed = False
                # Menu state
                if is_menu:
                    # Lmb
                    if event.button == 1:
                        pos = pg.mouse.get_pos()
                        pos = (
                            pos[0] // RESOLUTION_SCALE // TILE_SIZE,
                            pos[1] // RESOLUTION_SCALE // TILE_SIZE
                        )
                        cell = menu_pages_list[menu_page_index][
                            pos[1] * HORIZONTAL_TILES + pos[0]
                        ]
                        selected_sprite = cell.name
                        is_menu = not is_menu

    # Toggle menu
    if pg.key.get_just_pressed()[pg.K_q]:
        is_menu = not is_menu

    # Clear draw
    NATIVE_SURFACE.fill("grey0")

    # Menu state
    if is_menu:
        # draw menu items
        for cell in menu_pages_list[menu_page_index]:
            if cell == 0:
                continue
            cell.global_draw(dt)

        # Cycle menu pages
        menu_page_index += pg.key.get_just_pressed(
        )[pg.K_d] - pg.key.get_just_pressed()[pg.K_a]
        menu_page_index = menu_page_index % len(menu_pages_list)

        # Draw rect on hover
        pos = pg.mouse.get_pos()
        pos = (
            pos[0] // RESOLUTION_SCALE // TILE_SIZE,
            pos[1] // RESOLUTION_SCALE // TILE_SIZE
        )
        cell = menu_pages_list[menu_page_index][
            pos[1] * HORIZONTAL_TILES + pos[0]
        ]
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        if cell != 0:
            cell.draw_rect()
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)

    # Normal state
    else:
        # Update camera position
        direction, cam_velocity, CAM_FRECT = update_camera_position(
            direction, cam_velocity, CAM_FRECT, dt, CAM_SPEED, CAM_LERP_WEIGHT
        )

        # Draw background
        sky.draw()
        cloud.draw()
        trees.draw()
        glow.draw()
        draw_grid()

        # Draw sprites
        for room in ROOMS_LIST:
            for cell in room:
                if cell == 0:
                    continue

                cell.draw(dt)

        # Render selected sprite preview
        pos = pg.mouse.get_pos()
        pos = (
            pos[0] // RESOLUTION_SCALE,
            pos[1] // RESOLUTION_SCALE
        )
        render_pos_snapped_tile_unit = (
            int((pos[0] + CAM_FRECT.x) // TILE_SIZE),
            int((pos[1] + CAM_FRECT.y) // TILE_SIZE)
        )
        render_pos_snapped = (
            (render_pos_snapped_tile_unit[0] * TILE_SIZE),
            (render_pos_snapped_tile_unit[1] * TILE_SIZE)
        )
        x = render_pos_snapped[0] - CAM_FRECT.x
        y = render_pos_snapped[1] - CAM_FRECT.y
        if selected_sprite == "floor":
            floor.draw_preview(dt, (x, y))
        elif selected_sprite == "stone":
            stone.draw_preview(dt, (x, y))
        elif selected_sprite == "scone":
            scone.draw_preview(dt, (x, y))

        # Lmb pressed
        if is_lmb_pressed:
            pos = pg.mouse.get_pos()
            pos = (
                pos[0] // RESOLUTION_SCALE,
                pos[1] // RESOLUTION_SCALE
            )
            render_pos_snapped_tile_unit = (
                int((pos[0] + CAM_FRECT.x) // TILE_SIZE),
                int((pos[1] + CAM_FRECT.y) // TILE_SIZE)
            )
            render_pos_snapped = (
                (render_pos_snapped_tile_unit[0] * TILE_SIZE),
                (render_pos_snapped_tile_unit[1] * TILE_SIZE)
            )
            x = render_pos_snapped_tile_unit[0] - ROOM_TL_TILE_UNIT[0]
            y = render_pos_snapped_tile_unit[1] - ROOM_TL_TILE_UNIT[1]
            if (0 <= x < ROOM_W_TILE_UNIT) and (0 <= y < ROOM_H_TILE_UNIT):
                if selected_sprite == "floor":
                    cell = ROOMS_LIST[10][
                        y * ROOM_W_TILE_UNIT + x]
                    if cell == 0:
                        sprite = Floor(
                            (
                                render_pos_snapped[0],
                                render_pos_snapped[1]
                            )
                        )
                        ROOMS_LIST[10][
                            y * ROOM_W_TILE_UNIT + x
                        ] = sprite
                        update_bitmasks(sprite, (x, y))

                elif selected_sprite == "stone":
                    cell = ROOMS_LIST[10][
                        y * ROOM_W_TILE_UNIT + x]
                    if cell == 0:
                        sprite = Stone(
                            (
                                render_pos_snapped[0],
                                render_pos_snapped[1]
                            )
                        )
                        ROOMS_LIST[10][
                            y * ROOM_W_TILE_UNIT + x
                        ] = sprite
                        update_bitmasks(sprite, (x, y))

                elif selected_sprite == "scone":
                    cell = ROOMS_LIST[8][
                        y * ROOM_W_TILE_UNIT + x]
                    if cell == 0:
                        sprite = Scone(
                            (
                                render_pos_snapped[0],
                                render_pos_snapped[1]
                            )
                        )
                        ROOMS_LIST[8][
                            y * ROOM_W_TILE_UNIT + x
                        ] = sprite

    # Scale native to window
    pg.transform.scale(
        NATIVE_SURFACE,
        (DISPLAY_RECT.width, DISPLAY_RECT.height),
        DISPLAY_SURFACE
    )

    # Update window
    pg.display.update()
