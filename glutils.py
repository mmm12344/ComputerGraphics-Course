"""glutils.py - the reusable pieces built during labs 02-08.

Each lab first writes a piece itself; later labs import the finished version
from here, so their files stay short:

    create_window(...)   - the GLFW start-up code of lab 02 (Hello Window)
    Shader               - the shader class of lab 04 (Shaders)
    load_texture(...)    - the texture loading code of lab 05 (Textures)
    CUBE_VERTICES        - the 36-vertex cube of lab 07 (positions, normals,
                           texture coordinates)
    Camera               - the camera class of lab 08 (Camera)

Requires:  pip install PyOpenGL glfw PyGLM numpy pillow
"""
import ctypes
import math
import os

import glfw
import glm
import numpy as np
from OpenGL import GL
from PIL import Image

RESOURCES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")


# ===========================================================================
# window (lab 02)
# ===========================================================================
def create_window(width=800, height=600, title="LearnOpenGL"):
    """Initialise GLFW, open a window with an OpenGL 3.3 core context."""
    if not glfw.init():
        raise RuntimeError("Failed to initialise GLFW")
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)     # needed on macOS
    window = glfw.create_window(width, height, title, None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Failed to create the GLFW window")
    glfw.make_context_current(window)

    # keep the viewport the same size as the window when it is resized
    def framebuffer_size_callback(win, w, h):
        GL.glViewport(0, 0, w, h)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    w, h = glfw.get_framebuffer_size(window)
    GL.glViewport(0, 0, w, h)
    return window


# ===========================================================================
# Shader class (lab 04)
# ===========================================================================
class Shader:
    """Reads a vertex + fragment shader from files, compiles and links them."""

    def __init__(self, vertex_path, fragment_path):
        with open(vertex_path) as f:
            vertex_code = f.read()
        with open(fragment_path) as f:
            fragment_code = f.read()

        vertex = self._compile(vertex_code, GL.GL_VERTEX_SHADER, vertex_path)
        fragment = self._compile(fragment_code, GL.GL_FRAGMENT_SHADER, fragment_path)

        self.ID = GL.glCreateProgram()
        GL.glAttachShader(self.ID, vertex)
        GL.glAttachShader(self.ID, fragment)
        GL.glLinkProgram(self.ID)
        if not GL.glGetProgramiv(self.ID, GL.GL_LINK_STATUS):
            raise RuntimeError("Shader link error:\n" +
                               GL.glGetProgramInfoLog(self.ID).decode())
        GL.glDeleteShader(vertex)          # linked into the program - no longer needed
        GL.glDeleteShader(fragment)

    @staticmethod
    def _compile(source, kind, name):
        shader = GL.glCreateShader(kind)
        GL.glShaderSource(shader, source)
        GL.glCompileShader(shader)
        if not GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS):
            raise RuntimeError(f"Shader compile error in {name}:\n" +
                               GL.glGetShaderInfoLog(shader).decode())
        return shader

    def use(self):
        GL.glUseProgram(self.ID)

    # --- uniform setters ---------------------------------------------------
    def _loc(self, name):
        return GL.glGetUniformLocation(self.ID, name)

    def set_bool(self, name, value):
        GL.glUniform1i(self._loc(name), int(value))

    def set_int(self, name, value):
        GL.glUniform1i(self._loc(name), value)

    def set_float(self, name, value):
        GL.glUniform1f(self._loc(name), value)

    def set_vec3(self, name, x, y=None, z=None):
        if y is None:                       # a glm.vec3 was passed
            x, y, z = x.x, x.y, x.z
        GL.glUniform3f(self._loc(name), x, y, z)

    def set_mat4(self, name, matrix):
        GL.glUniformMatrix4fv(self._loc(name), 1, GL.GL_FALSE, glm.value_ptr(matrix))


# ===========================================================================
# textures (lab 05)
# ===========================================================================
def load_texture(path, flip=True):
    """Load an image file into a new OpenGL texture and return its id."""
    image = Image.open(path)
    if flip:                                # OpenGL expects y = 0 at the BOTTOM
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
    if image.mode == "RGBA":
        fmt = GL.GL_RGBA
    else:
        image = image.convert("RGB")
        fmt = GL.GL_RGB
    data = np.array(image, dtype=np.uint8)

    texture = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR_MIPMAP_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, fmt, image.width, image.height, 0,
                    fmt, GL.GL_UNSIGNED_BYTE, data)
    GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
    return texture


def texture_path(name):
    """Full path of a file in resources/textures/."""
    return os.path.join(RESOURCES, "textures", name)


# ===========================================================================
# cube data (lab 07) - 36 vertices: position (3), normal (3), tex coord (2)
# ===========================================================================
CUBE_VERTICES = np.array([
    # positions          # normals           # texture coords
    -0.5, -0.5, -0.5,    0.0,  0.0, -1.0,    0.0, 0.0,
     0.5, -0.5, -0.5,    0.0,  0.0, -1.0,    1.0, 0.0,
     0.5,  0.5, -0.5,    0.0,  0.0, -1.0,    1.0, 1.0,
     0.5,  0.5, -0.5,    0.0,  0.0, -1.0,    1.0, 1.0,
    -0.5,  0.5, -0.5,    0.0,  0.0, -1.0,    0.0, 1.0,
    -0.5, -0.5, -0.5,    0.0,  0.0, -1.0,    0.0, 0.0,

    -0.5, -0.5,  0.5,    0.0,  0.0,  1.0,    0.0, 0.0,
     0.5, -0.5,  0.5,    0.0,  0.0,  1.0,    1.0, 0.0,
     0.5,  0.5,  0.5,    0.0,  0.0,  1.0,    1.0, 1.0,
     0.5,  0.5,  0.5,    0.0,  0.0,  1.0,    1.0, 1.0,
    -0.5,  0.5,  0.5,    0.0,  0.0,  1.0,    0.0, 1.0,
    -0.5, -0.5,  0.5,    0.0,  0.0,  1.0,    0.0, 0.0,

    -0.5,  0.5,  0.5,   -1.0,  0.0,  0.0,    1.0, 0.0,
    -0.5,  0.5, -0.5,   -1.0,  0.0,  0.0,    1.0, 1.0,
    -0.5, -0.5, -0.5,   -1.0,  0.0,  0.0,    0.0, 1.0,
    -0.5, -0.5, -0.5,   -1.0,  0.0,  0.0,    0.0, 1.0,
    -0.5, -0.5,  0.5,   -1.0,  0.0,  0.0,    0.0, 0.0,
    -0.5,  0.5,  0.5,   -1.0,  0.0,  0.0,    1.0, 0.0,

     0.5,  0.5,  0.5,    1.0,  0.0,  0.0,    1.0, 0.0,
     0.5,  0.5, -0.5,    1.0,  0.0,  0.0,    1.0, 1.0,
     0.5, -0.5, -0.5,    1.0,  0.0,  0.0,    0.0, 1.0,
     0.5, -0.5, -0.5,    1.0,  0.0,  0.0,    0.0, 1.0,
     0.5, -0.5,  0.5,    1.0,  0.0,  0.0,    0.0, 0.0,
     0.5,  0.5,  0.5,    1.0,  0.0,  0.0,    1.0, 0.0,

    -0.5, -0.5, -0.5,    0.0, -1.0,  0.0,    0.0, 1.0,
     0.5, -0.5, -0.5,    0.0, -1.0,  0.0,    1.0, 1.0,
     0.5, -0.5,  0.5,    0.0, -1.0,  0.0,    1.0, 0.0,
     0.5, -0.5,  0.5,    0.0, -1.0,  0.0,    1.0, 0.0,
    -0.5, -0.5,  0.5,    0.0, -1.0,  0.0,    0.0, 0.0,
    -0.5, -0.5, -0.5,    0.0, -1.0,  0.0,    0.0, 1.0,

    -0.5,  0.5, -0.5,    0.0,  1.0,  0.0,    0.0, 1.0,
     0.5,  0.5, -0.5,    0.0,  1.0,  0.0,    1.0, 1.0,
     0.5,  0.5,  0.5,    0.0,  1.0,  0.0,    1.0, 0.0,
     0.5,  0.5,  0.5,    0.0,  1.0,  0.0,    1.0, 0.0,
    -0.5,  0.5,  0.5,    0.0,  1.0,  0.0,    0.0, 0.0,
    -0.5,  0.5, -0.5,    0.0,  1.0,  0.0,    0.0, 1.0,
], dtype=np.float32)

CUBE_POSITIONS = [                        # the ten cubes of lab 07 onwards
    glm.vec3(0.0, 0.0, 0.0), glm.vec3(2.0, 5.0, -15.0),
    glm.vec3(-1.5, -2.2, -2.5), glm.vec3(-3.8, -2.0, -12.3),
    glm.vec3(2.4, -0.4, -3.5), glm.vec3(-1.7, 3.0, -7.5),
    glm.vec3(1.3, -2.0, -2.5), glm.vec3(1.5, 2.0, -2.5),
    glm.vec3(1.5, 0.2, -1.5), glm.vec3(-1.3, 1.0, -1.5),
]


def make_cube_vao(with_normals=True, with_texcoords=True):
    """Upload CUBE_VERTICES and return a VAO with the requested attributes:
    location 0 = position, 1 = normal, 2 = texture coordinate."""
    vao = GL.glGenVertexArrays(1)
    vbo = GL.glGenBuffers(1)
    GL.glBindVertexArray(vao)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, CUBE_VERTICES.nbytes, CUBE_VERTICES, GL.GL_STATIC_DRAW)
    stride = 8 * 4                           # 8 floats per vertex, 4 bytes each
    GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, ctypes.c_void_p(0))
    GL.glEnableVertexAttribArray(0)
    if with_normals:
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, ctypes.c_void_p(3 * 4))
        GL.glEnableVertexAttribArray(1)
    if with_texcoords:
        GL.glVertexAttribPointer(2, 2, GL.GL_FLOAT, GL.GL_FALSE, stride, ctypes.c_void_p(6 * 4))
        GL.glEnableVertexAttribArray(2)
    GL.glBindVertexArray(0)
    return vao


# ===========================================================================
# Camera class (lab 08) - a fly-style camera using Euler angles
# ===========================================================================
FORWARD, BACKWARD, LEFT, RIGHT = "FORWARD", "BACKWARD", "LEFT", "RIGHT"


class Camera:
    def __init__(self, position=glm.vec3(0.0, 0.0, 3.0), up=glm.vec3(0.0, 1.0, 0.0),
                 yaw=-90.0, pitch=0.0):
        self.position = glm.vec3(position)
        self.world_up = glm.vec3(up)
        self.yaw = yaw                      # left/right angle (degrees)
        self.pitch = pitch                  # up/down angle (degrees)
        self.movement_speed = 2.5           # units per second
        self.mouse_sensitivity = 0.1
        self.zoom = 45.0                    # field of view (degrees)
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.right = glm.vec3(1.0, 0.0, 0.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)
        self.update_vectors()

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.front, self.up)

    def process_keyboard(self, direction, delta_time):
        velocity = self.movement_speed * delta_time
        if direction == FORWARD:
            self.position += self.front * velocity
        if direction == BACKWARD:
            self.position -= self.front * velocity
        if direction == LEFT:
            self.position -= self.right * velocity
        if direction == RIGHT:
            self.position += self.right * velocity

    def process_mouse_movement(self, x_offset, y_offset, constrain_pitch=True):
        self.yaw += x_offset * self.mouse_sensitivity
        self.pitch += y_offset * self.mouse_sensitivity
        if constrain_pitch:                 # don't flip over the top
            self.pitch = max(-89.0, min(89.0, self.pitch))
        self.update_vectors()

    def process_mouse_scroll(self, y_offset):
        self.zoom = max(1.0, min(45.0, self.zoom - y_offset))

    def update_vectors(self):
        """Recompute front/right/up from the yaw and pitch angles."""
        front = glm.vec3(math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch)),
                         math.sin(math.radians(self.pitch)),
                         math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch)))
        self.front = glm.normalize(front)
        self.right = glm.normalize(glm.cross(self.front, self.world_up))
        self.up = glm.normalize(glm.cross(self.right, self.front))


class CameraControls:
    """The input code of lab 08 (camera_class.py) packed into one object:
    mouse look, scroll zoom, W A S D movement and ESC to quit.

        controls = CameraControls(window, camera)
        ...
        while not glfw.window_should_close(window):
            delta_time = controls.update()      # handles the keyboard, returns dt
    """

    def __init__(self, window, camera):
        self.window = window
        self.camera = camera
        self.first_mouse = True
        self.last_x = self.last_y = 0.0
        self.last_frame = glfw.get_time()
        glfw.set_cursor_pos_callback(window, self.mouse_callback)
        glfw.set_scroll_callback(window, self.scroll_callback)
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    def mouse_callback(self, window, xpos, ypos):
        if self.first_mouse:
            self.last_x, self.last_y = xpos, ypos
            self.first_mouse = False
        self.camera.process_mouse_movement(xpos - self.last_x, self.last_y - ypos)
        self.last_x, self.last_y = xpos, ypos

    def scroll_callback(self, window, x_offset, y_offset):
        self.camera.process_mouse_scroll(y_offset)

    def update(self):
        """Call once per frame: moves the camera, returns delta time."""
        now = glfw.get_time()
        delta_time = now - self.last_frame
        self.last_frame = now
        w = self.window
        if glfw.get_key(w, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(w, True)
        for key, direction in [(glfw.KEY_W, FORWARD), (glfw.KEY_S, BACKWARD),
                               (glfw.KEY_A, LEFT), (glfw.KEY_D, RIGHT)]:
            if glfw.get_key(w, key) == glfw.PRESS:
                self.camera.process_keyboard(direction, delta_time)
        return delta_time
