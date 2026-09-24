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
