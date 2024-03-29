import pygame as pg
import pygame.freetype as font
from sys import exit
from json import dump
from json import load
from os.path import join

pg.init()

# Starts with loaded data
# On save will save both the editor load save and the in game load save

# region Room editor settings
room_dict = {}
ROOM_NAME = input("Load data room name?")
PATH = join("room_json_data_load", "stage_1", f"{ROOM_NAME}.json")
with open(PATH, 'r') as json_file:
    room_dict = load(json_file)
RESOLUTION = room_dict["RESOLUTION"]
ROOM_X_RU = room_dict["ROOM_X_RU"]
ROOM_Y_RU = room_dict["ROOM_Y_RU"]
ROOM_SCALE_X = room_dict["ROOM_SCALE_X"]
ROOM_SCALE_Y = room_dict["ROOM_SCALE_Y"]
STAGE_NO = room_dict["STAGE_NO"]
ROOM_NAME = room_dict["ROOM_NAME"]
STAGES = {
    1: {
        "SPRITE_SHEET_PNG_NAME": "stage_1_sprite_sheet.png",
        "TOTAL_LAYERS": 15,
        "TILE_S": 16,
        "BITMASK_TYPE_SPRITE_NAMES": ["Floor", "Rock", "BgRock", "Pillar", "Balcony", "Rail", "BalconySupport", "WallFence", "BigWindow", "WallWindow", "Window", "VPillar", "HPillar"],
        "V_BITMASK_TYPE_SPRITE_NAMES": ["Pillar", "BalconySupport", "HPillar"],
        "H_BITMASK_TYPE_SPRITE_NAMES": ["Balcony", "Rail", "WallFence", "VPillar"],
        "MIX_BITMASK_TYPE_SPRITE_NAMES": ["Floor", "Rock"],
        "COLIISION_LAYER_I": 12,
        "SAVE_PATH": join("room_json_data", "stage_1", f"{ROOM_NAME}.json"),
        "SAVE_PATH_LOAD": join("room_json_data_load", "stage_1", f"{ROOM_NAME}.json"),
        "SPRITES": [
            {
                "name": "Floor",
                "xds": 0,
                "yds": 0,
                "layer_i": 12,
                "regions": {
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
                "region": (368, 48, 16, 16)
            },
            {
                "name": "Rock",
                "xds": 0,
                "yds": 0,
                "layer_i": 12,
                "regions": {
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
                "region": (368, 128, 16, 16)
            },
            {
                "name": "BgRock",
                "xds": 0,
                "yds": 0,
                "layer_i": 0,
                "regions": {
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
                },
                "region": (368, 208, 16, 16)
            },
            {
                "name": "TallBush",
                "xds": 0,
                "yds": 0,
                "layer_i": 1,
                "region": (320, 240, 176, 32)
            },
            {
                "name": "ShortBush",
                "xds": 0,
                "yds": 0,
                "layer_i": 2,
                "region": (320, 272, 112, 32)
            },
            {
                "name": "Boulder",
                "xds": 0,
                "yds": 0,
                "layer_i": 3,
                "region": (432, 272, 48, 32)
            },
            {
                "name": "VPillar",
                "xds": 0,
                "yds": 0,
                "layer_i": 5,
                "regions": {
                    208: 0,
                    248: 0,
                    104: 0,
                    64: 0,
                    80: 0,
                    120: 0,
                    216: 0,
                    72: 0,
                    88: 0,
                    219: 0,

                    214: 0,
                    255: 0,
                    107: 0,
                    66: 0,
                    86: 0,
                    127: 0,
                    223: 0,
                    75: 0,
                    95: 0,
                    126: 0,

                    22: 0,
                    31: 0,
                    11: 0,
                    2: 0,
                    210: 0,
                    251: 0,
                    254: 0,
                    106: 0,
                    250: 0,
                    218: 0,
                    122: 0,

                    16: (320, 304, 16, 16),
                    24: 0,
                    8: (336, 304, 16, 16),
                    0: 0,
                    18: 0,
                    27: 0,
                    30: 0,
                    10: 0,
                    26: 0,
                    94: 0,
                    91: 0,

                    82: 0,
                    123: 0,
                    222: 0,
                    74: 0,
                    90: 0,
                },
                "region": (320, 304, 16, 16)
            },
            {
                "name": "Pillar",
                "xds": 0,
                "yds": 0,
                "layer_i": 5,
                "regions": {
                    208: 0,
                    248: 0,
                    104: 0,
                    64: (320, 320, 16, 16),
                    80: 0,
                    120: 0,
                    216: 0,
                    72: 0,
                    88: 0,
                    219: 0,

                    214: 0,
                    255: 0,
                    107: 0,
                    66: (320, 336, 16, 16),
                    86: 0,
                    127: 0,
                    223: 0,
                    75: 0,
                    95: 0,
                    126: 0,

                    22: 0,
                    31: 0,
                    11: 0,
                    2: (320, 352, 16, 16),
                    210: 0,
                    251: 0,
                    254: 0,
                    106: 0,
                    250: 0,
                    218: 0,
                    122: 0,

                    16: 0,
                    24: 0,
                    8: 0,
                    0: 0,
                    18: 0,
                    27: 0,
                    30: 0,
                    10: 0,
                    26: 0,
                    94: 0,
                    91: 0,

                    82: 0,
                    123: 0,
                    222: 0,
                    74: 0,
                    90: 0,
                },
                "region": (320, 320, 16, 16)
            },
            {
                "name": "BrokenWall",
                "xds": 0,
                "yds": 0,
                "layer_i": 5,
                "region": (336, 320, 16, 16)
            },
            {
                "name": "Wall",
                "xds": 0,
                "yds": 0,
                "layer_i": 5,
                "region": (336, 336, 16, 16)
            },
            {
                "name": "SmallTree",
                "xds": 0,
                "yds": 0,
                "layer_i": 4,
                "region": (352, 304, 48, 64)
            },
            {
                "name": "SmallerTree",
                "xds": 0,
                "yds": 0,
                "layer_i": 4,
                "region": (400, 320, 32, 48)
            },
            {
                "name": "BigPillarTop",
                "xds": 0,
                "yds": 0,
                "layer_i": 6,
                "region": (432, 304, 32, 32)
            },
            {
                "name": "BigPillarMid",
                "xds": 0,
                "yds": 0,
                "layer_i": 6,
                "region": (432, 336, 32, 16)
            },
            {
                "name": "BigPillarBot",
                "xds": 0,
                "yds": 0,
                "layer_i": 6,
                "region": (432, 352, 32, 16)
            },
            {
                "name": "ThinTop",
                "xds": 0,
                "yds": 0,
                "layer_i": 12,
                "region": (464, 304, 32, 48)
            },
            {
                "name": "ThinMid",
                "xds": 0,
                "yds": 0,
                "layer_i": 11,
                "region": (432, 416, 32, 16)
            },
            {
                "name": "ThinBot",
                "xds": 0,
                "yds": 0,
                "layer_i": 11,
                "region": (464, 352, 32, 16)
            },
            {
                "name": "Window",
                "xds": 0,
                "yds": 0,
                "layer_i": 5,
                "regions": {
                    208: (432, 368, 16, 16),
                    248: 0,
                    104: (448, 368, 16, 16),
                    64: 0,
                    80: 0,
                    120: 0,
                    216: 0,
                    72: 0,
                    88: 0,
                    219: 0,

                    214: 0,
                    255: 0,
                    107: 0,
                    66: 0,
                    86: 0,
                    127: 0,
                    223: 0,
                    75: 0,
                    95: 0,
                    126: 0,

                    22: (432, 384, 16, 16),
                    31: 0,
                    11: (448, 384, 16, 16),
                    2: 0,
                    210: 0,
                    251: 0,
                    254: 0,
                    106: 0,
                    250: 0,
                    218: 0,
                    122: 0,

                    16: 0,
                    24: 0,
                    8: 0,
                    0: 0,
                    18: 0,
                    27: 0,
                    30: 0,
                    10: 0,
                    26: 0,
                    94: 0,
                    91: 0,

                    82: 0,
                    123: 0,
                    222: 0,
                    74: 0,
                    90: 0,
                },
                "region": (432, 368, 16, 16)
            },
            {
                "name": "Furnace",
                "xds": 0,
                "yds": 0,
                "layer_i": 8,
                "region": (464, 368, 32, 32)
            },
            {
                "name": "Scone",
                "xds": 0,
                "yds": 0,
                "layer_i": 10,
                "region": (400, 368, 16, 32)
            },
            {
                "name": "ThinScone",
                "xds": 0,
                "yds": 0,
                "layer_i": 10,
                "region": (416, 368, 16, 32)
            },
            {
                "name": "Furniture",
                "xds": 0,
                "yds": 0,
                "layer_i": 9,
                "region": (400, 432, 64, 32)
            },
            {
                "name": "HPillar",
                "xds": 0,
                "yds": 0,
                "layer_i": 5,
                "regions": {
                    208: 0,
                    248: 0,
                    104: 0,
                    64: (464, 432, 16, 16),
                    80: 0,
                    120: 0,
                    216: 0,
                    72: 0,
                    88: 0,
                    219: 0,

                    214: 0,
                    255: 0,
                    107: 0,
                    66: 0,
                    86: 0,
                    127: 0,
                    223: 0,
                    75: 0,
                    95: 0,
                    126: 0,

                    22: 0,
                    31: 0,
                    11: 0,
                    2: (464, 448, 16, 16),
                    210: 0,
                    251: 0,
                    254: 0,
                    106: 0,
                    250: 0,
                    218: 0,
                    122: 0,

                    16: 0,
                    24: 0,
                    8: 0,
                    0: 0,
                    18: 0,
                    27: 0,
                    30: 0,
                    10: 0,
                    26: 0,
                    94: 0,
                    91: 0,

                    82: 0,
                    123: 0,
                    222: 0,
                    74: 0,
                    90: 0,
                },
                "region": (464, 432, 16, 16)
            },
            {
                "name": "Gate",
                "xds": 0,
                "yds": 0,
                "layer_i": 12,
                "region": (384, 432, 16, 16)
            },
            {
                "name": "Balcony",
                "xds": 0,
                "yds": 0,
                "layer_i": 12,
                "regions": {
                    208: 0,
                    248: 0,
                    104: 0,
                    64: 0,
                    80: 0,
                    120: 0,
                    216: 0,
                    72: 0,
                    88: 0,
                    219: 0,

                    214: 0,
                    255: 0,
                    107: 0,
                    66: 0,
                    86: 0,
                    127: 0,
                    223: 0,
                    75: 0,
                    95: 0,
                    126: 0,

                    22: 0,
                    31: 0,
                    11: 0,
                    2: 0,
                    210: 0,
                    251: 0,
                    254: 0,
                    106: 0,
                    250: 0,
                    218: 0,
                    122: 0,

                    16: (320, 384, 16, 16),
                    24: (336, 384, 16, 16),
                    8: (352, 384, 16, 16),
                    0: 0,
                    18: 0,
                    27: 0,
                    30: 0,
                    10: 0,
                    26: 0,
                    94: 0,
                    91: 0,

                    82: 0,
                    123: 0,
                    222: 0,
                    74: 0,
                    90: 0,
                },
                "region": (320, 384, 16, 16)
            },
            {
                "name": "Rail",
                "xds": 0,
                "yds": 0,
                "layer_i": 13,
                "regions": {
                    208: 0,
                    248: 0,
                    104: 0,
                    64: 0,
                    80: 0,
                    120: 0,
                    216: 0,
                    72: 0,
                    88: 0,
                    219: 0,

                    214: 0,
                    255: 0,
                    107: 0,
                    66: 0,
                    86: 0,
                    127: 0,
                    223: 0,
                    75: 0,
                    95: 0,
                    126: 0,

                    22: 0,
                    31: 0,
                    11: 0,
                    2: 0,
                    210: 0,
                    251: 0,
                    254: 0,
                    106: 0,
                    250: 0,
                    218: 0,
                    122: 0,

                    16: (320, 368, 16, 16),
                    24: (336, 368, 16, 16),
                    8: (352, 368, 16, 16),
                    0: 0,
                    18: 0,
                    27: 0,
                    30: 0,
                    10: 0,
                    26: 0,
                    94: 0,
                    91: 0,

                    82: 0,
                    123: 0,
                    222: 0,
                    74: 0,
                    90: 0,
                },
                "region": (320, 368, 16, 16)
            },
            {
                "name": "BalconySupport",
                "xds": 0,
                "yds": 0,
                "layer_i": 11,
                "regions": {
                    208: 0,
                    248: 0,
                    104: 0,
                    64: (320, 400, 16, 16),
                    80: 0,
                    120: 0,
                    216: 0,
                    72: 0,
                    88: 0,
                    219: 0,

                    214: 0,
                    255: 0,
                    107: 0,
                    66: (320, 416, 16, 16),
                    86: 0,
                    127: 0,
                    223: 0,
                    75: 0,
                    95: 0,
                    126: 0,

                    22: 0,
                    31: 0,
                    11: 0,
                    2: (320, 432, 16, 16),
                    210: 0,
                    251: 0,
                    254: 0,
                    106: 0,
                    250: 0,
                    218: 0,
                    122: 0,

                    16: 0,
                    24: 0,
                    8: 0,
                    0: 0,
                    18: 0,
                    27: 0,
                    30: 0,
                    10: 0,
                    26: 0,
                    94: 0,
                    91: 0,

                    82: 0,
                    123: 0,
                    222: 0,
                    74: 0,
                    90: 0,
                },
                "region": (320, 400, 16, 16)
            },
            {
                "name": "Grass",
                "xds": 0,
                "yds": 0,
                "layer_i": 14,
                "region": (368, 368, 32, 32)
            },
            {
                "name": "WallFence",
                "xds": 0,
                "yds": 0,
                "layer_i": 5,
                "regions": {
                    208: 0,
                    248: 0,
                    104: 0,
                    64: 0,
                    80: 0,
                    120: 0,
                    216: 0,
                    72: 0,
                    88: 0,
                    219: 0,

                    214: 0,
                    255: 0,
                    107: 0,
                    66: 0,
                    86: 0,
                    127: 0,
                    223: 0,
                    75: 0,
                    95: 0,
                    126: 0,

                    22: 0,
                    31: 0,
                    11: 0,
                    2: 0,
                    210: 0,
                    251: 0,
                    254: 0,
                    106: 0,
                    250: 0,
                    218: 0,
                    122: 0,

                    16: (336, 432, 16, 16),
                    24: (352, 432, 16, 16),
                    8: (368, 432, 16, 16),
                    0: 0,
                    18: 0,
                    27: 0,
                    30: 0,
                    10: 0,
                    26: 0,
                    94: 0,
                    91: 0,

                    82: 0,
                    123: 0,
                    222: 0,
                    74: 0,
                    90: 0,
                },
                "region": (336, 432, 16, 16)
            },
            {
                "name": "Fire",
                "xds": 0,
                "yds": 0,
                "layer_i": 10,
                "regions": [
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
                ],
                "region": (336, 400, 16, 16)
            },
            {
                "name": "BigWindow",
                "xds": 0,
                "yds": 0,
                "layer_i": 5,
                "regions": {
                    208: (400, 464, 16, 16),
                    248: (416, 464, 16, 16),
                    104: (432, 464, 16, 16),
                    64: 0,
                    80: 0,
                    120: 0,
                    216: 0,
                    72: 0,
                    88: 0,
                    219: 0,

                    214: (400, 480, 16, 16),
                    255: (416, 496, 16, 16),
                    107: (432, 480, 16, 16),
                    66: 0,
                    86: 0,
                    127: 0,
                    223: 0,
                    75: 0,
                    95: 0,
                    126: 0,

                    22: (400, 496, 16, 16),
                    31: (416, 496, 16, 16),
                    11: (432, 496, 16, 16),
                    2: 0,
                    210: 0,
                    251: 0,
                    254: 0,
                    106: 0,
                    250: 0,
                    218: 0,
                    122: 0,

                    16: 0,
                    24: 0,
                    8: 0,
                    0: 0,
                    18: 0,
                    27: 0,
                    30: 0,
                    10: 0,
                    26: 0,
                    94: 0,
                    91: 0,

                    82: 0,
                    123: 0,
                    222: 0,
                    74: 0,
                    90: 0,
                },
                "region": (416, 496, 16, 16)
            },
            {
                "name": "BigWindowLamp",
                "xds": 0,
                "yds": 0,
                "layer_i": 5,
                "region": (416, 480, 16, 16)
            },
            {
                "name": "WallWindow",
                "xds": 0,
                "yds": 0,
                "layer_i": 5,
                "regions": {
                    208: (448, 464, 16, 16),
                    248: (464, 464, 16, 16),
                    104: (480, 464, 16, 16),
                    64: 0,
                    80: 0,
                    120: 0,
                    216: 0,
                    72: 0,
                    88: 0,
                    219: 0,

                    214: (448, 480, 16, 16),
                    255: (464, 496, 16, 16),
                    107: (480, 480, 16, 16),
                    66: 0,
                    86: 0,
                    127: 0,
                    223: 0,
                    75: 0,
                    95: 0,
                    126: 0,

                    22: (448, 496, 16, 16),
                    31: (464, 496, 16, 16),
                    11: (480, 496, 16, 16),
                    2: 0,
                    210: 0,
                    251: 0,
                    254: 0,
                    106: 0,
                    250: 0,
                    218: 0,
                    122: 0,

                    16: 0,
                    24: 0,
                    8: 0,
                    0: 0,
                    18: 0,
                    27: 0,
                    30: 0,
                    10: 0,
                    26: 0,
                    94: 0,
                    91: 0,

                    82: 0,
                    123: 0,
                    222: 0,
                    74: 0,
                    90: 0,
                },
                "region": (464, 496, 16, 16)
            },
            {
                "name": "WallWindowLamp",
                "xds": 0,
                "yds": 0,
                "layer_i": 5,
                "region": (464, 480, 16, 16)
            },
            {
                "name": "Door",
                "xds": 0,
                "yds": 0,
                "layer_i": 5,
                "region": (400, 512, 32, 64)
            },
            {
                "name": "CurtainLeft",
                "xds": 0,
                "yds": 0,
                "layer_i": 7,
                "region": (432, 512, 32, 80)
            },
            {
                "name": "CurtainRight",
                "xds": 0,
                "yds": 0,
                "layer_i": 7,
                "region": (464, 512, 32, 80)
            },
            {
                "name": "Door",
                "id": "",
                "target": "",
                "xds": 0,
                "yds": 0,
                "layer_i": 12,
                "region": (320, 608, 16, 16)
            },
            {
                "name": "Door",
                "id": "",
                "target": "",
                "xds": 0,
                "yds": 0,
                "layer_i": 12,
                "region": (336, 608, 16, 16)
            },
            {
                "name": "Door",
                "id": "",
                "target": "",
                "xds": 0,
                "yds": 0,
                "layer_i": 12,
                "region": (352, 608, 16, 16)
            },
            {
                "name": "Door",
                "id": "",
                "target": "",
                "xds": 0,
                "yds": 0,
                "layer_i": 12,
                "region": (368, 608, 16, 16)
            },
        ]
    }
}
STAGE = STAGES[STAGE_NO]
SPRITE_SHEET_PNG_NAME = STAGE["SPRITE_SHEET_PNG_NAME"]
TOTAL_LAYERS = STAGE["TOTAL_LAYERS"]
TILE_S = STAGE["TILE_S"]
BITMASK_TYPE_SPRITE_NAMES = STAGE["BITMASK_TYPE_SPRITE_NAMES"]
V_BITMASK_TYPE_SPRITE_NAMES = STAGE["V_BITMASK_TYPE_SPRITE_NAMES"]
H_BITMASK_TYPE_SPRITE_NAMES = STAGE["H_BITMASK_TYPE_SPRITE_NAMES"]
MIX_BITMASK_TYPE_SPRITE_NAMES = STAGE["MIX_BITMASK_TYPE_SPRITE_NAMES"]
COLLISION_LAYER_I = STAGE["COLIISION_LAYER_I"]
SAVE_PATH = STAGE["SAVE_PATH"]
SAVE_PATH_LOAD = STAGE["SAVE_PATH_LOAD"]
SPRITES = STAGE["SPRITES"]
SPRITES_LEN = len(SPRITES)
# endregion

# region Constants
ADD_CURSOR_PNG_NAME = "add_cursor.png"
DEL_CURSOR_PNG_NAME = "del_cursor.png"
FONT_H = 5
FONT_W = 3
FPS = 30
NATIVE_W_TU = 20
NATIVE_H_TU = 11
NATIVE_W = TILE_S * NATIVE_W_TU
NATIVE_H = TILE_S * NATIVE_H_TU
WINDOW_W = NATIVE_W * RESOLUTION
WINDOW_H = NATIVE_H * RESOLUTION
CAM_SPD = 4
WINDOW_SURF = pg.display.set_mode((WINDOW_W, WINDOW_H))
NATIVE_SURF = pg.Surface((NATIVE_W, NATIVE_H))
CLOCK = pg.time.Clock()
FONT = font.Font("cg_pixel_3x5_mono.ttf", FONT_H)
EVENTS = [pg.KEYDOWN, pg.KEYUP, pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.QUIT]
CAM_RECT = pg.Rect(0, 0, NATIVE_W, NATIVE_H)
SPRITE_SHEET_SURF = pg.image.load(SPRITE_SHEET_PNG_NAME).convert_alpha()
ROOM_X_TU = ROOM_X_RU * NATIVE_W_TU
ROOM_Y_TU = ROOM_Y_RU * NATIVE_H_TU
ROOM_W_TU = ROOM_SCALE_X * NATIVE_W_TU
ROOM_H_TU = ROOM_SCALE_Y * NATIVE_H_TU
ROOM_RECT = pg.Rect(ROOM_X_TU * TILE_S, ROOM_Y_TU * TILE_S,
                    ROOM_W_TU * TILE_S, ROOM_H_TU * TILE_S)
CAM_RECT.topleft = ROOM_RECT.topleft
LAYERS_LIST = room_dict["LAYERS_LIST"]
LIGHT_SURF = pg.Surface((NATIVE_W, NATIVE_H))
LIGHT_SURF.fill("white")
LIGHT_SURF.set_alpha(204)
MENU_COLLISIONS = [0 for _ in range(NATIVE_W_TU * NATIVE_H_TU)]
MENU_SURF = pg.Surface((NATIVE_W, NATIVE_H))
MENU_SURF.fill("grey0")
for i in range(SPRITES_LEN):
    sprite = SPRITES[i]
    x_tu = i % NATIVE_W_TU
    y_tu = i // NATIVE_W_TU
    x = x_tu * TILE_S
    y = y_tu * TILE_S
    MENU_COLLISIONS[i] = sprite
    REGION = sprite["region"]
    MENU_SURF.blit(SPRITE_SHEET_SURF, (x, y), (REGION[0], REGION[1], 16, 16))
    for i in range(NATIVE_W_TU + 1):
        v = TILE_S * i
        pg.draw.line(MENU_SURF, "grey4", (v, 0), (v, NATIVE_H))
        pg.draw.line(MENU_SURF, "grey4", (0, v), (NATIVE_W, v))
TALK_SFX = pg.mixer.Sound("talk.wav")
ADD_CURSOR_SURF = pg.image.load(ADD_CURSOR_PNG_NAME).convert_alpha()
ADD_CURSOR_SURF = pg.transform.scale_by(ADD_CURSOR_SURF, RESOLUTION)
ADD_CURSOR = pg.cursors.Cursor(
    (16 * RESOLUTION, 16 * RESOLUTION), ADD_CURSOR_SURF)
DEL_CURSOR_SURF = pg.image.load(DEL_CURSOR_PNG_NAME).convert_alpha()
DEL_CURSOR_SURF = pg.transform.scale_by(DEL_CURSOR_SURF, RESOLUTION)
DEL_CURSOR = pg.cursors.Cursor(
    (16 * RESOLUTION, 16 * RESOLUTION), DEL_CURSOR_SURF)
pg.mouse.set_cursor(ADD_CURSOR)
# endregion

# region Menu vars
# Keep track what state, the selected sprite and selected layer
is_menu = False
selected_sprite = MENU_COLLISIONS[0]
selected_layer = LAYERS_LIST[selected_sprite["layer_i"]]
# endregion

# region Rect draw vars
# Vards needed to keep track for rect drawing style
start_xs = 0
start_ys = 0
top_left = 0
top_right = 0
bottom_left = 0
bottom_right = 0
# endregion

# region Input flags
# All inputs that needs to be tracked are here
is_w_pressed = 0
is_a_pressed = 0
is_s_pressed = 0
is_d_pressed = 0
is_lmb_pressed = False
is_rmb_pressed = False
is_mmb_pressed = False
is_shift_pressed = False
# endregion

# region Helper functions


def update_bitmasks(x_tu, y_tu, xds, yds, last=False):
    # Create a blink effect on tile that mask about to change
    xs = xds - CAM_RECT.x
    ys = yds - CAM_RECT.y
    NATIVE_SURF.blit(LIGHT_SURF, (xs, ys), (0, 0, TILE_S, TILE_S))

    # Raw bits
    br, b, bl, r, l, tr, t, tl = 0, 0, 0, 0, 0, 0, 0, 0

    # Check my neighbour positions
    neighbour_pos_tu = [
        (x_tu - 1, y_tu - 1), (x_tu - 0, y_tu - 1), (x_tu + 1, y_tu - 1),
        (x_tu - 1, y_tu - 0),                       (x_tu + 1, y_tu - 0),
        (x_tu - 1, y_tu + 1), (x_tu - 0, y_tu + 1), (x_tu + 1, y_tu + 1)
    ]
    # Top and bottom checks only
    if selected_sprite["name"] in V_BITMASK_TYPE_SPRITE_NAMES:
        neighbour_pos_tu = [
            (x_tu - 0, y_tu - 1),
            (x_tu - 0, y_tu + 1),
        ]
    # Left and right checks only
    elif selected_sprite["name"] in H_BITMASK_TYPE_SPRITE_NAMES:
        neighbour_pos_tu = [
            (x_tu - 1, y_tu - 0), (x_tu + 1, y_tu - 0),
        ]
    for pos in neighbour_pos_tu:
        # Get tile from collision list
        neighbour_x_tu = pos[0]
        neighbour_y_tu = pos[1]

        # Make sure that pos is inside the list
        if (0 <= neighbour_x_tu < ROOM_W_TU) and (0 <= neighbour_y_tu < ROOM_H_TU):
            neighbour = selected_layer[neighbour_y_tu *
                                       ROOM_W_TU + neighbour_x_tu]

            # Air? check other position
            if neighbour == 0:
                continue

            # Only Floor and Rock mix in the same layer bitmask
            if not selected_sprite["name"] in MIX_BITMASK_TYPE_SPRITE_NAMES:
                if selected_sprite["name"] != neighbour["name"]:
                    continue

            # Found! Tell my neighbour to update bitmask
            if last == False:
                update_bitmasks(
                    neighbour_x_tu, neighbour_y_tu,
                    neighbour["xds"], neighbour["yds"],
                    last=True
                )

            # Cook bitmask -> mask_id
            dx = neighbour_x_tu - x_tu
            dy = neighbour_y_tu - y_tu
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

    # Update region of this tile (passed arg) with cooked bitmask
    sprite = selected_layer[y_tu * ROOM_W_TU + x_tu]

    # In case this tile is from deleted draw, then I cannot update this tile
    if sprite != 0:
        if sprite["name"] in BITMASK_TYPE_SPRITE_NAMES:
            # Hacky solution but json file has it stored in string but mine is in int
            new_region = []
            try:
                new_region = sprite["regions"][str(mask_id)]
            except:
                new_region = sprite["regions"][mask_id]
            if new_region != 0:
                selected_layer[y_tu * ROOM_W_TU + x_tu]["region"] = new_region


def bucket_fill(x_tu, y_tu, xds, yds):
    # Create a blink effect on tile that mask about to change
    xs = xds - CAM_RECT.x
    ys = yds - CAM_RECT.y
    NATIVE_SURF.blit(LIGHT_SURF, (xs, ys), (0, 0, TILE_S, TILE_S))

    # Check my neighbours, but not corners
    neighbour_pos_tu = [
        (x_tu - 0, y_tu - 1), (x_tu - 1, y_tu - 0),
        (x_tu + 1, y_tu - 0), (x_tu - 0, y_tu + 1)
    ]
    for pos in neighbour_pos_tu:
        # Get tile from collision list
        neighbour_x_tu = pos[0]
        neighbour_y_tu = pos[1]

        # Make sure that pos is inside the list
        if (0 <= neighbour_x_tu < ROOM_W_TU) and (0 <= neighbour_y_tu < ROOM_H_TU):
            neighbour = selected_layer[neighbour_y_tu *
                                       ROOM_W_TU + neighbour_x_tu]

            # Air? Instance new sprite
            if neighbour == 0:
                # Prepare real draw positions
                neighbour_xd_tu = neighbour_x_tu + ROOM_X_TU
                neighbour_yd_tu = neighbour_y_tu + ROOM_Y_TU
                neighbour_xds = neighbour_xd_tu * TILE_S
                neighbour_yds = neighbour_yd_tu * TILE_S

                # Instance new sprite
                new_sprite = selected_sprite.copy()
                new_sprite["xds"] = neighbour_xds
                new_sprite["yds"] = neighbour_yds
                selected_layer[neighbour_y_tu *
                               ROOM_W_TU + neighbour_x_tu] = new_sprite

                # Tell my neighbour to fill
                bucket_fill(
                    neighbour_x_tu, neighbour_y_tu,
                    neighbour_xds, neighbour_yds,
                )

                # Update bistmasks if it is bitmask type
                if new_sprite["name"] in BITMASK_TYPE_SPRITE_NAMES:
                    update_bitmasks(neighbour_x_tu, neighbour_y_tu,
                                    neighbour_xds, neighbour_yds)
# endregion


# Main loop
while 1:
    # Dt
    dt = CLOCK.tick(FPS)

    # Menu state
    if is_menu:
        # Clear native
        NATIVE_SURF.fill("grey0")

        # region Draw menu surface and item hover
        NATIVE_SURF.blit(MENU_SURF, (0, 0))
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
        # endregion

        # region Draw cursor
        r = xs + TILE_S
        b = ys + TILE_S
        pg.draw.lines(NATIVE_SURF, "white", True, [
                      (xs, ys), (r, ys), (r, ys), (r, b), (r, b), (xs, b)], 1)
        # endregion

    # Normal state
    else:
        # Clear native
        NATIVE_SURF.fill("grey0")

        # region Move camera
        if not is_shift_pressed:
            # Cannot move during rect draw
            CAM_RECT.x += (is_d_pressed - is_a_pressed) * CAM_SPD
            CAM_RECT.y += (is_s_pressed - is_w_pressed) * CAM_SPD
            CAM_RECT.clamp_ip(ROOM_RECT)
        # endregion

        # region Draw all sprites on grid
        for room in LAYERS_LIST:
            for item in room:
                if item != 0:
                    # Only update sprites that are in view
                    if (CAM_RECT.x - item["region"][2] <= item["xds"] < CAM_RECT.right) and (CAM_RECT.y - item["region"][3] <= item["yds"] < CAM_RECT.bottom):
                        xd = item["xds"] - CAM_RECT.x
                        yd = item["yds"] - CAM_RECT.y
                        NATIVE_SURF.blit(SPRITE_SHEET_SURF,
                                         (xd, yd), item["region"])
        # endregion

        # region Draw grid
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
        FONT.render_to(
            NATIVE_SURF, (xd + FONT_W, yd + FONT_H), f"{
                (CAM_RECT.x - 1) // NATIVE_W + 1}{
                (CAM_RECT.y - 1) // NATIVE_H + 1}", "grey100"
        )
        # endregion

        # region Draw room
        xd = ROOM_RECT.x - CAM_RECT.x - 1
        yd = ROOM_RECT.y - CAM_RECT.y - 1
        b = yd + ROOM_RECT.height
        r = xd + ROOM_RECT.width
        pg.draw.lines(NATIVE_SURF, "red", True, [
                      (xd, yd), (r, yd), (r, yd), (r, b), (r, b), (xd, b)], 2)
        # endregion

        # region Draw cursor
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
        r = xs + selected_sprite["region"][2]
        b = ys + selected_sprite["region"][3]
        if not (is_shift_pressed and is_lmb_pressed) and not (is_shift_pressed and is_rmb_pressed):
            if is_rmb_pressed:
                pg.draw.lines(NATIVE_SURF, "red", True, [
                    (xs, ys), (r, ys), (r, ys), (r, b), (r, b), (xs, b)], 1)
            else:
                pg.draw.lines(NATIVE_SURF, "white", True, [
                    (xs, ys), (r, ys), (r, ys), (r, b), (r, b), (xs, b)], 1)
        # endregion

        # Rect draw mode
        if is_shift_pressed:
            # region Draw the white rect cursor
            if is_lmb_pressed:
                if start_xs <= xs:
                    xs += TILE_S
                if start_ys <= ys:
                    ys += TILE_S
                top_left = (max(min(start_xs, xs), 0),
                            max(min(start_ys, ys), 0))
                top_right = (min(max(start_xs, xs), NATIVE_W),
                             max(min(start_ys, ys), 0))
                bottom_left = (max(min(start_xs, xs), 0),
                               min(max(start_ys, ys), NATIVE_H))

                bottom_right = (min(max(start_xs, xs), NATIVE_W),
                                min(max(start_ys, ys), NATIVE_H))
                pg.draw.lines(NATIVE_SURF, "white", True, [
                    top_left, top_right, bottom_right, bottom_left], 1)
            # endregion

            # region Draw the red rect cursor
            elif is_rmb_pressed:
                if start_xs <= xs:
                    xs += TILE_S
                if start_ys <= ys:
                    ys += TILE_S
                top_left = (max(min(start_xs, xs), 0),
                            max(min(start_ys, ys), 0))
                top_right = (min(max(start_xs, xs), NATIVE_W),
                             max(min(start_ys, ys), 0))
                bottom_left = (max(min(start_xs, xs), 0),
                               min(max(start_ys, ys), NATIVE_H))

                bottom_right = (min(max(start_xs, xs), NATIVE_W),
                                min(max(start_ys, ys), NATIVE_H))
                pg.draw.lines(NATIVE_SURF, "red", True, [
                    top_left, top_right, bottom_right, bottom_left], 1)
            # endregion

        # Normal drawing mode
        else:
            # region Add sprite on grid
            if is_lmb_pressed:
                item = selected_layer[y_tu * ROOM_W_TU + x_tu]
                if item == 0:
                    # Check if sprite right side and bottom side does not overshoot room rect
                    r = xds + selected_sprite["region"][2]
                    b = yds + selected_sprite["region"][3]
                    if not r > ROOM_RECT.right and not b > ROOM_RECT.bottom:
                        new_sprite = selected_sprite.copy()
                        new_sprite["xds"] = xds
                        new_sprite["yds"] = yds
                        selected_layer[y_tu * ROOM_W_TU + x_tu] = new_sprite
                        NATIVE_SURF.blit(LIGHT_SURF, (xs, ys),
                                         (0, 0, selected_sprite["region"][2], selected_sprite["region"][3],))
                        TALK_SFX.play()
                        if new_sprite["name"] in BITMASK_TYPE_SPRITE_NAMES:
                            update_bitmasks(x_tu, y_tu, xds, yds)
            # endregion

            # region Del sprite on grid
            if is_rmb_pressed:
                item = selected_layer[y_tu * ROOM_W_TU + x_tu]
                if item != 0:
                    selected_layer[y_tu * ROOM_W_TU + x_tu] = 0
                    NATIVE_SURF.blit(LIGHT_SURF, (xs, ys),
                                     (0, 0, selected_sprite["region"][2], selected_sprite["region"][3],))
                    TALK_SFX.play()
                    if item["name"] in BITMASK_TYPE_SPRITE_NAMES:
                        update_bitmasks(x_tu, y_tu, xds, yds)
            # endregion

    # Get event
    for event in pg.event.get(EVENTS):
        # region Window quit
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        # endregion

        # Key down
        if event.type == pg.KEYDOWN:
            # region Cam input flag
            if event.key == pg.K_w:
                is_w_pressed = 1
            if event.key == pg.K_a:
                is_a_pressed = 1
            if event.key == pg.K_s:
                is_s_pressed = 1
            if event.key == pg.K_d:
                is_d_pressed = 1
            # endregion

            # region Rect draw input flag
            if event.key == pg.K_LSHIFT:
                is_shift_pressed = True
                # region Rect draw start pos
                start_xs = xs
                start_ys = ys
                # endregion
            # endregion

        # Key up
        elif event.type == pg.KEYUP:
            # region Cam input flag
            if event.key == pg.K_w:
                is_w_pressed = 0
            if event.key == pg.K_a:
                is_a_pressed = 0
            if event.key == pg.K_s:
                is_s_pressed = 0
            if event.key == pg.K_d:
                is_d_pressed = 0
            # endregion

            # region Open menu
            if event.key == pg.K_SPACE:
                is_menu = not is_menu
                TALK_SFX.play()
                pg.mouse.set_cursor(ADD_CURSOR)
                NATIVE_SURF.blit(LIGHT_SURF, (0, 0))
            # endregion

            # region Rect draw input flag
            if event.key == pg.K_LSHIFT:
                is_shift_pressed = False
                start_xs = 0
                start_ys = 0
                top_left = 0
                top_right = 0
                bottom_left = 0
                bottom_right = 0
            # endregion

            # region Delete all button
            if event.key == pg.K_0:
                is_something_deleted = False
                for room in LAYERS_LIST:
                    for i in range(len(room)):
                        item = room[i]
                        if item != 0:
                            is_something_deleted = True
                            xs = item["xds"] - CAM_RECT.x
                            ys = item["yds"] - CAM_RECT.y
                            NATIVE_SURF.blit(
                                LIGHT_SURF, (xs, ys), (0, 0, TILE_S, TILE_S))
                        room[i] = 0
                if is_something_deleted:
                    TALK_SFX.play()
            # endregion

            # region Show layers list
            if event.key == pg.K_p:
                # Save data to be used in editor load
                ROOM_TO_BE_SAVED_DATA_LOAD = {
                    "RESOLUTION": RESOLUTION,
                    "ROOM_X_RU": ROOM_X_RU,
                    "ROOM_Y_RU": ROOM_Y_RU,
                    "ROOM_SCALE_X": ROOM_SCALE_X,
                    "ROOM_SCALE_Y": ROOM_SCALE_Y,
                    "ROOM_SCALE_Y": ROOM_SCALE_Y,
                    "STAGE_NO": STAGE_NO,
                    "ROOM_NAME": ROOM_NAME,
                    "LAYERS_LIST": LAYERS_LIST,
                }
                with open(SAVE_PATH_LOAD, "w") as json_file:
                    dump(ROOM_TO_BE_SAVED_DATA_LOAD, json_file)
                # Room ready
                TO_BE_SAVED_BG_LAYERS = []
                TO_BE_SAVED_COLLISION_LAYER = []
                TO_BE_SAVED_FG_LAYERS = []
                for i in range(TOTAL_LAYERS):
                    room = LAYERS_LIST[i]
                    # Remove zeroes from non collision layers
                    if i != COLLISION_LAYER_I:
                        room = [x for x in room if x != 0]
                    # Remove layer_i and regions from sprites, these are not needed for drawing in game
                    for sprite in room:
                        if sprite != 0:
                            sprite.pop("layer_i")
                            # Not all sprites has regions
                            if "regions" in sprite:
                                sprite.pop("regions")
                    # Collect non empty rooms
                    if room:
                        for cell in room:
                            if cell != 0:
                                region = cell["region"]
                                cell["region"] = [region[0],
                                                  region[1], region[2], region[3]]
                        if i < COLLISION_LAYER_I:
                            TO_BE_SAVED_BG_LAYERS.append(room)
                        elif i == COLLISION_LAYER_I:
                            TO_BE_SAVED_COLLISION_LAYER = room
                        elif i > COLLISION_LAYER_I:
                            TO_BE_SAVED_FG_LAYERS.append(room)
                # Save data to be used in game
                ROOM_TO_BE_SAVED_DATA = {
                    "BG_LAYERS": TO_BE_SAVED_BG_LAYERS,
                    "COLLISION_LAYER": TO_BE_SAVED_COLLISION_LAYER,
                    "FG_LAYERS": TO_BE_SAVED_FG_LAYERS,
                    "ROOM_RECT": [ROOM_RECT.x, ROOM_RECT.y, ROOM_RECT.width, ROOM_RECT.height],
                    "SPRITE_SHEET_PNG_NAME": SPRITE_SHEET_PNG_NAME,
                    "TILE_S": TILE_S,
                    # TODO: If state 1 was choosed, add the option to select bg either sky, clouds and temple
                    "BG1": "sky",
                    "BG2": "clouds",
                    "BG3": "trees",
                }
                with open(SAVE_PATH, "w") as json_file:
                    dump(ROOM_TO_BE_SAVED_DATA, json_file)
            # endregion

        # Mouse down
        if event.type == pg.MOUSEBUTTONDOWN:
            # region Drawing input flag
            if event.button == 1:
                is_lmb_pressed = True
                # region Rect draw start pos
                if is_shift_pressed:
                    start_xs = xs
                    start_ys = ys
                # endregion
            if event.button == 2:
                is_mmb_pressed = True
            if event.button == 3:
                is_rmb_pressed = True
                if not is_menu:
                    pg.mouse.set_cursor(DEL_CURSOR)
                # region Rect draw start pos
                if is_shift_pressed:
                    start_xs = xs
                    start_ys = ys
                # endregion
            # endregion

        # Mouse up
        elif event.type == pg.MOUSEBUTTONUP:
            # region Drawing input flag and rect and fill draw feature
            if event.button == 1:
                is_lmb_pressed = False

                # region Rect add fill
                if is_shift_pressed and not is_menu:
                    # region Turn xs into tu
                    tl_xs = top_left[0]
                    tl_xds = tl_xs + CAM_RECT.x
                    tl_xd_tu = tl_xds // TILE_S
                    # Remove room offset to be collision index
                    tl_x_tu = tl_xd_tu - ROOM_X_TU

                    tl_ys = top_left[1]
                    tl_yds = tl_ys + CAM_RECT.y
                    tl_yd_tu = tl_yds // TILE_S
                    # Remove room offset to be collision index
                    tl_y_tu = tl_yd_tu - ROOM_Y_TU

                    tr_xs = top_right[0]
                    tr_xds = tr_xs + CAM_RECT.x
                    tr_xd_tu = tr_xds // TILE_S
                    # Remove room offset to be collision index
                    tr_x_tu = tr_xd_tu - ROOM_X_TU

                    tr_ys = top_right[1]
                    tr_yds = tr_ys + CAM_RECT.y
                    tr_yd_tu = tr_yds // TILE_S
                    # Remove room offset to be collision index
                    tr_y_tu = tr_yd_tu - ROOM_Y_TU

                    bl_xs = bottom_left[0]
                    bl_xds = bl_xs + CAM_RECT.x
                    bl_xd_tu = bl_xds // TILE_S
                    # Remove room offset to be collision index
                    bl_x_tu = bl_xd_tu - ROOM_X_TU

                    bl_ys = bottom_left[1]
                    bl_yds = bl_ys + CAM_RECT.y
                    bl_yd_tu = bl_yds // TILE_S
                    # Remove room offset to be collision index
                    bl_y_tu = bl_yd_tu - ROOM_Y_TU

                    br_xs = bottom_right[0]
                    br_xds = br_xs + CAM_RECT.x
                    br_xd_tu = br_xds // TILE_S
                    # Remove room offset to be collision index
                    br_x_tu = br_xd_tu - ROOM_X_TU

                    br_ys = bottom_right[1]
                    br_yds = br_ys + CAM_RECT.y
                    br_yd_tu = br_yds // TILE_S
                    # Remove room offset to be collision index
                    br_y_tu = br_yd_tu - ROOM_Y_TU
                    # endregion

                    # region collect corner positions - tl_tu and so on
                    tl_tu = (tl_x_tu, tl_y_tu)
                    tr_tu = (tr_x_tu, tr_y_tu)
                    bl_tu = (bl_x_tu, bl_y_tu)
                    br_tu = (br_x_tu, br_y_tu)
                    # endregion

                    # region corner positions -> list of all positions inside the corners
                    min_x = min(tl_tu[0], tr_tu[0], bl_tu[0], br_tu[0])
                    max_x = max(tl_tu[0], tr_tu[0], bl_tu[0], br_tu[0])
                    min_y = min(tl_tu[1], tr_tu[1], bl_tu[1], br_tu[1])
                    max_y = max(tl_tu[1], tr_tu[1], bl_tu[1], br_tu[1])
                    filled_points = []
                    for y in range(min_y, max_y + 1):
                        for x in range(min_x, max_x + 1):
                            if (x <= tr_tu[0] and x > tl_tu[0]) and (y >= tl_tu[1] and y < bl_tu[1]):
                                filled_points.append((x, y))
                    # endregion

                    # region iterate over all points, and instance like normal drawing state
                    is_all_items_sprite = True
                    is_outside = True
                    for point in filled_points:
                        x_tu = point[0] - 1
                        y_tu = point[1]
                        xd_tu = x_tu + ROOM_X_TU
                        yd_tu = y_tu + ROOM_Y_TU
                        xds = xd_tu * TILE_S
                        yds = yd_tu * TILE_S
                        item = selected_layer[y_tu * ROOM_W_TU + x_tu]
                        if item == 0:
                            is_all_items_sprite = False
                            # Check if sprite right side and bottom side does not overshoot room rect
                            r = xds + selected_sprite["region"][2]
                            b = yds + selected_sprite["region"][3]
                            if not r > ROOM_RECT.right and not b > ROOM_RECT.bottom:
                                is_outside = False
                                new_sprite = selected_sprite.copy()
                                new_sprite["xds"] = xds
                                new_sprite["yds"] = yds
                                selected_layer[y_tu *
                                               ROOM_W_TU + x_tu] = new_sprite
                                if new_sprite["name"] in BITMASK_TYPE_SPRITE_NAMES:
                                    update_bitmasks(x_tu, y_tu, xds, yds)
                                else:
                                    xs = xds - CAM_RECT.x
                                    ys = yds - CAM_RECT.y
                                    NATIVE_SURF.blit(
                                        LIGHT_SURF, (xs, ys), (0, 0, new_sprite["region"][2], new_sprite["region"][3]))
                    if not is_all_items_sprite and not is_outside:
                        TALK_SFX.play()
                    # endregion
                # endregion

            elif event.button == 2:
                is_mmb_pressed = False

                # region Fill input
                if not is_menu:
                    item = selected_layer[y_tu * ROOM_W_TU + x_tu]
                    if item == 0:
                        # Check if sprite right side and bottom side does not overshoot room rect
                        r = xds + selected_sprite["region"][2]
                        b = yds + selected_sprite["region"][3]
                        if not r > ROOM_RECT.right and not b > ROOM_RECT.bottom:
                            new_sprite = selected_sprite.copy()
                            new_sprite["xds"] = xds
                            new_sprite["yds"] = yds
                            selected_layer[y_tu *
                                           ROOM_W_TU + x_tu] = new_sprite
                            TALK_SFX.play()
                            bucket_fill(x_tu, y_tu, xds, yds)
                            if new_sprite["name"] in BITMASK_TYPE_SPRITE_NAMES:
                                update_bitmasks(x_tu, y_tu, xds, yds)
                # endregion

            elif event.button == 3:
                is_rmb_pressed = False
                if not is_menu:
                    pg.mouse.set_cursor(ADD_CURSOR)

                # region Rect del fill
                if is_shift_pressed and not is_menu:
                    # region Turn xs into tu
                    tl_xs = top_left[0]
                    tl_xds = tl_xs + CAM_RECT.x
                    tl_xd_tu = tl_xds // TILE_S
                    # Remove room offset to be collision index
                    tl_x_tu = tl_xd_tu - ROOM_X_TU

                    tl_ys = top_left[1]
                    tl_yds = tl_ys + CAM_RECT.y
                    tl_yd_tu = tl_yds // TILE_S
                    # Remove room offset to be collision index
                    tl_y_tu = tl_yd_tu - ROOM_Y_TU

                    tr_xs = top_right[0]
                    tr_xds = tr_xs + CAM_RECT.x
                    tr_xd_tu = tr_xds // TILE_S
                    # Remove room offset to be collision index
                    tr_x_tu = tr_xd_tu - ROOM_X_TU

                    tr_ys = top_right[1]
                    tr_yds = tr_ys + CAM_RECT.y
                    tr_yd_tu = tr_yds // TILE_S
                    # Remove room offset to be collision index
                    tr_y_tu = tr_yd_tu - ROOM_Y_TU

                    bl_xs = bottom_left[0]
                    bl_xds = bl_xs + CAM_RECT.x
                    bl_xd_tu = bl_xds // TILE_S
                    # Remove room offset to be collision index
                    bl_x_tu = bl_xd_tu - ROOM_X_TU

                    bl_ys = bottom_left[1]
                    bl_yds = bl_ys + CAM_RECT.y
                    bl_yd_tu = bl_yds // TILE_S
                    # Remove room offset to be collision index
                    bl_y_tu = bl_yd_tu - ROOM_Y_TU

                    br_xs = bottom_right[0]
                    br_xds = br_xs + CAM_RECT.x
                    br_xd_tu = br_xds // TILE_S
                    # Remove room offset to be collision index
                    br_x_tu = br_xd_tu - ROOM_X_TU

                    br_ys = bottom_right[1]
                    br_yds = br_ys + CAM_RECT.y
                    br_yd_tu = br_yds // TILE_S
                    # Remove room offset to be collision index
                    br_y_tu = br_yd_tu - ROOM_Y_TU
                    # endregion

                    # region collect corner positions
                    tl_tu = (tl_x_tu, tl_y_tu)
                    tr_tu = (tr_x_tu, tr_y_tu)
                    bl_tu = (bl_x_tu, bl_y_tu)
                    br_tu = (br_x_tu, br_y_tu)
                    # endregion

                    # region corner positions -> list of all positions inside the corners
                    min_x = min(tl_tu[0], tr_tu[0], bl_tu[0], br_tu[0])
                    max_x = max(tl_tu[0], tr_tu[0], bl_tu[0], br_tu[0])
                    min_y = min(tl_tu[1], tr_tu[1], bl_tu[1], br_tu[1])
                    max_y = max(tl_tu[1], tr_tu[1], bl_tu[1], br_tu[1])
                    filled_points = []
                    for y in range(min_y, max_y + 1):
                        for x in range(min_x, max_x + 1):
                            if (x <= tr_tu[0] and x > tl_tu[0]) and (y >= tl_tu[1] and y < bl_tu[1]):
                                filled_points.append((x, y))
                    # endregion

                    # region iterate over all points, and instance like normal drawing state
                    is_all_items_zero = True
                    for point in filled_points:
                        x_tu = point[0] - 1
                        y_tu = point[1]
                        xd_tu = x_tu + ROOM_X_TU
                        yd_tu = y_tu + ROOM_Y_TU
                        xds = xd_tu * TILE_S
                        yds = yd_tu * TILE_S
                        item = selected_layer[y_tu * ROOM_W_TU + x_tu]
                        if item != 0:
                            is_all_items_zero = False
                            selected_layer[y_tu * ROOM_W_TU + x_tu] = 0
                            if item["name"] in BITMASK_TYPE_SPRITE_NAMES:
                                update_bitmasks(x_tu, y_tu, xds, yds)
                            else:
                                xs = xds - CAM_RECT.x
                                ys = yds - CAM_RECT.y
                                NATIVE_SURF.blit(
                                    LIGHT_SURF, (xs, ys), (0, 0, item["region"][2], item["region"][3]))
                    if not is_all_items_zero:
                        TALK_SFX.play()
                    # endregion
                # endregion
            # endregion

            # region Select menu item
            if is_menu:
                pos = pg.mouse.get_pos()
                x = pos[0] // RESOLUTION
                y = pos[1] // RESOLUTION
                x_tu = x // TILE_S
                y_tu = y // TILE_S
                xs = x_tu * TILE_S
                ys = y_tu * TILE_S
                cell = MENU_COLLISIONS[y_tu * NATIVE_W_TU + x_tu]
                if cell != 0:
                    selected_sprite = cell
                    # Handle door select
                    if selected_sprite["name"] == "Door":
                        selected_sprite["id"] = input("Door name: ")
                        selected_sprite["target"] = input("Door target: ")
                    selected_layer = LAYERS_LIST[selected_sprite["layer_i"]]
                    is_menu = False
                    TALK_SFX.play()
                    NATIVE_SURF.blit(LIGHT_SURF, (0, 0))
            # endregion

    # region Debug draw
    FONT.render_to(NATIVE_SURF, (FONT_W, 32 * FONT_H),
                   f"fps: {int(CLOCK.get_fps())}", "grey100", "black")
    FONT.render_to(NATIVE_SURF, (FONT_W, 34 * FONT_H),
                   f"sprite: {selected_sprite["name"]}", "grey100", "black")
    # endregion

    # region Native to window and update window
    pg.transform.scale(NATIVE_SURF, (WINDOW_W, WINDOW_H), WINDOW_SURF)
    pg.display.update()
    # endregion
