"""Lab 05 - Textures (learnopengl.com: Getting started > Textures)

A texture is an image we wrap onto a shape.  Each vertex gets a TEXTURE
COORDINATE (s, t) between 0 and 1 saying which part of the image it shows:

      (0,1) +--------+ (1,1)          The rasteriser interpolates (s, t)
            | image  |                for every fragment; the fragment
      (0,0) +--------+ (1,0)          shader SAMPLES the texture there.

Loading a texture, step by step (all in load_container_texture below):
    1. read the image file (we use Pillow - learnopengl uses stb_image)
    2. flip it vertically (images store the top row first, OpenGL the bottom)
    3. glGenTextures + glBindTexture
    4. choose WRAPPING (what happens outside 0..1) and FILTERING
       (how to pick a colour between texels / when the image is small)
    5. glTexImage2D uploads the pixels;  glGenerateMipmap makes mipmaps

Keys:  C = toggle multiplying by the vertex colours      ESC = quit
Run:  python3 textures.py
"""
import ctypes
import os
import sys

import glfw
import numpy as np
from OpenGL import GL
from PIL import Image

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # so we can import glutils.py
from glutils import Shader, create_window, texture_path

HERE = os.path.dirname(os.path.abspath(__file__))
use_vertex_color = True


def load_container_texture():
    # 1-2. load the image and flip it (OpenGL's y axis points up)
    image = Image.open(texture_path("container.jpg")).convert("RGB")
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    pixels = np.array(image, dtype=np.uint8)

    # 3. create a texture object and bind it
    texture = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture)

    # 4. wrapping (s = x direction, t = y direction) and filtering
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR_MIPMAP_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)

    # 5. upload the pixels and build the mipmaps (smaller copies of the image)
    GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, image.width, image.height, 0,
                    GL.GL_RGB, GL.GL_UNSIGNED_BYTE, pixels)
    GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
    return texture


def key_callback(window, key, scancode, action, mods):
    global use_vertex_color
    if action != glfw.PRESS:
        return
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    elif key == glfw.KEY_C:
        use_vertex_color = not use_vertex_color


def main():
    window = create_window(800, 600, "LearnOpenGL - Textures (C = vertex colours)")
    glfw.set_key_callback(window, key_callback)

    shader = Shader(os.path.join(HERE, "shaders", "texture.vs"),
                    os.path.join(HERE, "shaders", "texture.fs"))

    vertices = np.array([
        # positions        # colours        # texture coords
         0.5,  0.5, 0.0,   1.0, 0.0, 0.0,   1.0, 1.0,   # top right
         0.5, -0.5, 0.0,   0.0, 1.0, 0.0,   1.0, 0.0,   # bottom right
        -0.5, -0.5, 0.0,   0.0, 0.0, 1.0,   0.0, 0.0,   # bottom left
        -0.5,  0.5, 0.0,   1.0, 1.0, 0.0,   0.0, 1.0,   # top left
    ], dtype=np.float32)
    indices = np.array([0, 1, 3, 1, 2, 3], dtype=np.uint32)

    VAO = GL.glGenVertexArrays(1)
    VBO, EBO = GL.glGenBuffers(2)
    GL.glBindVertexArray(VAO)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, EBO)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL.GL_STATIC_DRAW)

    stride = 8 * 4                                  # 8 floats per vertex
    GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, ctypes.c_void_p(0))
    GL.glEnableVertexAttribArray(0)                 # position
    GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, ctypes.c_void_p(3 * 4))
    GL.glEnableVertexAttribArray(1)                 # colour
    GL.glVertexAttribPointer(2, 2, GL.GL_FLOAT, GL.GL_FALSE, stride, ctypes.c_void_p(6 * 4))
    GL.glEnableVertexAttribArray(2)                 # texture coordinate

    texture = load_container_texture()

    while not glfw.window_should_close(window):
        GL.glClearColor(0.2, 0.3, 0.3, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
        shader.use()
        shader.set_bool("useVertexColor", use_vertex_color)
        GL.glBindVertexArray(VAO)
        GL.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, ctypes.c_void_p(0))

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
