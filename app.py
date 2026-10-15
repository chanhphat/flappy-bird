import streamlit as st
import random
import time
from PIL import Image, ImageDraw

# --- Config ---
MAP_SIZE = 10
WALL_PROB = 0.12
NUM_ENEMIES = 8
NUM_TREASURES = 6
TILE_SIZE = 64            # pixel size of each tile
ANIM_FRAMES = 8           # số khung hình cho animation
ANIM_DELAY = 0.03         # giây giữa các khung

# --- Helpers: tile drawing ---
def make_tile_images(tile_size):
    # create common tile images (PIL.Image)
    floor = Image.new("RGBA", (tile_size, tile_size), (240, 240, 235, 255))
    draw = ImageDraw.Draw(floor)
    draw.rectangle([0, 0, tile_size-1, tile_size-1], outline=(200,200,190))
    # subtle pattern
    draw.line([(0, tile_size//2), (tile_size, tile_size//2)], fill=(230,230,225))
    draw.line([(tile_size//2, 0), (tile_size//2, tile_size)], fill=(230,230,225))

    wall = Image.new("RGBA", (tile_size, tile_size), (60, 60, 60, 255))
    draw = ImageDraw.Draw(wall)
    for i in range(0, tile_size, 8):
        draw.line([(i, 0), (i, tile_size)], fill=(75,75,75))
    draw.rectangle([0,0,tile_size-1,tile_size-1], outline=(30,30,30))

    exit_img = Image.new("RGBA", (tile_size, tile_size), (210,180,140,255))
    draw = ImageDraw.Draw(exit_img)
    draw.rectangle([tile_size*0.25, tile_size*0.15, tile_size*0.75, tile_size*0.9], fill=(140,90,40))
    draw.rectangle([tile_size*0.45, tile_size*0.45, tile_size*0.62, tile_size*0.62], fill=(220,200,140))

    treasure = Image.new("RGBA", (tile_size, tile_size), (0,0,0,0))
    draw = ImageDraw.Draw(treasure)
    cx, cy = tile_size//2, tile_size//2
    r = tile_size*0.18
    # simple gem: rotated square
    coords = [(cx, cy-r), (cx+r, cy), (cx, cy+r), (cx-r, cy)]
    draw.polygon(coords, fill=(255,215,0), outline=(200,170,0))

    enemy = Image.new("RGBA", (tile_size, tile_size), (0,0,0,0))
    draw = ImageDraw.Draw(enemy)
    draw.ellipse([tile_size*0.15, tile_size*0.15, tile_size*0.85, tile_size*0.85], fill=(200,50,50))
    draw.rectangle([tile_size*0.28, tile_size*0.4, tile_size*0.4, tile_size*0.55], fill=(0,0,0))
    draw.rectangle([tile_size*0.6, tile_size*0.4, tile_size*0.72, tile_size*0.55], fill=(0,0,0))

    player = Image.new("RGBA", (tile_size, tile_size), (0,0,0,0))
    draw = ImageDraw.Draw(player)
    draw.ellipse([tile_size*0.18, tile_size*0.12, tile_size*0.82, tile_size*0.72], fill=(50,110,200))
    draw.rectangle([tile_size*0.35, tile_size*0.6, tile_size*0.65, tile_size*0.9], fill=(30,70,160))

    return {
        "floor": floor,
        "wall": wall,
        "exit": exit_img,
        "treasure": treasure,
        "enemy": enemy,
        "player": player
    }

def render_map_image(grid, player_pos_f, enemies, treasures, exit_pos, tiles):
    size = len(grid)
    img = Image.new("RGBA", (size * TILE_SIZE, size * TILE_SIZE), (20, 20, 20, 255))
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            px = x * TILE_SIZE
            py = y * TILE_SIZE
            base = tiles["floor"] if cell == "." else tiles["wall"]
            img.paste(base, (px, py), base)
            if (x, y) == exit_pos:
                img.paste(tiles["exit"], (px, py), tiles["exit"])
            if (x, y) in treasures:
                img.paste(tiles["treasure"], (px, py), tiles["treasure"])
            if (x, y) in enemies:
                img.paste(tiles["enemy"], (px, py), tiles["enemy"])

    # draw player at fractional position (pixels)
    player_px = int(player_pos_f[0] * TILE_SIZE)
    player_py = int(player_pos_f[1] * TILE_SIZE)
    img.paste(tiles["player"], (player_px, player_py), tiles["player"])
    # optional grid lines
    draw = ImageDraw.Draw(img)
    for i in range(size+1):
        draw.line([(i*TILE_SIZE,0),(i*TILE_SIZE,size*TILE_SIZE)], fill=(40,40,40,100))
        draw.line([(0,i*TILE_SIZE),(size*TILE_SIZE,i*TILE_SIZE)], fill=(40,40,40,100))
    return img

# --- Map & game helpers (same logic as before)
