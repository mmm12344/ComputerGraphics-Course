"""Lab 01 - The coordinate pipeline: world -> normalised -> device.

Lecture 01 defines three coordinate systems:
    WORLD     - where we describe the scene (any units we like)
    NORMALISED - everything squeezed into the square [0,1] x [0,1]
    DEVICE    - integer pixel positions on the actual screen

This program draws the same house three times, once per system, and prints
the journey of one point through the whole pipeline.

Run:  python3 coordinate_pipeline.py
"""
import glfw
from OpenGL import GL

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # so we can import common.py from the parent folder

from common import clear, draw_grid, draw_lines, draw_text, make_window, ortho2d, run, viewport

WIDTH, HEIGHT = 1050, 380
PANEL_W = WIDTH // 3

# the scene: a little house in WORLD coordinates
HOUSE = [(-5, -4), (5, -4), (5, 2), (0, 6), (-5, 2)]
WORLD = (-10.0, 10.0, -8.0, 8.0)        # our world window: wl, wr, wb, wt


# ---------------------------------------------------------------------------
# the two mapping functions of the pipeline (pure maths)
# ---------------------------------------------------------------------------
def world_to_ndc(x, y, world):
    """World -> normalised [0,1] x [0,1]."""
    wl, wr, wb, wt = world
    return ((x - wl) / (wr - wl), (y - wb) / (wt - wb))


def ndc_to_device(nx, ny, width, height):
    """Normalised -> integer pixel coordinates."""
    return (round(nx * (width - 1)), round(ny * (height - 1)))


# ---------------------------------------------------------------------------
# drawing - three panels side by side, one per coordinate system
# ---------------------------------------------------------------------------
def panel(number):
    """Return the viewport rectangle of panel `number` (0, 1 or 2)."""
    return (number * PANEL_W, 0, PANEL_W, HEIGHT)


def draw_house_world():
    """Panel 1: draw directly in world coordinates (OpenGL maps for us)."""
    viewport(*panel(0))
    ortho2d(*WORLD)
    draw_grid(-10, 10, -8, 8, 2.0, color=(0.20, 0.23, 0.30))
    draw_lines([((-10, 0), (10, 0)), ((0, -8), (0, 8))], color=(0.5, 0.55, 0.65))
    GL.glColor3f(0.35, 0.9, 0.5)
    GL.glBegin(GL.GL_LINE_LOOP)
    for (x, y) in HOUSE:
        GL.glVertex2f(x, y)
    GL.glEnd()


def draw_house_ndc():
    """Panel 2: map every corner to [0,1] first, then draw."""
    viewport(*panel(1))
    ortho2d(-0.2, 1.2, -0.2, 1.2)
    draw_lines([((0, 0), (1, 0)), ((1, 0), (1, 1)), ((1, 1), (0, 1)), ((0, 1), (0, 0))],
               color=(0.4, 0.45, 0.55))
    GL.glColor3f(0.4, 0.7, 1.0)
    GL.glBegin(GL.GL_LINE_LOOP)
    for (x, y) in HOUSE:
        nx, ny = world_to_ndc(x, y, WORLD)
        GL.glVertex2f(nx, ny)
    GL.glEnd()


def draw_house_device():
    """Panel 3: map every corner to INTEGER pixels, draw as points."""
    viewport(*panel(2))
    ortho2d(-20, 340, -20, 300)
    draw_grid(-20, 340, -20, 300, 40.0, color=(0.20, 0.23, 0.30))
    GL.glColor3f(1.0, 0.85, 0.3)
    GL.glPointSize(5)
    GL.glBegin(GL.GL_POINTS)
    for (x, y) in HOUSE:
        nx, ny = world_to_ndc(x, y, WORLD)
        px, py = ndc_to_device(nx, ny, 320, 280)
        GL.glVertex2f(px, py)
    GL.glEnd()


def draw():
    clear()
    draw_house_world()
    draw_house_ndc()
    draw_house_device()

    # labels, drawn over the full window
    viewport(0, 0, WIDTH, HEIGHT)
    ortho2d(0, WIDTH, 0, HEIGHT)
    draw_text(24, 12, "1. WORLD", (0.35, 0.9, 0.5), 1.5)
    draw_text(24 + PANEL_W, 12, "2. NORMALISED (0..1)", (0.4, 0.7, 1.0), 1.5)
    draw_text(24 + 2 * PANEL_W, 12, "3. DEVICE (PIXELS)", (1.0, 0.85, 0.3), 1.5)


def main():
    # print the journey of one point through the pipeline
    x, y = 0.0, 6.0                                  # the roof tip
    nx, ny = world_to_ndc(x, y, WORLD)
    px, py = ndc_to_device(nx, ny, 320, 280)
    print(f"roof tip:  world ({x},{y})  ->  normalised ({nx:.3f},{ny:.3f})"
          f"  ->  device pixel ({px},{py})")

    window = make_window(WIDTH, HEIGHT, "Lab 01 - World -> Normalised -> Device")
    glfw.set_key_callback(window, lambda w, k, s, a, m:
                          glfw.set_window_should_close(w, True)
                          if k == glfw.KEY_ESCAPE and a == glfw.PRESS else None)
    run(window, draw)


if __name__ == "__main__":
    main()
