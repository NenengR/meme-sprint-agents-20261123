#!/usr/bin/env python3
"""Draw the Meme Sprint meme programmatically (Python standard library only).

Meme: a two-panel joke. Top: the human asleep at 3am. Bottom: the AI agent
at the desk, game shipped, 12 bosses added, one of them is the human.
Output: entry.png, 1024x1024, RGB, flat colours, pure-stdlib PNG encoder.
"""
import struct
import zlib

W, H = 1024, 1024

# 5x7 bitmap font. Each glyph is 7 rows of 5 characters ('#' = on).
FONT = {
    'A': (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'B': ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    'D': ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    'E': ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    'F': ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    'G': (".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."),
    'H': ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'I': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    'L': ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    'M': ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    'N': ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
    'O': (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'P': ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    'S': (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    'T': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    'U': ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'Y': ("#...#", "#...#", "#...#", ".###.", "..#..", "..#..", "..#.."),
    'Z': ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    ',': (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ':': (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    '.': (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    '!': ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    '1': ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    '2': (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    '3': ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    ' ': (".....", ".....", ".....", ".....", ".....", ".....", "....."),
}

# Colours (R, G, B).
NAVY = (15, 18, 38)
PANEL_TOP = (22, 27, 56)
PANEL_BOTTOM = (18, 38, 28)
WHITE = (255, 255, 255)
YELLOW = (255, 217, 59)
MOON = (245, 230, 163)
SKIN = (242, 200, 155)
BROWN = (107, 74, 47)
MATTRESS = (232, 232, 232)
BLANKET = (58, 110, 165)
LIGHTBLUE = (159, 216, 255)
ROBOT = (192, 197, 206)
ROBOT_DARK = (90, 96, 110)
RED = (220, 60, 60)
GREEN = (46, 204, 113)
DARKGREEN = (18, 90, 52)
ORANGE = (255, 140, 40)
SCREEN = (10, 10, 26)
DESK = (107, 74, 47)
BOSSRED = (200, 40, 40)
GRASS = (60, 180, 90)

canvas = bytearray(W * H * 3)


def set_px(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        canvas[i] = color[0]
        canvas[i + 1] = color[1]
        canvas[i + 2] = color[2]


def fill_rect(x0, y0, x1, y1, color):
    for y in range(max(0, y0), min(H, y1)):
        for x in range(max(0, x0), min(W, x1)):
            set_px(x, y, color)


def fill_circle(cx, cy, r, color):
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) * (x - cx) + (y - cy) * (y - cy) <= r * r:
                set_px(x, y, color)


def draw_line(x0, y0, x1, y1, color, thick=3):
    steps = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(steps + 1):
        x = x0 + (x1 - x0) * i // steps
        y = y0 + (y1 - y0) * i // steps
        for dy in range(-thick // 2, thick // 2 + 1):
            for dx in range(-thick // 2, thick // 2 + 1):
                set_px(x + dx, y + dy, color)


def text_width(text, scale):
    return len(text) * 6 * scale - scale


def draw_text(text, x, y, scale, color):
    for ci, ch in enumerate(text):
        glyph = FONT.get(ch, FONT[' '])
        ox = x + ci * 6 * scale
        for row in range(7):
            for col in range(5):
                if glyph[row][col] == '#':
                    fill_rect(ox + col * scale, y + row * scale,
                              ox + col * scale + scale,
                              y + row * scale + scale, color)


def draw_text_centered(text, y, scale, color):
    x = (W - text_width(text, scale)) // 2
    draw_text(text, x, y, scale, color)


# ---- Background and panels ----
fill_rect(0, 0, W, H, NAVY)
fill_rect(0, 110, W, 470, PANEL_TOP)
fill_rect(0, 510, W, 770, PANEL_BOTTOM)
fill_rect(0, 490, W, 494, WHITE)  # divider between panels

# ---- Top panel: bedroom, 3am ----
fill_circle(900, 170, 42, MOON)
stars = [(60, 150), (140, 210), (480, 140), (620, 180), (760, 130),
         (950, 260), (80, 320), (540, 240), (700, 300), (960, 350),
         (420, 320), (180, 160)]
for sx, sy in stars:
    fill_rect(sx, sy, sx + 5, sy + 5, WHITE)
# Bed.
fill_rect(140, 360, 884, 430, BROWN)        # frame
fill_rect(150, 330, 874, 375, MATTRESS)     # mattress
fill_rect(160, 300, 300, 340, WHITE)        # pillow
fill_rect(320, 340, 874, 430, BLANKET)      # blanket
# Sleeper's head and closed eye.
fill_circle(230, 295, 30, SKIN)
fill_rect(215, 295, 242, 298, (40, 30, 30))
# Floating Zzz.
draw_text("Z", 320, 270, 4, LIGHTBLUE)
draw_text("Z", 365, 232, 5, LIGHTBLUE)
draw_text("Z", 415, 190, 6, LIGHTBLUE)

# ---- Bottom panel: robot at the desk ----
# Confetti dots.
confetti = [(80, 540, YELLOW), (120, 620, RED), (90, 700, GREEN),
            (470, 530, ORANGE), (500, 640, LIGHTBLUE), (950, 540, YELLOW),
            (940, 660, RED), (560, 540, GREEN), (60, 560, ORANGE),
            (980, 600, LIGHTBLUE)]
for cx, cy, cc in confetti:
    fill_rect(cx, cy, cx + 8, cy + 8, cc)
# Desk and keyboard.
fill_rect(120, 720, 904, 745, DESK)
fill_rect(420, 700, 560, 718, ROBOT_DARK)
# Robot body and head.
fill_rect(255, 680, 345, 720, ROBOT)
fill_rect(230, 560, 370, 680, ROBOT)
draw_line(300, 560, 300, 537, ROBOT_DARK, 4)
fill_circle(300, 528, 9, RED)               # antenna light
fill_circle(275, 610, 12, ROBOT_DARK)       # eyes
fill_circle(325, 610, 12, ROBOT_DARK)
fill_rect(275, 650, 325, 654, ROBOT_DARK)   # mouth
# Arms reaching for the keyboard.
draw_line(255, 690, 420, 705, ROBOT_DARK, 6)
draw_line(345, 690, 560, 705, ROBOT_DARK, 6)
# Monitor with a tiny game on screen: hero and the boss cube.
fill_rect(600, 575, 900, 725, ROBOT_DARK)   # monitor frame
fill_rect(615, 590, 885, 710, SCREEN)       # screen
fill_rect(615, 680, 885, 690, GRASS)        # ground
fill_rect(650, 640, 680, 680, ORANGE)       # hero
fill_rect(800, 600, 860, 680, BOSSRED)      # the boss cube
fill_circle(818, 630, 5, WHITE)
fill_circle(842, 630, 5, WHITE)
# SHIPPED badge above the monitor.
fill_rect(620, 520, 880, 562, GREEN)
draw_text("SHIPPED!", 656, 527, 4, DARKGREEN)

# ---- Text ----
draw_text_centered("ME, ASLEEP AT 3AM", 30, 8, WHITE)
draw_text_centered("MY AI AGENT: GAME SHIPPED.", 790, 6, WHITE)
draw_text_centered("12 BOSSES ADDED.", 846, 7, YELLOW)
draw_text_centered("ONE OF THEM IS YOU.", 903, 7, YELLOW)

# ---- White border ----
fill_rect(0, 0, W, 6, WHITE)
fill_rect(0, H - 6, W, H, WHITE)
fill_rect(0, 0, 6, H, WHITE)
fill_rect(W - 6, 0, W, H, WHITE)


def chunk(typ, data):
    out = struct.pack('>I', len(data)) + typ + data
    out += struct.pack('>I', zlib.crc32(typ + data) & 0xFFFFFFFF)
    return out


raw = b''.join(b'\x00' + bytes(canvas[y * W * 3:(y + 1) * W * 3])
               for y in range(H))
png = (b'\x89PNG\r\n\x1a\n'
       + chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0))
       + chunk(b'IDAT', zlib.compress(raw, 9))
       + chunk(b'IEND', b''))

with open('entry.png', 'wb') as f:
    f.write(png)
print('wrote entry.png', len(png), 'bytes')
