"""Lab 06 - Vectors and matrices with GLM (console only, no window).

learnopengl uses the C++ maths library GLM.  In Python we use PyGLM, which
has the same names:   pip install PyGLM

Run this file and compare each printed result with the maths in the
README - every block is one idea from the "Transformations" chapter.

Run:  python3 glm_basics.py
"""
import glm

print("=== VECTORS ===")
a = glm.vec3(1.0, 2.0, 2.0)
b = glm.vec3(0.0, 1.0, 0.0)
print("a            =", a)
print("length of a  =", glm.length(a))                  # sqrt(1+4+4) = 3
print("normalize(a) =", glm.normalize(a))               # unit vector, length 1
print("a + b        =", a + b)
print("a * 2        =", a * 2.0)                        # scalar multiplication
print("dot(a, b)    =", glm.dot(a, b))                  # = |a||b| cos(angle)
print("cross(x, y)  =", glm.cross(glm.vec3(1, 0, 0), glm.vec3(0, 1, 0)))   # = z

print("\n=== TRANSLATION: move the point (1,0,0) by (1,1,0) ===")
vec = glm.vec4(1.0, 0.0, 0.0, 1.0)          # w = 1 -> a POSITION (can be moved)
trans = glm.mat4(1.0)                        # start from the identity matrix
trans = glm.translate(trans, glm.vec3(1.0, 1.0, 0.0))
print("matrix:\n", trans)
print("result:", trans * vec)               # expected (2, 1, 0, 1)

print("\n=== w = 0 means a DIRECTION: translation does not affect it ===")
direction = glm.vec4(1.0, 0.0, 0.0, 0.0)
print("result:", trans * direction)          # still (1, 0, 0, 0)

print("\n=== ROTATION: 90 degrees around the z axis ===")
rot = glm.rotate(glm.mat4(1.0), glm.radians(90.0), glm.vec3(0.0, 0.0, 1.0))
print("(1,0,0) ->", rot * glm.vec4(1, 0, 0, 1))      # becomes (0, 1, 0)

print("\n=== SCALING: half size ===")
scale = glm.scale(glm.mat4(1.0), glm.vec3(0.5, 0.5, 0.5))
print("(2,4,6) ->", scale * glm.vec4(2, 4, 6, 1))     # becomes (1, 2, 3)

print("\n=== COMBINING: the order matters! ===")
# Matrices are applied RIGHT TO LEFT:  T * R * p  rotates p first, then moves it.
T = glm.translate(glm.mat4(1.0), glm.vec3(1.0, 0.0, 0.0))
R = glm.rotate(glm.mat4(1.0), glm.radians(90.0), glm.vec3(0.0, 0.0, 1.0))
p = glm.vec4(1, 0, 0, 1)
print("T * R * p  (rotate, then move) =", T * R * p)   # (1, 1, 0)
print("R * T * p  (move, then rotate) =", R * T * p)   # (0, 2, 0)
