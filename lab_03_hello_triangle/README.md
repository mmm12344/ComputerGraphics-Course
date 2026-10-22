# Lab 03 — Hello Triangle

**Based on learnopengl.com:** [Hello Triangle](https://learnopengl.com/Getting-started/Hello-Triangle)

## Objectives

- Know the stages of the **graphics pipeline** and which ones we program (vertex and fragment shaders).
- Send vertex data to the GPU with a **VBO** and describe its layout with a **VAO**.
- Write, compile and link a **vertex shader** and a **fragment shader** into a **shader program**.
- Draw with `glDrawArrays`, then with indices using an **EBO** and `glDrawElements`.
- Use **wireframe mode**.

## Theory

**The graphics pipeline** turns 3D coordinates into coloured pixels:

```
vertex data → VERTEX SHADER → shape assembly → geometry shader → rasterisation
            → FRAGMENT SHADER → tests and blending → screen
```

We must write the **vertex shader** (once per vertex, outputs `gl_Position`) and the
**fragment shader** (once per fragment, outputs its colour). The others are fixed or optional.

**Normalised Device Coordinates (NDC):** after the vertex shader, visible coordinates
lie between −1 and 1 on every axis; (0, 0) is the window centre.

**Objects that hold the data**

| Object | Holds | Key calls |
|---|---|---|
| **VBO** (Vertex Buffer Object) | the vertex data, in GPU memory | `glGenBuffers`, `glBindBuffer(GL_ARRAY_BUFFER)`, `glBufferData` |
| **VAO** (Vertex Array Object) | *how* to read the VBO (attribute layout) + the bound EBO | `glGenVertexArrays`, `glBindVertexArray` |
| **EBO** (Element Buffer Object) | indices: which vertices form each triangle | `glBindBuffer(GL_ELEMENT_ARRAY_BUFFER)` |

**Describing the layout:** `glVertexAttribPointer(location, size, type, normalise, stride, offset)`
tells OpenGL where attribute `location` lives in the buffer; `glEnableVertexAttribArray(location)` switches it on.

**Shaders** are written in **GLSL**. They are compiled at run time:
`glCreateShader` → `glShaderSource` → `glCompileShader` (check `GL_COMPILE_STATUS`!),
then linked: `glCreateProgram` → `glAttachShader` → `glLinkProgram`. Activate with `glUseProgram`.

**Indexed drawing:** a rectangle is two triangles but only four distinct corners. An
EBO stores the four corners once and the six indices `0,1,3, 1,2,3`.

## Files

| File | What it does | Run |
|------|--------------|-----|
| `hello_triangle.py` | One orange triangle: VBO, VAO, both shaders (as Python strings), error checks, draw. | `python3 hello_triangle.py` |
| `hello_rectangle.py` | A rectangle from 4 vertices + 6 indices with an EBO. **W** toggles wireframe mode. | `python3 hello_rectangle.py` |

## What to observe

1. The order of setup in `hello_triangle.py`: bind the **VAO first**, then the VBO
   and attribute pointers — the VAO *records* that configuration.
2. Put a typo in the GLSL code: the program stops with the compiler's error message
   (that is why we check `GL_COMPILE_STATUS`).
3. Press **W** in `hello_rectangle.py`: wireframe mode (`glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)`)
   reveals the two triangles sharing an edge.
4. The EBO is bound *while the VAO is bound*, so the VAO remembers it; unbinding the
   EBO before the VAO would break the drawing.
