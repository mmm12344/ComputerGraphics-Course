# Lab 01 — Introduction: OpenGL, Pixels, the Frame Buffer, and Coordinate Systems

**Linked lecture:** `01 Introduction.pptx`

## Objectives

By the end of this lab you will be able to:

- Run your **first OpenGL program** and understand the window + render-loop pattern.
- Explain what a **frame buffer** is and how its contents become the image on screen.
- Describe the three coordinate systems of the graphics pipeline:
  **world → normalised device (NDC) → device (screen) coordinates**.
- Convert a point between the three coordinate systems by hand and in code.

## Before you start

Install the two libraries (once):

```bash
pip install PyOpenGL glfw
```

| Name | Job |
|------|-----|
| OpenGL | draws points, lines and triangles |
| GLFW | opens the window, reads keyboard and mouse |
| PyOpenGL | lets Python call OpenGL (`from OpenGL import GL`) |

## Files

| File | What it does | Run |
|------|--------------|-----|
| `hello_opengl.py` | **Start here.** Your first OpenGL program: open a window, draw a triangle, points and a line. Every OpenGL call is commented. | `python3 hello_opengl.py` |
| `pixel_framebuffer.py` | An interactive simulated frame buffer: paint pixels with the mouse and watch them stored in a 2-D list (the buffer). | `python3 pixel_framebuffer.py` |
| `coordinate_pipeline.py` | The same house drawn three times — world, normalised, device — and one point's journey printed to the console. | `python3 coordinate_pipeline.py` |

Controls: `pixel_framebuffer.py` — **left-drag** paint, **right-drag** erase,
**1/2/3** simulate 1 / 3 / 24 bits per pixel, **R G B Y** paint colours,
**C** clear. All programs close with **ESC**.

## What to observe

1. In `hello_opengl.py`: the window is redrawn ~60 times per second — the small dot at the bottom breathes because every frame recomputes its colour from the clock. Every lab program uses this same `draw()` loop.
2. In `pixel_framebuffer.py`, press **1** (1-bit mode) and paint: the buffer can only store *on/off*, so detail is lost. Bit depth limits colour resolution.
3. In `coordinate_pipeline.py`, the house shape never changes — only its coordinate system does. In the third panel the corners sit at *integer pixels*: that is where scan conversion (lab 03) happens.
4. Check one mapping by hand: `ndc_x = (x − wl)/(wr − wl)`, then `device_x = round(ndc_x · (W − 1))`.

## Lab exercises

1. In `hello_opengl.py`, change the triangle's three vertices and its colour. Then add a **second** triangle that overlaps the first.
2. In `pixel_framebuffer.py`, draw a 10-pixel horizontal line and export nothing — just count the lit pixels. Does it match the pixels you intended to cover?
3. Edit `A` and `B`-style constants: in `coordinate_pipeline.py` change `WORLD` to `(0, 10, 0, 10)` so the house sits *outside* the window. What do you see? That is the problem **clipping** (lab 11) solves.
4. Write `device_to_world(px, py, world, W, H)` — the inverse of the pipeline — and check it round-trips a few points.

## Review questions

1. A frame buffer is 1024×768 with 24 bits per pixel. How much memory does it hold?
2. Why does a raster display produce jagged lines while a vector display does not?
3. Why do normalised device coordinates exist between world and device coordinates?
4. In `hello_opengl.py`, what is the difference between `glClearColor` and `glColor3f`?
