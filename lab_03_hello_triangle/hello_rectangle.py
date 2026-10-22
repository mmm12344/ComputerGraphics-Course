"""Lab 03 - A rectangle with an Element Buffer Object (EBO).

A rectangle is two triangles = 6 vertices, but only 4 are different.
An EBO (Element Buffer Object) stores each corner ONCE and then lists the
INDICES of the corners each triangle uses - this is "indexed drawing":

    vertices:  0 = top right, 1 = bottom right, 2 = bottom left, 3 = top left
    indices:   triangle 1 = (0, 1, 3)     triangle 2 = (1, 2, 3)

Keys:  W = toggle WIREFRAME mode (see the two triangles)    ESC = quit
Run:  python3 hello_rectangle.py
"""
import ctypes

import glfw
import numpy as np
from OpenGL import GL

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
void main()
{
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}
"""

wireframe = False


def framebuffer_size_callback(window, width, height):
    GL.glViewport(0, 0, width, height)


def key_callback(window, key, scancode, action, mods):
    global wireframe
    if action != glfw.PRESS:
        return
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    elif key == glfw.KEY_W:
        wireframe = not wireframe


def compile_shader(source, shader_type):
    shader = GL.glCreateShader(shader_type)
    GL.glShaderSource(shader, source)
    GL.glCompileShader(shader)
    if not GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS):
        raise RuntimeError(GL.glGetShaderInfoLog(shader).decode())
    return shader


def main():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
    window = glfw.create_window(800, 600, "LearnOpenGL - Rectangle (W = wireframe)", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    glfw.set_key_callback(window, key_callback)
    GL.glViewport(0, 0, *glfw.get_framebuffer_size(window))

    # ---- shader program (same as hello_triangle.py) -------------------------
    vs = compile_shader(VERTEX_SHADER_SOURCE, GL.GL_VERTEX_SHADER)
    fs = compile_shader(FRAGMENT_SHADER_SOURCE, GL.GL_FRAGMENT_SHADER)
    shader_program = GL.glCreateProgram()
    GL.glAttachShader(shader_program, vs)
    GL.glAttachShader(shader_program, fs)
    GL.glLinkProgram(shader_program)
    GL.glDeleteShader(vs)
    GL.glDeleteShader(fs)

    # ---- 4 unique corners + 6 indices ---------------------------------------
    vertices = np.array([
         0.5,  0.5, 0.0,    # 0: top right
         0.5, -0.5, 0.0,    # 1: bottom right
        -0.5, -0.5, 0.0,    # 2: bottom left
        -0.5,  0.5, 0.0,    # 3: top left
    ], dtype=np.float32)
    indices = np.array([
        0, 1, 3,            # first triangle
        1, 2, 3,            # second triangle
    ], dtype=np.uint32)

    VAO = GL.glGenVertexArrays(1)
    VBO = GL.glGenBuffers(1)
    EBO = GL.glGenBuffers(1)

    GL.glBindVertexArray(VAO)

    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW)

    # the EBO binding is stored INSIDE the VAO (so bind it while the VAO is bound)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, EBO)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL.GL_STATIC_DRAW)

    GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 3 * 4, ctypes.c_void_p(0))
    GL.glEnableVertexAttribArray(0)

    GL.glBindVertexArray(0)          # do NOT unbind the EBO before this line!

    # ---- render loop ----------------------------------------------------------
    while not glfw.window_should_close(window):
        GL.glClearColor(0.2, 0.3, 0.3, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        # wireframe = draw only the edges of each triangle
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE if wireframe else GL.GL_FILL)

        GL.glUseProgram(shader_program)
        GL.glBindVertexArray(VAO)
        # draw 6 indices from the EBO (the last argument is the byte offset)
        GL.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, ctypes.c_void_p(0))

        glfw.swap_buffers(window)
        glfw.poll_events()

    GL.glDeleteVertexArrays(1, [VAO])
    GL.glDeleteBuffers(2, [VBO, EBO])
    GL.glDeleteProgram(shader_program)
    glfw.terminate()


if __name__ == "__main__":
    main()
