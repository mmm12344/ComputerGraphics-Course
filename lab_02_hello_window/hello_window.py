"""Lab 02 - Hello Window (learnopengl.com: Getting started > Hello Window)

The skeleton of EVERY modern OpenGL program:

    1. initialise GLFW and ask for an OpenGL 3.3 CORE profile context
    2. create a window and make its context current
    3. tell OpenGL the size of the drawing area (the viewport)
    4. the RENDER LOOP:  input -> render -> swap buffers -> poll events
    5. clean up when the loop ends

Run:  python3 hello_window.py        (press ESC to close)
"""
import glfw
from OpenGL import GL

SCR_WIDTH = 800
SCR_HEIGHT = 600


def framebuffer_size_callback(window, width, height):
    """Called by GLFW whenever the window is resized:
    make the viewport match the new window size."""
    GL.glViewport(0, 0, width, height)


def process_input(window):
    """Check the keyboard once per frame."""
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def main():
    # ---- 1. initialise GLFW and choose the OpenGL version ----------------
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)     # OpenGL 3.3 ...
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)  # ... core
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)  # required on macOS

    # ---- 2. create the window ---------------------------------------------
    window = glfw.create_window(SCR_WIDTH, SCR_HEIGHT, "LearnOpenGL", None, None)
    if not window:
        print("Failed to create GLFW window")
        glfw.terminate()
        return
    glfw.make_context_current(window)   # OpenGL calls now draw into this window

    # ---- 3. the viewport ---------------------------------------------------
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    width, height = glfw.get_framebuffer_size(window)
    GL.glViewport(0, 0, width, height)

    print("OpenGL version:", GL.glGetString(GL.GL_VERSION).decode())

    # ---- 4. the render loop: runs once per frame until the window closes ---
    while not glfw.window_should_close(window):
        # input
        process_input(window)

        # rendering: fill the whole window with one colour
        GL.glClearColor(0.2, 0.3, 0.3, 1.0)   # STATE-SETTING function
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)      # STATE-USING function

        # show the finished frame and handle window events
        glfw.swap_buffers(window)   # double buffering: back buffer -> screen
        glfw.poll_events()          # keyboard, mouse, resize, close button ...

    # ---- 5. clean up -------------------------------------------------------
    glfw.terminate()


if __name__ == "__main__":
    main()
