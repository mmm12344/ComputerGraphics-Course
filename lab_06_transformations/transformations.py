"""Lab 06 - Transformations (learnopengl.com: Getting started > Transformations)

Instead of changing the vertex data, we send ONE 4x4 matrix to the vertex
shader as a uniform; the shader multiplies every vertex by it:

        gl_Position = transform * vec4(aPos, 1.0);

The container rotates over time in the bottom-right corner:

        trans = translate(0.5, -0.5, 0)  *  rotate(time, z axis)
                 ^ applied SECOND             ^ applied FIRST

(matrices apply from RIGHT to LEFT).  A second container in the top-left
corner grows and shrinks with a sine wave - the same quad drawn twice with
two different matrices.

Keys:  O = swap the order (rotate*translate): watch the box orbit instead!
       ESC = quit
Run:  python3 transformations.py
      (also run glm_basics.py for the maths on the console)
"""
import ctypes
import math
import os
import sys

import glfw
import glm
import numpy as np
from OpenGL import GL

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # so we can import glutils.py
from glutils import Shader, create_window, load_texture, texture_path

HERE = os.path.dirname(os.path.abspath(__file__))
swap_order = False


def key_callback(window, key, scancode, action, mods):
    global swap_order
    if action != glfw.PRESS:
        return
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    elif key == glfw.KEY_O:
        swap_order = not swap_order


def main():
    window = create_window(800, 600, "LearnOpenGL - Transformations (O = swap order)")
    glfw.set_key_callback(window, key_callback)

    shader = Shader(os.path.join(HERE, "shaders", "transform.vs"),
                    os.path.join(HERE, "shaders", "transform.fs"))

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
    GL.glVertexAttribPointer(1, 2, GL.GL_FLOAT, GL.GL_FALSE, 5 * 4, ctypes.c_void_p(3 * 4))
    GL.glEnableVertexAttribArray(1)

    container = load_texture(texture_path("container.jpg"))
    face = load_texture(texture_path("awesomeface.png"))
    shader.use()
    shader.set_int("texture1", 0)
    shader.set_int("texture2", 1)

    while not glfw.window_should_close(window):
        GL.glClearColor(0.2, 0.3, 0.3, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, container)
        GL.glActiveTexture(GL.GL_TEXTURE1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, face)
        shader.use()
        GL.glBindVertexArray(VAO)
        time = glfw.get_time()

        # ---- container 1: rotate, then move to the bottom right -------------
        trans = glm.mat4(1.0)                                   # identity
        if not swap_order:
            trans = glm.translate(trans, glm.vec3(0.5, -0.5, 0.0))
            trans = glm.rotate(trans, time, glm.vec3(0.0, 0.0, 1.0))
        else:
            trans = glm.rotate(trans, time, glm.vec3(0.0, 0.0, 1.0))
            trans = glm.translate(trans, glm.vec3(0.5, -0.5, 0.0))
        shader.set_mat4("transform", trans)
        GL.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, ctypes.c_void_p(0))

        # ---- container 2: move to the top left, scale with a sine wave ------
        s = abs(math.sin(time)) * 0.8 + 0.2
        trans = glm.mat4(1.0)
        trans = glm.translate(trans, glm.vec3(-0.5, 0.5, 0.0))
        trans = glm.scale(trans, glm.vec3(s, s, s))
        shader.set_mat4("transform", trans)
        GL.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, ctypes.c_void_p(0))

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
