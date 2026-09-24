"""Shared helper module for all Computer Graphics labs.

Windowing: GLFW      Rendering: classic OpenGL (fixed function)

Every lab program follows the same three-step recipe:

    window = make_window(800, 600, "Title")  # 1. open a window
    glfw.set_key_callback(window, on_key)    # 2. (optional) react to input
    run(window, draw)                        # 3. call draw() until closed

Open this file if you are curious what make_window() and run() do inside -
it is just GLFW calls.  The drawing helpers below are thin wrappers around
the classic OpenGL functions you know from the lectures (glBegin, glVertex2f,
glOrtho, glViewport, ...).

Requires:  pip install PyOpenGL glfw
"""
import os
import sys

import glfw
from OpenGL import GL

# ---------------------------------------------------------------------------
# environment switches (testing hooks)
# ---------------------------------------------------------------------------
AUTOCLOSE = float(os.environ.get("CG_LAB_AUTOCLOSE", "0") or 0)
HIDDEN = os.environ.get("CG_LAB_HIDDEN", "") not in ("", "0")
DUMP_PATH = os.environ.get("CG_LAB_DUMP", "")

_WINDOW = None  # keep a module-level reference so callbacks survive


def make_window(width=800, height=600, title="CG Lab"):
    """Create a GLFW window with a classic (compatibility) OpenGL context."""
    global _WINDOW
    if not glfw.init():
        raise RuntimeError("Could not initialise GLFW")
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE if HIDDEN else glfw.TRUE)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    window = glfw.create_window(width, height, title, None, None)
    if window is None:
        glfw.terminate()
        raise RuntimeError("Could not create GLFW window")
    glfw.make_context_current(window)
    glfw.swap_interval(0 if HIDDEN else 1)  # vsync off while testing
    _WINDOW = window
    return window


def destroy_window(window=None):
    """Close the window and release GLFW."""
    window = window or _WINDOW
    if window is not None:
        glfw.destroy_window(window)
    glfw.terminate()


def run(window, on_draw, on_key=None, on_button=None, on_cursor=None, on_scroll=None):
    """Standard render loop.  Callbacks are the plain GLFW signatures."""
    if on_key:
        glfw.set_key_callback(window, on_key)
    if on_button:
        glfw.set_mouse_button_callback(window, on_button)
    if on_cursor:
        glfw.set_cursor_pos_callback(window, on_cursor)
    if on_scroll:
        glfw.set_scroll_callback(window, on_scroll)

    deadline = glfw.get_time() + AUTOCLOSE if AUTOCLOSE else None
    dumped = False
    try:
        while not glfw.window_should_close(window):
            if deadline is not None and glfw.get_time() > deadline:
                break
            on_draw()
            if DUMP_PATH and not dumped:      # testing aid: save frame 1
                GL.glFinish()
                _dump_framebuffer(DUMP_PATH)
                dumped = True
            glfw.swap_buffers(window)
            glfw.poll_events()
    finally:
        destroy_window(window)


def _dump_framebuffer(path):
    """Read the default framebuffer back and save it as a PNG (testing aid)."""
    import numpy as np
    from PIL import Image

    w, h = glfw.get_framebuffer_size(_WINDOW)
    GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)
    data = GL.glReadPixels(0, 0, w, h, GL.GL_RGB, GL.GL_UNSIGNED_BYTE)
    img = np.frombuffer(data, dtype=np.uint8).reshape(h, w, 3)
    Image.fromarray(np.flipud(img).copy()).save(path)


def maybe_dump(path=None):
    """Save a screenshot when CG_LAB_DUMP is set (used by --selftest modes)."""
    if DUMP_PATH or path:
        _dump_framebuffer(path or DUMP_PATH)


# ---------------------------------------------------------------------------
# small drawing helpers (classic OpenGL)
# ---------------------------------------------------------------------------
def clear(color=(0.06, 0.07, 0.10, 1.0)):
    GL.glClearColor(*color)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)


def ortho2d(wl, wr, wb, wt):
    """Window-to-viewport mapping: define the world window (gluOrtho2D)."""
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GL.glOrtho(wl, wr, wb, wt, -1.0, 1.0)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()


def viewport(x, y, w, h):
    """Define the viewport in screen (device) coordinates."""
    GL.glViewport(int(x), int(y), int(w), int(h))


def window_size():
    """Actual framebuffer size in pixels (may differ from the requested one)."""
    return glfw.get_framebuffer_size(_WINDOW)


def cursor_to_world(window, wl, wr, wb, wt):
    """Convert the mouse position to world coordinates (y counted from the
    bottom, like OpenGL).  Give it the same rectangle you passed to ortho2d."""
    mx, my = glfw.get_cursor_pos(window)
    w, h = glfw.get_window_size(window)
    x = wl + (mx / w) * (wr - wl)
    y = wb + ((h - my) / h) * (wt - wb)
    return x, y


def set_color(rgb):
    GL.glColor3f(*rgb)


def draw_points(points, color=(1, 1, 1), size=4):
    """Plot a list of (x, y) positions as GL_POINTS."""
    set_color(color)
    GL.glPointSize(size)
    GL.glBegin(GL.GL_POINTS)
    for x, y in points:
        GL.glVertex2f(x, y)
    GL.glEnd()


def draw_polyline(points, color=(1, 1, 1), width=2, closed=False):
    if len(points) < 2:
        return
    set_color(color)
    GL.glLineWidth(width)
    mode = GL.GL_LINE_LOOP if closed else GL.GL_LINE_STRIP
    GL.glBegin(mode)
    for x, y in points:
        GL.glVertex2f(x, y)
    GL.glEnd()


def draw_lines(segments, color=(1, 1, 1), width=1):
    """segments: iterable of ((x0, y0), (x1, y1))."""
    set_color(color)
    GL.glLineWidth(width)
    GL.glBegin(GL.GL_LINES)
    for (x0, y0), (x1, y1) in segments:
        GL.glVertex2f(x0, y0)
        GL.glVertex2f(x1, y1)
    GL.glEnd()


def draw_segment(p, q, color=(1, 1, 1), width=1):
    """Draw one straight line from point p to point q."""
    draw_lines([(p, q)], color=color, width=width)


def draw_filled_polygon(points, color=(1, 1, 1)):
    if len(points) < 3:
        return
    set_color(color)
    GL.glBegin(GL.GL_POLYGON)
    for x, y in points:
        GL.glVertex2f(x, y)
    GL.glEnd()


def draw_grid(xmin, xmax, ymin, ymax, step=1.0, color=(0.22, 0.25, 0.32)):
    """Light grid lines every `step` world units - visualises the pixel lattice."""
    segments = []
    x = xmin
    while x <= xmax + 1e-9:
        segments.append(((x, ymin), (x, ymax)))
        x += step
    y = ymin
    while y <= ymax + 1e-9:
        segments.append(((xmin, y), (xmax, y)))
        y += step
    draw_lines(segments, color=color, width=1)


def draw_axes(length=10.0, color=(0.55, 0.6, 0.7)):
    draw_lines([((-length, 0.0), (length, 0.0)), ((0.0, -length), (0.0, length))],
               color=color, width=1)


# ---------------------------------------------------------------------------
# tiny 5x7 bitmap font, so labs can label things without GLUT
# ---------------------------------------------------------------------------
_FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    ">": ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "'": ("00100", "00100", "00000", "00000", "00000", "00000", "00000"),
}


def draw_text(x, y, text, color=(1, 1, 1), scale=1.0):
    """Draw `text` with the built-in 5x7 font, lower-left corner at (x, y).

    `scale` is measured in world units per font pixel.
    """
    set_color(color)
    GL.glBegin(GL.GL_QUADS)
    cx = x
    for ch in text.upper():
        glyph = _FONT.get(ch, _FONT[" "])
        for row, bits in enumerate(glyph):
            for col, bit in enumerate(bits):
                if bit == "1":
                    x0 = cx + col * scale
                    y0 = y + (6 - row) * scale
                    GL.glVertex2f(x0, y0)
                    GL.glVertex2f(x0 + scale, y0)
                    GL.glVertex2f(x0 + scale, y0 + scale)
                    GL.glVertex2f(x0, y0 + scale)
        cx += 6 * scale
    GL.glEnd()


def text_width(text, scale=1.0):
    return len(text) * 6 * scale
