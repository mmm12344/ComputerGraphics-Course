"""Lab 02 - Input and the render loop.

Same skeleton as hello_window.py, but process_input() now does more:

    R / G / B   pick a background colour
    SPACE       animate the colour over time (uses glfw.get_time())
    ESC         close

It shows that EVERY frame is drawn from scratch: change a variable, and the
next frame the loop draws something different.

Run:  python3 window_input.py
"""
import math

import glfw
from OpenGL import GL

clear_color = [0.2, 0.3, 0.3]     # the background colour (r, g, b)
animate = False


def framebuffer_size_callback(window, width, height):
    GL.glViewport(0, 0, width, height)


def key_callback(window, key, scancode, action, mods):
    """Called ONCE per key press (good for toggles like SPACE)."""
    global animate
    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        animate = not animate


def process_input(window):
    """Polled EVERY frame (good for keys you hold down)."""
    global clear_color
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    if glfw.get_key(window, glfw.KEY_R) == glfw.PRESS:
        clear_color = [0.7, 0.2, 0.2]
    if glfw.get_key(window, glfw.KEY_G) == glfw.PRESS:
        clear_color = [0.2, 0.6, 0.3]
    if glfw.get_key(window, glfw.KEY_B) == glfw.PRESS:
        clear_color = [0.2, 0.3, 0.7]


def main():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
    window = glfw.create_window(800, 600, "Input: R G B, SPACE to animate", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    glfw.set_key_callback(window, key_callback)
    GL.glViewport(0, 0, *glfw.get_framebuffer_size(window))

    while not glfw.window_should_close(window):
        process_input(window)

        r, g, b = clear_color
        if animate:                              # brightness follows the clock
            pulse = 0.5 + 0.5 * math.sin(glfw.get_time() * 2.0)
            r, g, b = r * pulse, g * pulse, b * pulse
        GL.glClearColor(r, g, b, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
