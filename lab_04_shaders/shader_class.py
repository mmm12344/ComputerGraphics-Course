"""Lab 04 - Our own SHADER CLASS, reading GLSL from files.

Writing shaders inside Python strings and repeating the compile/link code
gets tiresome.  learnopengl builds a small Shader class that:

    * reads the vertex and fragment shader from FILES (shaders/shader.vs/.fs)
    * compiles and links them, reporting errors clearly
    * offers use() and easy uniform setters: set_float(), set_int(), ...

Here the class is written out in full.  From lab 05 on we import the same
class from glutils.py.

The triangle slides left/right: a float uniform 'xOffset' (see shader.vs).

Run:  python3 shader_class.py        (ESC to close)
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

HERE = os.path.dirname(os.path.abspath(__file__))


class Shader:
    def __init__(self, vertex_path, fragment_path):
        # 1. read the GLSL source code from the two files
        with open(vertex_path) as f:
            vertex_code = f.read()
        with open(fragment_path) as f:
            fragment_code = f.read()

        # 2. compile each shader
        vertex = self.compile(vertex_code, GL.GL_VERTEX_SHADER, vertex_path)
        fragment = self.compile(fragment_code, GL.GL_FRAGMENT_SHADER, fragment_path)

        # 3. link them into one program; self.ID is the program's id
        self.ID = GL.glCreateProgram()
        GL.glAttachShader(self.ID, vertex)
        GL.glAttachShader(self.ID, fragment)
        GL.glLinkProgram(self.ID)
        if not GL.glGetProgramiv(self.ID, GL.GL_LINK_STATUS):
            raise RuntimeError("PROGRAM LINKING FAILED:\n" +
                               GL.glGetProgramInfoLog(self.ID).decode())
        GL.glDeleteShader(vertex)
        GL.glDeleteShader(fragment)

    def compile(self, source, shader_type, file_name):
        shader = GL.glCreateShader(shader_type)
        GL.glShaderSource(shader, source)
        GL.glCompileShader(shader)
        if not GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS):
            raise RuntimeError(f"COMPILATION FAILED in {file_name}:\n" +
                               GL.glGetShaderInfoLog(shader).decode())
        return shader

    def use(self):
        GL.glUseProgram(self.ID)

    # uniform setters: look up the location by name, then set the value
    def set_bool(self, name, value):
        GL.glUniform1i(GL.glGetUniformLocation(self.ID, name), int(value))

    def set_int(self, name, value):
        GL.glUniform1i(GL.glGetUniformLocation(self.ID, name), value)

    def set_float(self, name, value):
        GL.glUniform1f(GL.glGetUniformLocation(self.ID, name), value)


def main():
    window = create_window(800, 600, "LearnOpenGL - Shader class")

    our_shader = Shader(os.path.join(HERE, "shaders", "shader.vs"),
                        os.path.join(HERE, "shaders", "shader.fs"))

    vertices = np.array([
        # positions         # colours
         0.5, -0.5, 0.0,    1.0, 0.0, 0.0,
        -0.5, -0.5, 0.0,    0.0, 1.0, 0.0,
         0.0,  0.5, 0.0,    0.0, 0.0, 1.0,
    ], dtype=np.float32)

    VAO = GL.glGenVertexArrays(1)
    VBO = GL.glGenBuffers(1)
    GL.glBindVertexArray(VAO)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW)
    GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 6 * 4, ctypes.c_void_p(0))
    GL.glEnableVertexAttribArray(0)
    GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4))
    GL.glEnableVertexAttribArray(1)

    while not glfw.window_should_close(window):
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)

        GL.glClearColor(0.2, 0.3, 0.3, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        our_shader.use()
        our_shader.set_float("xOffset", 0.4 * math.sin(glfw.get_time()))
        GL.glBindVertexArray(VAO)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
