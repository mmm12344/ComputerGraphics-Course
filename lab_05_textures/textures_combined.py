"""Lab 05 - TWO textures with TEXTURE UNITS, wrapping and filtering.

A fragment shader can read several textures at once.  Each sampler uniform
is told WHICH TEXTURE UNIT to read from, and before drawing we bind a
texture to each unit:

    shader.set_int("texture1", 0)          # sampler texture1 reads unit 0
    shader.set_int("texture2", 1)          # sampler texture2 reads unit 1
    glActiveTexture(GL_TEXTURE0); glBindTexture(..., container)
    glActiveTexture(GL_TEXTURE1); glBindTexture(..., awesomeface)

The GLSL function mix(a, b, 0.2) gives 80% of a and 20% of b.

Keys:  UP / DOWN   change the mix value (how much smiley you see)
       S           texture coordinates 0..1  <->  0..2 (shows WRAPPING)
       W           cycle the wrapping mode: REPEAT, MIRRORED_REPEAT,
                   CLAMP_TO_EDGE
       F           toggle filtering: LINEAR (smooth) <-> NEAREST (blocky)
       ESC         quit
Run:  python3 textures_combined.py
"""
import ctypes
import os
import sys

import glfw
import numpy as np
from OpenGL import GL

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # so we can import glutils.py
from glutils import Shader, create_window, load_texture, texture_path

HERE = os.path.dirname(os.path.abspath(__file__))

WRAP_MODES = [("REPEAT", GL.GL_REPEAT),
              ("MIRRORED_REPEAT", GL.GL_MIRRORED_REPEAT),
              ("CLAMP_TO_EDGE", GL.GL_CLAMP_TO_EDGE)]

mix_value = 0.2
tex_scale = 1.0
wrap_index = 0
nearest = False
settings_changed = True       # apply wrap/filter settings on the first frame


def key_callback(window, key, scancode, action, mods):
    global tex_scale, wrap_index, nearest, settings_changed
    if action != glfw.PRESS:
        return
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    elif key == glfw.KEY_S:
        tex_scale = 2.0 if tex_scale == 1.0 else 1.0
    elif key == glfw.KEY_W:
        wrap_index = (wrap_index + 1) % len(WRAP_MODES)
        settings_changed = True
    elif key == glfw.KEY_F:
        nearest = not nearest
        settings_changed = True
    if action == glfw.PRESS and key in (glfw.KEY_S, glfw.KEY_W, glfw.KEY_F):
        print(f"tex coords 0..{tex_scale:.0f}   wrap = {WRAP_MODES[wrap_index][0]}"
              f"   filter = {'NEAREST' if nearest else 'LINEAR'}")


def process_input(window, delta_time):
    """UP/DOWN are HELD keys, so they are polled every frame."""
    global mix_value
    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        mix_value = min(1.0, mix_value + 1.0 * delta_time)
    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        mix_value = max(0.0, mix_value - 1.0 * delta_time)


def apply_texture_settings(texture):
    """Set wrapping and filtering on the currently chosen texture."""
    wrap = WRAP_MODES[wrap_index][1]
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, wrap)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, wrap)
    if nearest:
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
    else:
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR_MIPMAP_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)


def main():
    global settings_changed
    window = create_window(800, 600, "LearnOpenGL - Two textures (UP/DOWN, S, W, F)")
    glfw.set_key_callback(window, key_callback)

    shader = Shader(os.path.join(HERE, "shaders", "combined.vs"),
                    os.path.join(HERE, "shaders", "combined.fs"))

    vertices = np.array([
        # positions        # texture coords
         0.5,  0.5, 0.0,   1.0, 1.0,
         0.5, -0.5, 0.0,   1.0, 0.0,
        -0.5, -0.5, 0.0,   0.0, 0.0,
        -0.5,  0.5, 0.0,   0.0, 1.0,
    ], dtype=np.float32)
    indices = np.array([0, 1, 3, 1, 2, 3], dtype=np.uint32)

    VAO = GL.glGenVertexArrays(1)
    VBO, EBO = GL.glGenBuffers(2)
    GL.glBindVertexArray(VAO)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, EBO)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL.GL_STATIC_DRAW)
    GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 5 * 4, ctypes.c_void_p(0))
    GL.glEnableVertexAttribArray(0)
    # attribute 1 = texture coordinate (this shader has no colour attribute)
    GL.glVertexAttribPointer(1, 2, GL.GL_FLOAT, GL.GL_FALSE, 5 * 4, ctypes.c_void_p(3 * 4))
    GL.glEnableVertexAttribArray(1)

    container = load_texture(texture_path("container.jpg"))     # see textures.py
    face = load_texture(texture_path("awesomeface.png"))        # has transparency

    # tell each sampler which texture unit it belongs to (only once)
    shader.use()
    shader.set_int("texture1", 0)
    shader.set_int("texture2", 1)

    last_frame = glfw.get_time()
    while not glfw.window_should_close(window):
        now = glfw.get_time()
        process_input(window, now - last_frame)
        last_frame = now

        if settings_changed:
            apply_texture_settings(container)
            apply_texture_settings(face)
            settings_changed = False

        GL.glClearColor(0.2, 0.3, 0.3, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        # bind each texture to its texture unit
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, container)
        GL.glActiveTexture(GL.GL_TEXTURE1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, face)

        shader.use()
        shader.set_float("mixValue", mix_value)
        shader.set_float("texScale", tex_scale)
        GL.glBindVertexArray(VAO)
        GL.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, ctypes.c_void_p(0))

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
