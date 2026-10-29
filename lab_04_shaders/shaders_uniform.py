"""Lab 04 - Shaders: UNIFORMS (learnopengl.com: Getting started > Shaders)

A UNIFORM is a global shader variable that the CPU (our Python code) sets.
It keeps its value until we change it, and every vertex / fragment sees the
same value.  Here we change the colour uniform every frame, so the triangle
pulses green over time.

Steps:
    1. declare it in GLSL:          uniform vec4 ourColor;
    2. find its location:           glGetUniformLocation(program, "ourColor")
    3. set it (program in use!):    glUniform4f(location, r, g, b, a)

Run:  python3 shaders_uniform.py        (ESC to close)
"""
import ctypes
import math
import os
import sys

import glfw
import numpy as np
from OpenGL import GL

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # so we can import glutils.py
from glutils import create_window

VERTEX_SHADER_SOURCE = """
#version 330 core
layout (location = 0) in vec3 aPos;
void main()
{
    gl_Position = vec4(aPos, 1.0);
}
"""

FRAGMENT_SHADER_SOURCE = """
#version 330 core
out vec4 FragColor;
uniform vec4 ourColor;      // set from Python every frame
void main()
{
    FragColor = ourColor;
}
"""


def compile_program(vertex_source, fragment_source):
    """Compile two shaders and link them into a program (as in lab 03)."""
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
    window = create_window(800, 600, "LearnOpenGL - Uniforms")
    shader_program = compile_program(VERTEX_SHADER_SOURCE, FRAGMENT_SHADER_SOURCE)

    vertices = np.array([
         0.5, -0.5, 0.0,    # bottom right
        -0.5, -0.5, 0.0,    # bottom left
         0.0,  0.5, 0.0,    # top
    ], dtype=np.float32)

    VAO = GL.glGenVertexArrays(1)
    VBO = GL.glGenBuffers(1)
    GL.glBindVertexArray(VAO)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW)
    GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 3 * 4, ctypes.c_void_p(0))
    GL.glEnableVertexAttribArray(0)

    # look the uniform up ONCE - its location never changes
    color_location = GL.glGetUniformLocation(shader_program, "ourColor")

    while not glfw.window_should_close(window):
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)

        GL.glClearColor(0.2, 0.3, 0.3, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glUseProgram(shader_program)            # MUST be active before glUniform

        time_value = glfw.get_time()
        green = math.sin(time_value) / 2.0 + 0.5   # 0 .. 1 .. 0 ...
        GL.glUniform4f(color_location, 0.0, green, 0.0, 1.0)

        GL.glBindVertexArray(VAO)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
