# Lab 02 — Hello Window

**Based on learnopengl.com:** [OpenGL](https://learnopengl.com/Getting-started/OpenGL) ·
[Creating a window](https://learnopengl.com/Getting-started/Creating-a-window) ·
[Hello Window](https://learnopengl.com/Getting-started/Hello-Window)

## Objectives

- Understand what **modern (core-profile) OpenGL** is, and how it differs from the classic `glBegin/glEnd` OpenGL of lab 01.
- Open a window with **GLFW** and request an **OpenGL 3.3 core** context.
- Write the **render loop** that every program from now on uses: input → render → swap buffers → poll events.
- Use **double buffering**, the **viewport**, and **keyboard input**.

## Theory

**OpenGL is a specification**, implemented by your graphics driver. It works as a big
**state machine**: some functions *set* state (`glClearColor` chooses a colour),
others *use* it (`glClear` fills the screen with that colour).

**Immediate mode vs core profile.** Lab 01 used the old *immediate mode*
(`glBegin`, `glVertex2f`, `glEnd`): easy, but slow and inflexible. Since OpenGL 3.3
the **core profile** removes it: you send vertex data to the GPU in buffers and write
small programs — **shaders** — that run on the GPU. Everything from lab 03 on is core
profile, exactly as on learnopengl.com.

**Libraries in Python**

| C++ (learnopengl) | Python (these labs) | Job |
|---|---|---|
| GLFW | `glfw` | window, OpenGL context, keyboard and mouse |
| GLAD | `PyOpenGL` (`from OpenGL import GL`) | gives access to the OpenGL functions |
| GLM | `PyGLM` (`import glm`) | vector and matrix maths (from lab 06) |
| stb_image | `Pillow` | loading images (from lab 05) |

```bash
pip install PyOpenGL glfw PyGLM numpy pillow
```

**The skeleton of every program**

1. `glfw.init()` and *window hints*: OpenGL 3.3, core profile (plus forward-compat for macOS).
2. `glfw.create_window(...)`, then `glfw.make_context_current(window)`.
3. `glViewport(0, 0, width, height)` — where OpenGL draws inside the window; a
   *framebuffer size callback* updates it when the window is resized.
4. The **render loop**, once per frame:
   `process_input` → draw → `glfw.swap_buffers` → `glfw.poll_events`.
5. `glfw.terminate()`.

**Double buffering:** we draw into an invisible *back buffer*; `swap_buffers`
shows it all at once, so you never see a half-drawn frame.

## Files

| File | What it does | Run |
|------|--------------|-----|
| `hello_window.py` | The complete skeleton: a window cleared to dark teal; ESC closes it. Every line is commented. | `python3 hello_window.py` |
| `window_input.py` | Same skeleton with more input: **R / G / B** choose the background colour, **SPACE** animates it, **ESC** quits. Shows *polled* keys vs a *key callback*. | `python3 window_input.py` |

## What to observe

1. `hello_window.py` prints the OpenGL version your driver provides — it must be 3.3 or higher.
2. Resize the window: the framebuffer size callback keeps the viewport matching the window.
3. In `window_input.py`, **SPACE** makes the colour pulse — proof that the whole
   frame is redrawn many times per second.
4. Compare with lab 01's `hello_opengl.py`: the loop is the same idea, but from now
   on we write it ourselves instead of using `common.run`.
