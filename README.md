# Computer Graphics Course — Labs

Lab material for the Computer Graphics course (CS352), written in **Python
with classic OpenGL**. Each lab folder contains a `README.md` (objectives,
theory, exercises) and small commented programs that reproduce the examples
from the lectures.

## Setup

```bash
pip install PyOpenGL glfw
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
