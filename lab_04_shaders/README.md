# Lab 04 — Shaders

**Based on learnopengl.com:** [Shaders](https://learnopengl.com/Getting-started/Shaders)

## Objectives

- Read and write **GLSL**: types, vectors, swizzling.
- Pass data between shaders with **`in` / `out`** variables.
- Set **uniforms** from Python and animate with them.
- Give each vertex **several attributes** (position + colour) and see **interpolation**.
- Build a reusable **Shader class** that reads shaders from files.

## Theory

**GLSL basics.** Every shader starts with `#version 330 core`. Types include
`float`, `int`, `bool` and vectors `vec2`, `vec3`, `vec4`. Components are
`.x .y .z .w` (or `.r .g .b .a`), and can be **swizzled**: `v.xyz`, `v.zyx`, `v.xxyy`.

**Ins and outs.** The vertex shader reads vertex attributes declared with
`layout (location = N) in ...`. It sends data on with `out`; the fragment shader
receives it with an `in` of the **same name and type**. The fragment shader must
output a `vec4` colour.

**Uniforms** are global values set from the CPU, the same for every vertex and fragment,
and they keep their value until changed:

```python
location = glGetUniformLocation(program, "ourColor")   # find it
glUseProgram(program)                                  # program must be active
glUniform4f(location, 0.0, green, 0.0, 1.0)            # set it
```

**More attributes.** With position *and* colour in one buffer, each vertex is 6 floats:
the stride is `6 * 4` bytes and the colour starts at offset `3 * 4` bytes.

**Interpolation.** Outputs of the vertex shader are *interpolated* across the triangle
for every fragment — three corner colours become a smooth gradient.

**The Shader class** (learnopengl's `shader_s.h`) reads `shader.vs` and `shader.fs`,
compiles, links, reports errors, and offers `use()`, `set_float()`, `set_int()`, …
It is written out in full in `shader_class.py`; from lab 05 on the same class is
imported from `glutils.py`.

From this lab on, the window start-up code of lab 02 comes from
`glutils.create_window(width, height, title)` — open `glutils.py` to see it.

## Files

| File | What it does | Run |
|------|--------------|-----|
| `shaders_uniform.py` | A triangle whose green **uniform** follows `sin(time)`. | `python3 shaders_uniform.py` |
| `shaders_interpolation.py` | Position + colour attributes; red/green/blue corners blend smoothly. | `python3 shaders_interpolation.py` |
| `shader_class.py` | The **Shader class**, reading `shaders/shader.vs` and `shaders/shader.fs`; an `xOffset` uniform slides the triangle. | `python3 shader_class.py` |
| `shaders/shader.vs`, `shaders/shader.fs` | The GLSL files used by `shader_class.py`. | — |

## What to observe

1. In `shaders_uniform.py`, the uniform is set **every frame**, after `glUseProgram`.
2. In `shaders_interpolation.py`, only three colours are given, yet every pixel inside
   gets its own colour — that is interpolation by the rasteriser.
3. Edit `shaders/shader.vs` and run `shader_class.py` again — no Python change needed,
   because the shader is read from the file at start-up.
