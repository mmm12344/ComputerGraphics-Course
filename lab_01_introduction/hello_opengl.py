"""YOUR FIRST OPENGL PROGRAM
===========================

What is what:
  * OpenGL  - a library that draws points, lines and triangles on the GPU.
  * GLFW    - a library that opens a window and reads the keyboard/mouse.
  * PyOpenGL - lets us call both from Python.

Install the two libraries once:
      pip install PyOpenGL glfw

Then run this program:
      python3 hello_opengl.py
Close it with ESC.

Read the comments top to bottom - every OpenGL call is explained.
"""
import glfw
from OpenGL import GL

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # so we can import common.py from the parent folder

from common import make_window, run


# ---------------------------------------------------------------------------
# This function is called about 60 times every second.
# Every call must redraw the WHOLE image from scratch.
# ---------------------------------------------------------------------------
def draw():
    # 1. Choose the background colour (red, green, blue, alpha - each 0..1)
    #    and paint every pixel of the window with it.
    GL.glClearColor(0.05, 0.06, 0.10, 1.0)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)

    # 2. Choose the drawing colour, then draw a triangle.
    #    OpenGL's DEFAULT coordinate system is a square from (-1,-1)
    #    (bottom-left) to (+1,+1) (top-right).
    GL.glColor3f(1.0, 0.6, 0.1)                 # orange
    GL.glBegin(GL.GL_TRIANGLES)                 # start a triangle
    GL.glVertex2f(-0.6, -0.5)                   # corner 1  (x, y)
    GL.glVertex2f(0.6, -0.5)                    # corner 2
    GL.glVertex2f(0.0, 0.7)                     # corner 3
    GL.glEnd()                                  # finish

    # 3. Points work the same way - here are the three corners again,
    #    drawn as big dots.
    GL.glColor3f(0.3, 0.9, 0.5)                 # green
    GL.glPointSize(12)                          # dot size in pixels
    GL.glBegin(GL.GL_POINTS)
    GL.glVertex2f(-0.6, -0.5)
    GL.glVertex2f(0.6, -0.5)
    GL.glVertex2f(0.0, 0.7)
    GL.glEnd()

    # 4. Lines work the same way too.  GL_LINES joins pairs of vertices.
    GL.glColor3f(0.4, 0.7, 1.0)                 # blue
    GL.glLineWidth(2)
    GL.glBegin(GL.GL_LINES)
    GL.glVertex2f(-1.0, 0.0)                    # start of line 1
    GL.glVertex2f(1.0, 0.0)                     # end of line 1
    GL.glEnd()

    # 5. Prove the window really is redrawn constantly: the background
    #    brightness slowly follows the clock.
    import math
    glow = 0.5 + 0.5 * math.sin(glfw.get_time())
    GL.glColor3f(glow, glow, glow)
    GL.glBegin(GL.GL_POINTS)
    GL.glVertex2f(0.0, -0.85)
    GL.glEnd()


# ---------------------------------------------------------------------------
# Called every time a key is pressed or released.
# ---------------------------------------------------------------------------
def on_key(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)   # closes the window


# ---------------------------------------------------------------------------
def main():
    window = make_window(700, 500, "Hello OpenGL")   # open the window
    glfw.set_key_callback(window, on_key)            # receive key presses
    run(window, draw)                                # loop draw() until closed


if __name__ == "__main__":
    main()
