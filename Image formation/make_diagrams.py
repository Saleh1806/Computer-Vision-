#!/usr/bin/env python3
"""
Generate simple schematic images for the explanation file.
Uses only Pillow to keep dependencies light.
"""

import os
from PIL import Image, ImageDraw, ImageFont


BASE_DIR = os.path.dirname(__file__)
OUT_DIR = os.path.join(BASE_DIR, "diagrams")


def font():
    return ImageFont.load_default()


def draw_pinhole_projection(path):
    w, h = 900, 450
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    fnt = font()

    # Title
    d.text((20, 10), "Pinhole Projection", fill="black", font=fnt)

    # Object line (left)
    d.line([(120, 100), (120, 350)], fill="black", width=3)
    d.text((80, 80), "Object", fill="black", font=fnt)

    # Pinhole
    d.ellipse([(430, 215), (450, 235)], fill="black")
    d.text((395, 190), "Pinhole", fill="black", font=fnt)

    # Image plane (right)
    d.line([(760, 80), (760, 370)], fill="black", width=3)
    d.text((720, 50), "Image plane", fill="black", font=fnt)

    # Rays
    d.line([(120, 100), (440, 225), (760, 350)], fill="#1f77b4", width=2)
    d.line([(120, 350), (440, 225), (760, 100)], fill="#1f77b4", width=2)

    # Labels for image
    d.text((770, 330), "Inverted", fill="black", font=fnt)

    # Coordinate hints
    d.text((130, 355), "3D point (X, Y, Z)", fill="black", font=fnt)
    d.text((770, 100), "Image point (x, y)", fill="black", font=fnt)

    img.save(path)


def draw_thin_lens(path):
    w, h = 900, 450
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    fnt = font()

    d.text((20, 10), "Thin Lens Focusing", fill="black", font=fnt)

    # Object
    d.line([(120, 100), (120, 350)], fill="black", width=3)
    d.text((80, 80), "Object", fill="black", font=fnt)

    # Lens (vertical ellipse)
    d.ellipse([(430, 120), (470, 330)], outline="black", width=3)
    d.text((420, 90), "Lens", fill="black", font=fnt)

    # Sensor (image plane)
    d.line([(760, 80), (760, 370)], fill="black", width=3)
    d.text((700, 50), "Sensor", fill="black", font=fnt)

    # Rays converging to a point
    d.line([(120, 100), (450, 210), (760, 240)], fill="#d62728", width=2)
    d.line([(120, 350), (450, 240), (760, 240)], fill="#d62728", width=2)
    d.ellipse([(752, 232), (768, 248)], fill="#d62728")

    d.text((770, 230), "Focus point", fill="black", font=fnt)

    # Distances
    d.text((200, 370), "do (object distance)", fill="black", font=fnt)
    d.text((520, 370), "di (image distance)", fill="black", font=fnt)
    d.text((410, 350), "f (focal length)", fill="black", font=fnt)

    img.save(path)


def draw_defocus_blur(path):
    w, h = 900, 450
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    fnt = font()

    d.text((20, 10), "Defocus Blur (Circle of Confusion)", fill="black", font=fnt)

    # Lens
    d.ellipse([(300, 120), (340, 330)], outline="black", width=3)
    d.text((290, 90), "Lens", fill="black", font=fnt)

    # Sensor plane
    d.line([(650, 80), (650, 370)], fill="black", width=3)
    d.text((600, 50), "Sensor", fill="black", font=fnt)

    # Two image points: one in focus, one out of focus
    # In-focus rays (meet at a point on sensor)
    d.line([(80, 140), (320, 220), (650, 220)], fill="#1f77b4", width=2)
    d.line([(80, 300), (320, 220), (650, 220)], fill="#1f77b4", width=2)
    d.ellipse([(642, 212), (658, 228)], fill="#1f77b4")
    d.text((670, 210), "Sharp point", fill="black", font=fnt)

    # Out-of-focus rays (hit sensor as a blur circle)
    d.line([(80, 90), (320, 200), (650, 170)], fill="#ff7f0e", width=2)
    d.line([(80, 350), (320, 240), (650, 270)], fill="#ff7f0e", width=2)
    d.ellipse([(638, 165), (662, 275)], outline="#ff7f0e", width=3)
    d.text((670, 240), "Blur circle (c)", fill="black", font=fnt)
    d.text((20, 410), "c = circle of confusion", fill="black", font=fnt)
    d.text((300, 410), "A = aperture diameter", fill="black", font=fnt)

    img.save(path)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    draw_pinhole_projection(os.path.join(OUT_DIR, "pinhole_projection.png"))
    draw_thin_lens(os.path.join(OUT_DIR, "thin_lens.png"))
    draw_defocus_blur(os.path.join(OUT_DIR, "defocus_blur.png"))
    print("Saved diagrams to:", OUT_DIR)


if __name__ == "__main__":
    main()
