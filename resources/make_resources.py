"""Generate every texture and model the labs use.

The images are drawn procedurally (with numpy + Pillow), so the labs need no
downloads.  The files are already included in this folder - run this script
only if you deleted them or want to tweak them:

    python3 make_resources.py
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "textures")
MODEL = os.path.join(HERE, "models", "scene")
rng = np.random.default_rng(7)


def wood(size, base=(150, 100, 55)):
    """Wooden planks: horizontal grain + plank seams."""
    y = np.arange(size)[:, None]
    x = np.arange(size)[None, :]
    grain = 0.5 + 0.5 * np.sin(y * 0.35 + 3.0 * np.sin(x * 0.02 + y * 0.01))
    noise = rng.normal(0, 0.06, (size, size))
    shade = 0.75 + 0.2 * grain + noise
    plank = size // 4
    shade[(y % plank < 3).repeat(size, 1)] *= 0.45            # plank seams
    img = np.stack([base[0] * shade, base[1] * shade, base[2] * shade], axis=-1)
    return np.clip(img, 0, 255)


def make_container():
    """Classic crate: planks with a dark frame and a diagonal brace."""
    s = 512
    img = wood(s)
    frame = 40
    img[:frame], img[-frame:], img[:, :frame], img[:, -frame:] = (
        img[:frame] * 0.6, img[-frame:] * 0.6, img[:, :frame] * 0.6, img[:, -frame:] * 0.6)
    pil = Image.fromarray(img.astype(np.uint8))
    d = ImageDraw.Draw(pil)
    d.line([(frame, s - frame), (s - frame, frame)], fill=(95, 60, 30), width=34)
    d.rectangle([frame, frame, s - frame, s - frame], outline=(70, 45, 22), width=6)
    pil.save(os.path.join(TEX, "container.jpg"), quality=92)


def make_awesomeface():
    """A smiley face with a transparent background (RGBA)."""
    s = 512
    pil = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(pil)
    d.ellipse([40, 40, s - 40, s - 40], fill=(255, 205, 40, 255), outline=(60, 40, 0, 255), width=10)
    d.ellipse([160, 150, 220, 250], fill=(40, 25, 0, 255))     # left eye
    d.ellipse([292, 150, 352, 250], fill=(40, 25, 0, 255))     # right eye
    d.arc([130, 170, 382, 400], start=20, end=160, fill=(40, 25, 0, 255), width=18)
    pil.save(os.path.join(TEX, "awesomeface.png"))


def make_container2():
    """Wooden box with a steel border, plus its matching specular map."""
    s = 512
    img = wood(s, base=(170, 110, 50))
    border = 48
    mask = np.zeros((s, s), bool)
    mask[:border], mask[-border:], mask[:, :border], mask[:, -border:] = True, True, True, True
    steel = 120 + rng.normal(0, 12, (s, s))
    for c in range(3):
        img[..., c][mask] = steel[mask]
    pil = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(pil)
    for (cx, cy) in [(24, 24), (s - 24, 24), (24, s - 24), (s - 24, s - 24)]:
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(70, 70, 75))   # rivets
    pil.save(os.path.join(TEX, "container2.png"))

    # specular map: steel shines (bright), wood is matte (black)
    spec = np.zeros((s, s))
    spec[mask] = 180 + rng.normal(0, 25, (s, s))[mask]
    scratches = rng.random((s, s)) < 0.01
    spec[mask & scratches] = 60
    Image.fromarray(np.clip(spec, 0, 255).astype(np.uint8)).convert("RGB").save(
        os.path.join(TEX, "container2_specular.png"))


def make_torus_textures():
    """Diffuse + specular maps for the torus in the model."""
    s = 256
    u = np.linspace(0, 1, s)[None, :]
    v = np.linspace(0, 1, s)[:, None]
    stripes = (np.floor(u * 16) + np.floor(v * 4)) % 2
    diffuse = np.stack([40 + 160 * stripes, 90 + 60 * stripes + 0 * v, 200 - 60 * stripes],
                       axis=-1)
    Image.fromarray(np.clip(diffuse, 0, 255).astype(np.uint8)).save(
        os.path.join(MODEL, "torus_diffuse.png"))
    spec = np.repeat((255 * stripes)[..., None], 3, axis=-1)
    Image.fromarray(spec.astype(np.uint8)).save(os.path.join(MODEL, "torus_specular.png"))


def write_scene_model():
    """An OBJ with two objects and two materials: a torus on a crate."""
    v, vt, vn = [], [], []          # positions, texture coords, normals

    # ---- object 1: a torus floating above the crate -----------------------
    R, r, nu, nv = 1.0, 0.35, 48, 24
    first = len(v)
    for i in range(nu + 1):
        for j in range(nv + 1):
            a, b = 2 * math.pi * i / nu, 2 * math.pi * j / nv
            nx, ny, nz = math.cos(b) * math.cos(a), math.sin(b), math.cos(b) * math.sin(a)
            v.append((R * math.cos(a) + r * nx, 1.35 + r * ny, R * math.sin(a) + r * nz))
            vn.append((nx, ny, nz))
            vt.append((i / nu, j / nv))
    torus_faces = []
    for i in range(nu):
        for j in range(nv):
            a = first + i * (nv + 1) + j + 1          # OBJ indices start at 1
            b = a + nv + 1
            torus_faces.append((a, a + 1, b + 1, b))

    # ---- object 2: a crate (a cube with 4 vertices per face) ----------------
    h = 0.6
    sides = [((0, 0, 1), (1, 0, 0), (0, 1, 0)), ((0, 0, -1), (-1, 0, 0), (0, 1, 0)),
             ((1, 0, 0), (0, 0, -1), (0, 1, 0)), ((-1, 0, 0), (0, 0, 1), (0, 1, 0)),
             ((0, 1, 0), (1, 0, 0), (0, 0, -1)), ((0, -1, 0), (1, 0, 0), (0, 0, 1))]
    crate_faces = []
    for (n, tu, tv) in sides:
        face = []
        for (su, sv) in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
            v.append(tuple(h * (n[k] + su * tu[k] + sv * tv[k]) for k in range(3)))
            vn.append(n)
            vt.append(((su + 1) / 2, (sv + 1) / 2))
            face.append(len(v))
        crate_faces.append(tuple(face))

    lines = ["# generated by make_resources.py", "mtllib scene.mtl"]
    lines += [f"v {x:.5f} {y:.5f} {z:.5f}" for (x, y, z) in v]
    lines += [f"vt {s:.5f} {t:.5f}" for (s, t) in vt]
    lines += [f"vn {x:.5f} {y:.5f} {z:.5f}" for (x, y, z) in vn]
    lines += ["o Torus", "usemtl torus"]
    lines += ["f " + " ".join(f"{k}/{k}/{k}" for k in f) for f in torus_faces]
    lines += ["o Crate", "usemtl crate"]
    lines += ["f " + " ".join(f"{k}/{k}/{k}" for k in f) for f in crate_faces]
    with open(os.path.join(MODEL, "scene.obj"), "w") as f:
        f.write("\n".join(lines) + "\n")

    with open(os.path.join(MODEL, "scene.mtl"), "w") as f:
        f.write("newmtl torus\nKd 1 1 1\nKs 1 1 1\nNs 64\n"
                "map_Kd torus_diffuse.png\nmap_Ks torus_specular.png\n\n"
                "newmtl crate\nKd 1 1 1\nKs 1 1 1\nNs 32\n"
                "map_Kd ../../textures/container2.png\n"
                "map_Ks ../../textures/container2_specular.png\n")


if __name__ == "__main__":
    os.makedirs(TEX, exist_ok=True)
    os.makedirs(MODEL, exist_ok=True)
    make_container()
    make_awesomeface()
    make_container2()
    make_torus_textures()
    write_scene_model()
    print("textures and model written to", HERE)
