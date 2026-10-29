"""Lab 04 - Shaders: MORE ATTRIBUTES and INTERPOLATION.

Each vertex now carries TWO attributes in the same buffer:

    x, y, z,  r, g, b      <- 6 floats per vertex
    |position| |colour|

    attribute 0 (position): 3 floats, stride 6 floats, offset 0
    attribute 1 (colour):   3 floats, stride 6 floats, offset 3 floats

The vertex shader passes the colour OUT; the fragment shader receives it
IN.  We only gave 3 colours, but the triangle shows a smooth gradient:
the rasteriser INTERPOLATES the outputs for every fragment in between.

Run:  python3 shaders_interpolation.py      (ESC to close)
"""
import ctypes
import os
import sys

import glfw
import numpy as np
from OpenGL import GL

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # so we can import glutils.py
from glutils import create_window

VERTEX_SHADER_SOURCE = """
#version 330 core
layout (location = 0) in vec3 aPos;     // attribute 0
layout (location = 1) in vec3 aColor;   // attribute 1

out vec3 ourColor;                      // passed on to the fragment shader

void main()
{
    gl_Position = vec4(aPos, 1.0);
    ourColor = aColor;
}
"""

FRAGMENT_SHADER_SOURCE = """
#version 330 core
in vec3 ourColor;                       // same NAME and TYPE as the 'out' above
out vec4 FragColor;

void main()
{
    FragColor = vec4(ourColor, 1.0);
}
"""


def compile_program(vertex_source, fragment_source):
    program = GL.glCreateProgram()
    for source, kind in [(vertex_source, GL.GL_VERTEX_SHADER),
                         (fragment_source, GL.GL_FRAGMENT_SHADER)]:
        shader = GL.glCreateShader(kind)
        GL.glShaderSource(shader, source)
        GL.glCompileShader(shader)
        if not GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS):
            raise RuntimeError(GL.glGetShaderInfoLog(shader).decode())
        GL.glAttachShader(program, shader)
        GL.glDeleteShader(shader)
    GL.glLinkProgram(program)
    return program


def main():
    window = create_window(800, 600, "LearnOpenGL - Interpolated colours")
    shader_program = compile_program(VERTEX_SHADER_SOURCE, FRAGMENT_SHADER_SOURCE)

    vertices = np.array([
        # positions         # colours
         0.5, -0.5, 0.0,    1.0, 0.0, 0.0,   # bottom right: red
        -0.5, -0.5, 0.0,    0.0, 1.0, 0.0,   # bottom left:  green
         0.0,  0.5, 0.0,    0.0, 0.0, 1.0,   # top:          blue
    ], dtype=np.float32)

    VAO = GL.glGenVertexArrays(1)
    VBO = GL.glGenBuffers(1)
    GL.glBindVertexArray(VAO)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW)

    stride = 6 * 4                                       # 6 floats * 4 bytes
    # position attribute
    GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, ctypes.c_void_p(0))
    GL.glEnableVertexAttribArray(0)
    # colour attribute: starts after the 3 position floats
    GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, ctypes.c_void_p(3 * 4))
    GL.glEnableVertexAttribArray(1)

    while not glfw.window_should_close(window):
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)

        GL.glClearColor(0.2, 0.3, 0.3, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glUseProgram(shader_program)
        GL.glBindVertexArray(VAO)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
