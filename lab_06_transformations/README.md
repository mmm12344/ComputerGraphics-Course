# Lab 06 — Transformations

**Based on learnopengl.com:** [Transformations](https://learnopengl.com/Getting-started/Transformations)

## Objectives

- Use **vectors**: addition, scaling, length, normalisation, **dot** and **cross** products.
- Use **matrices**: identity, **scaling**, **translation**, **rotation**, and combining them.
- Understand **homogeneous coordinates** (the `w` component).
- Do the maths with **GLM** (PyGLM) and send a matrix to a shader as a **uniform**.

## Theory

**Vectors.** `length(v)`; `normalize(v)` gives a unit vector; `dot(a, b) = |a||b|cos θ`
(1 for the same direction, 0 for perpendicular); `cross(a, b)` is perpendicular to both.

**Matrices (4×4).**

```
scale (Sx,Sy,Sz)        translate (Tx,Ty,Tz)        rotate θ about z
| Sx 0  0  0 |          | 1 0 0 Tx |                | cosθ -sinθ 0 0 |
| 0  Sy 0  0 |          | 0 1 0 Ty |                | sinθ  cosθ 0 0 |
| 0  0  Sz 0 |          | 0 0 1 Tz |                |  0     0   1 0 |
| 0  0  0  1 |          | 0 0 0 1  |                |  0     0   0 1 |
```

**Homogeneous coordinates.** Points are `vec4(x, y, z, 1)`; with `w = 1` translation
works. A *direction* uses `w = 0`, so translation does not move it.

**Combining.** Matrices multiply into one matrix that does everything. They apply
**right to left**: `T * R * v` rotates first, then translates. The recommended order is
scale, then rotate, then translate (read right to left: `T * R * S`).

**GLM in Python** — `pip install PyGLM`, same names as the C++ library:

```python
trans = glm.mat4(1.0)                                          # identity
trans = glm.translate(trans, glm.vec3(0.5, -0.5, 0.0))
trans = glm.rotate(trans, glfw.get_time(), glm.vec3(0, 0, 1))  # radians
shader.set_mat4("transform", trans)   # glUniformMatrix4fv(..., glm.value_ptr(trans))
```

In the vertex shader: `gl_Position = transform * vec4(aPos, 1.0);`

## Files

| File | What it does | Run |
|------|--------------|-----|
| `glm_basics.py` | Console only: every vector and matrix example of the chapter, printed. | `python3 glm_basics.py` |
| `transformations.py` | A container that rotates in the bottom-right corner, and a second one in the top-left that scales with `sin(time)`. **O** swaps the matrix order. | `python3 transformations.py` |
| `shaders/` | `transform.vs` (uses `uniform mat4 transform`) and `transform.fs`. | — |

## What to observe

1. `glm_basics.py` prints `(2, 1, 0, 1)` for the translated point and `(1, 0, 0, 0)`
   for the translated *direction* — `w` decides.
2. The two containers use the **same vertex data**; only the matrix changes between draw calls.
3. Press **O**: rotating *after* translating makes the box orbit around the window centre
   instead of spinning in place — matrix order matters.
