"""Lab 01 - A simulated frame buffer you can paint on.

A raster screen is just a grid of pixels.  The frame buffer is the memory
that stores the colour of EVERY pixel.  This program keeps such a buffer as
a simple 2-D list and shows it magnified on screen.

Mouse:  left-drag = paint      right-drag = erase
Keys:   1 / 2 / 3 = pretend the buffer has 1 / 3 / 24 bits per pixel
        R G B Y   = choose the paint colour        C = clear
        ESC = quit

Run:  python3 pixel_framebuffer.py
"""
import glfw
from OpenGL import GL

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # so we can import common.py from the parent folder

from common import clear, draw_grid, draw_lines, draw_text, make_window, ortho2d, run

COLS, ROWS = 32, 24          # size of the simulated frame buffer, in pixels
CELL = 20                    # screen pixels per simulated pixel

# The frame buffer itself: frame_buffer[y][x] holds an (r, g, b) colour.
frame_buffer = [[(0.0, 0.0, 0.0) for x in range(COLS)] for y in range(ROWS)]

paint_color = (1.0, 1.0, 1.0)     # what the mouse paints with
depth = 24                        # simulated bits per pixel: 1, 3 or 24
erasing = False                   # is the right button held down?


# ---------------------------------------------------------------------------
# frame buffer functions (plain Python - no OpenGL here)
# ---------------------------------------------------------------------------
def quantise(color, depth):
    """Simulate few bits per pixel: 1 bit = black/white, 3 bits = 8 colours."""
    if depth == 24:
        return tuple(color)
    if depth == 3:
        return tuple(0.0 if c < 0.5 else 1.0 for c in color)
    bright = (color[0] + color[1] + color[2]) / 3.0
    return (1.0, 1.0, 1.0) if bright >= 0.5 else (0.0, 0.0, 0.0)


def plot_pixel(x, y, color):
    """Write one pixel into the buffer (ignore coordinates outside it)."""
    if 0 <= x < COLS and 0 <= y < ROWS:
        frame_buffer[y][x] = quantise(color, depth)


def clear_buffer():
    for y in range(ROWS):
        for x in range(COLS):
            frame_buffer[y][x] = (0.0, 0.0, 0.0)


# ---------------------------------------------------------------------------
# mouse and keyboard
# ---------------------------------------------------------------------------
def mouse_to_pixel(window):
    """Which buffer pixel is the mouse on?"""
    import glfw
    mx, my = glfw.get_cursor_pos(window)
    w, h = glfw.get_window_size(window)
    x = int(mx / w * COLS)
    y = int((h - my) / h * ROWS)      # OpenGL counts y from the BOTTOM
    return x, y


def on_button(window, button, action, mods):
    global erasing
    if action == glfw.PRESS or action == glfw.RELEASE:
        erasing = (button == glfw.MOUSE_BUTTON_RIGHT) and action == glfw.PRESS
        x, y = mouse_to_pixel(window)
        paint(x, y)


def on_cursor(window, xpix, ypix):
    x, y = mouse_to_pixel(window)
    paint(x, y)


def paint(x, y):
    if erasing:
        plot_pixel(x, y, (0.0, 0.0, 0.0))
    else:
        plot_pixel(x, y, paint_color)


def on_key(window, key, scancode, action, mods):
    global paint_color, depth
    if action != glfw.PRESS:
        return
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    elif key == glfw.KEY_C:
        clear_buffer()
    elif key == glfw.KEY_R:
        paint_color = (1.0, 0.2, 0.2)
    elif key == glfw.KEY_G:
        paint_color = (0.2, 1.0, 0.2)
    elif key == glfw.KEY_B:
        paint_color = (0.2, 0.2, 1.0)
    elif key == glfw.KEY_Y:
        paint_color = (1.0, 1.0, 0.1)
    elif key == glfw.KEY_1:
        depth = 1
    elif key == glfw.KEY_2:
        depth = 3
    elif key == glfw.KEY_3:
        depth = 24


# ---------------------------------------------------------------------------
# drawing: show the buffer magnified, one big square per simulated pixel
# ---------------------------------------------------------------------------
def draw():
    clear()
    ortho2d(0, COLS, 0, ROWS)

    GL.glBegin(GL.GL_QUADS)           # one coloured square per lit pixel
    for y in range(ROWS):
        for x in range(COLS):
            r, g, b = frame_buffer[y][x]
            if (r, g, b) != (0.0, 0.0, 0.0):
                GL.glColor3f(r, g, b)
                GL.glVertex2f(x, y)
                GL.glVertex2f(x + 1, y)
                GL.glVertex2f(x + 1, y + 1)
                GL.glVertex2f(x, y + 1)
    GL.glEnd()

    draw_grid(0, COLS, 0, ROWS, 1.0, color=(0.15, 0.17, 0.23))
    draw_text(0.3, ROWS + 0.5, f"BITS/PIXEL: {depth}",
              color=(0.9, 0.9, 0.9), scale=0.35)


def main():
    window = make_window(COLS * CELL, ROWS * CELL + 30,
                         "Lab 01 - Simulated frame buffer (paint with the mouse)")
    glfw.set_mouse_button_callback(window, on_button)
    glfw.set_cursor_pos_callback(window, on_cursor)
    glfw.set_key_callback(window, on_key)
    run(window, draw)


if __name__ == "__main__":
    main()
