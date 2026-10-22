"""Lab 03 - Hello Triangle (learnopengl.com: Getting started > Hello Triangle)

Drawing ONE orange triangle needs every stage of the modern pipeline:

    vertex data (numpy array)
      -> VBO  (Vertex Buffer Object: the data copied into GPU memory)
      -> VAO  (Vertex Array Object: remembers HOW to read the VBO)
      -> VERTEX SHADER   (runs once per vertex, outputs gl_Position)
      -> rasterisation   (OpenGL turns the triangle into fragments/pixels)
      -> FRAGMENT SHADER (runs once per fragment, outputs its colour)

Run:  python3 hello_triangle.py        (ESC to close)
"""
import ctypes

import glfw
import numpy as np
from OpenGL import GL

# ---------------------------------------------------------------------------
# the two shaders, written in GLSL (the OpenGL Shading Language)
# ---------------------------------------------------------------------------
VERTEX_SHADER_SOURCE = """
#version 330 core
layout (location = 0) in vec3 aPos;     // attribute 0 = the vertex position

void main()
{
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
"""

FRAGMENT_SHADER_SOURCE = """
#version 330 core
out vec4 FragColor;                      // the colour of this fragment

void main()
{
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);   // orange
}
"""


def framebuffer_size_callback(window, width, height):
    GL.glViewport(0, 0, width, height)


def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def compile_shader(source, shader_type):
    """Create a shader object, compile it, and stop with a clear message if
    the GLSL code has an error."""
    shader = GL.glCreateShader(shader_type)
    GL.glShaderSource(shader, source)
    GL.glCompileShader(shader)
    if not GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS):
        raise RuntimeError("SHADER COMPILATION FAILED:\n" +
                           GL.glGetShaderInfoLog(shader).decode())
    return shader


def main():
    # ---- window (exactly as in lab 02) ------------------------------------
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
    window = glfw.create_window(800, 600, "LearnOpenGL - Hello Triangle", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    GL.glViewport(0, 0, *glfw.get_framebuffer_size(window))

    # ---- build the shader program -----------------------------------------
    vertex_shader = compile_shader(VERTEX_SHADER_SOURCE, GL.GL_VERTEX_SHADER)
    fragment_shader = compile_shader(FRAGMENT_SHADER_SOURCE, GL.GL_FRAGMENT_SHADER)

    shader_program = GL.glCreateProgram()          # link both into one program
    GL.glAttachShader(shader_program, vertex_shader)
    GL.glAttachShader(shader_program, fragment_shader)
    GL.glLinkProgram(shader_program)
    if not GL.glGetProgramiv(shader_program, GL.GL_LINK_STATUS):
        raise RuntimeError("PROGRAM LINKING FAILED:\n" +
                           GL.glGetProgramInfoLog(shader_program).decode())
    GL.glDeleteShader(vertex_shader)               # not needed after linking
    GL.glDeleteShader(fragment_shader)

    # ---- vertex data: three corners in NORMALISED DEVICE COORDINATES -------
    # (x, y, z) each between -1 and 1; (0, 0) is the centre of the window
    vertices = np.array([
        -0.5, -0.5, 0.0,     # left
         0.5, -0.5, 0.0,     # right
         0.0,  0.5, 0.0,     # top
    ], dtype=np.float32)

    VAO = GL.glGenVertexArrays(1)
    VBO = GL.glGenBuffers(1)

    # bind the VAO FIRST: it records everything we set up next
    GL.glBindVertexArray(VAO)

    # copy the vertices into the buffer on the GPU
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW)

    # explain the layout of the data to OpenGL:
    #   attribute 0, 3 floats per vertex, not normalised,
    #   stride = 3 floats * 4 bytes, the data starts at offset 0
    GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 3 * 4, ctypes.c_void_p(0))
    GL.glEnableVertexAttribArray(0)

    # unbind (optional - just good practice)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindVertexArray(0)

    # ---- render loop --------------------------------------------------------
    while not glfw.window_should_close(window):
        process_input(window)

        GL.glClearColor(0.2, 0.3, 0.3, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        # draw the triangle
        GL.glUseProgram(shader_program)
        GL.glBindVertexArray(VAO)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)     # 3 vertices from index 0

        glfw.swap_buffers(window)
        glfw.poll_events()

    # ---- clean up -------------------------------------------------------------
    GL.glDeleteVertexArrays(1, [VAO])
    GL.glDeleteBuffers(1, [VBO])
    GL.glDeleteProgram(shader_program)
    glfw.terminate()


if __name__ == "__main__":
    main()
