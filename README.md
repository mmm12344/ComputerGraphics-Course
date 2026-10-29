# Computer Graphics Course — Labs

Lab material for the Computer Graphics course (CS352), written in **Python
with classic OpenGL**. Each lab folder contains a `README.md` (objectives,
theory, exercises) and small commented programs that reproduce the examples
from the lectures.

## Setup

```bash
pip install PyOpenGL glfw PyGLM numpy pillow
```

| Name | Job |
|------|-----|
| OpenGL | draws points, lines and triangles |
| GLFW | opens the window, reads keyboard and mouse |
| PyOpenGL | lets Python call OpenGL (`from OpenGL import GL`) |

The shared helper `common.py` (in this folder) wraps the window/loop
boilerplate — open it once to see what `make_window`, `run`, `ortho2d` and
the draw helpers do.

## Lab 01 — Introduction

Linked lecture: *01 Introduction*.

| File | What it does | Run |
|------|--------------|-----|
| `lab_01_introduction/hello_opengl.py` | **Start here.** Your first OpenGL program: window, triangle, points, line — every call commented. | `python3 hello_opengl.py` |
| `lab_01_introduction/pixel_framebuffer.py` | A simulated frame buffer you can paint on with the mouse. | `python3 pixel_framebuffer.py` |
| `lab_01_introduction/coordinate_pipeline.py` | The same house in world, normalised and device coordinates. | `python3 coordinate_pipeline.py` |

Run from inside the lab folder:

```bash
cd lab_01_introduction
python3 hello_opengl.py
```

See `lab_01_introduction/README.md` for objectives, guided observations,
exercises and review questions.

## Lab 02 — Hello Window

From this lab on the course follows [learnopengl.com](https://learnopengl.com)
with **modern OpenGL (3.3 core profile)**: we write the window code and the
render loop ourselves instead of using `common.py`.
Linked chapters: *OpenGL*, *Creating a window*, *Hello Window*.

| File | What it does | Run |
|------|--------------|-----|
| `lab_02_hello_window/hello_window.py` | The skeleton of every modern OpenGL program: GLFW start-up, OpenGL 3.3 core context, viewport, render loop, ESC to close. | `python3 hello_window.py` |
| `lab_02_hello_window/window_input.py` | The same skeleton with keyboard input: **R/G/B** change the colour, **SPACE** animates it. | `python3 window_input.py` |

```bash
cd lab_02_hello_window
python3 hello_window.py
```

See `lab_02_hello_window/README.md` for the theory and what to observe.

## Lab 03 — Hello Triangle

The first shapes drawn with the modern pipeline: vertex data on the GPU, and our own
vertex and fragment shaders written in GLSL.
Linked chapter: *Hello Triangle*.

| File | What it does | Run |
|------|--------------|-----|
| `lab_03_hello_triangle/hello_triangle.py` | One orange triangle: VBO, VAO, vertex + fragment shader, compile/link error checks, `glDrawArrays`. | `python3 hello_triangle.py` |
| `lab_03_hello_triangle/hello_rectangle.py` | A rectangle from 4 vertices + 6 indices with an EBO and `glDrawElements`. **W** toggles wireframe mode. | `python3 hello_rectangle.py` |

```bash
cd lab_03_hello_triangle
python3 hello_triangle.py
```

See `lab_03_hello_triangle/README.md` for the theory and what to observe.

## Lab 04 — Shaders

GLSL in more depth: uniforms set from Python, several attributes per vertex and
interpolation, and a reusable `Shader` class that reads GLSL from files.
Linked chapter: *Shaders*.

From this lab on, the window start-up code of lab 02 comes from the shared helper
`glutils.py` (in this folder): `create_window(width, height, title)`.

| File | What it does | Run |
|------|--------------|-----|
| `lab_04_shaders/shaders_uniform.py` | A triangle whose green **uniform** follows `sin(time)`. | `python3 shaders_uniform.py` |
| `lab_04_shaders/shaders_interpolation.py` | Position + colour attributes; red/green/blue corners blend smoothly. | `python3 shaders_interpolation.py` |
| `lab_04_shaders/shader_class.py` | The **Shader class**, reading `shaders/shader.vs` and `shaders/shader.fs`; an `xOffset` uniform slides the triangle. | `python3 shader_class.py` |

```bash
cd lab_04_shaders
python3 shaders_uniform.py
```

See `lab_04_shaders/README.md` for the theory and what to observe.
