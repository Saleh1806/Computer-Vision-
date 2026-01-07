#!/usr/bin/env python3
"""
Simple, junior-friendly demo: pinhole camera vs lens camera.
We build a synthetic scene, then render:
  1) Pinhole: everything is sharp.
  2) Lens: focus on foreground, background is blurred (defocus).
We also draw a simple ray diagram to visualize the difference.
"""

import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter


OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")


def blur_image_rgb(img, sigma):
    """Gaussian blur using Pillow (fast and simple)."""
    if sigma <= 0.0:
        return img.copy()

    img_u8 = (np.clip(img, 0.0, 1.0) * 255.0).astype(np.uint8)
    pil = Image.fromarray(img_u8)
    blurred = pil.filter(ImageFilter.GaussianBlur(radius=sigma))
    return np.asarray(blurred).astype(np.float32) / 255.0


def make_scene(width=400, height=250):
    """Create a simple synthetic scene with a depth map."""
    img = np.zeros((height, width, 3), dtype=np.float32)
    depth = np.full((height, width), 5.0, dtype=np.float32)  # background depth

    # Background gradient sky
    for y in range(height):
        t = y / (height - 1)
        img[y, :, :] = [0.65 - 0.35 * t, 0.85 - 0.45 * t, 1.0]

    # Checkerboard ground
    ground_y = int(height * 0.55)
    tile = 40
    for y in range(ground_y, height):
        for x in range(width):
            if ((x // tile) + (y // tile)) % 2 == 0:
                img[y, x, :] = [0.75, 0.75, 0.75]
            else:
                img[y, x, :] = [0.55, 0.55, 0.55]
    depth[ground_y:, :] = 6.0

    # Sun (background)
    cy, cx, r = int(height * 0.2), int(width * 0.8), 50
    for y in range(max(0, cy - r), min(height, cy + r)):
        for x in range(max(0, cx - r), min(width, cx + r)):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r ** 2:
                img[y, x, :] = [1.0, 0.9, 0.4]
    depth[cy - r : cy + r, cx - r : cx + r] = 8.0

    # Foreground object (close)
    rect_top = int(height * 0.35)
    rect_bottom = int(height * 0.8)
    rect_left = int(width * 0.15)
    rect_right = int(width * 0.45)
    img[rect_top:rect_bottom, rect_left:rect_right, :] = [0.2, 0.4, 0.9]
    depth[rect_top:rect_bottom, rect_left:rect_right] = 1.2

    # Add a white circle on the foreground block
    cy2, cx2, r2 = int(height * 0.55), int(width * 0.3), 45
    for y in range(max(0, cy2 - r2), min(height, cy2 + r2)):
        for x in range(max(0, cx2 - r2), min(width, cx2 + r2)):
            if (x - cx2) ** 2 + (y - cy2) ** 2 <= r2 ** 2:
                img[y, x, :] = [0.97, 0.97, 0.97]
                depth[y, x] = 1.0

    # Text-like stripe on background
    stripe_y = int(height * 0.32)
    img[stripe_y:stripe_y + 10, int(width * 0.55):int(width * 0.95), :] = [0.1, 0.1, 0.1]
    depth[stripe_y:stripe_y + 10, int(width * 0.55):int(width * 0.95)] = 7.0

    return img, depth


def render_pinhole(img):
    """Pinhole camera: everything is sharp."""
    return img.copy()


def render_lens(img, depth, focus_depth=1.0):
    """Lens camera: defocus blur grows with distance from focus."""
    # Blur background and midground more than foreground.
    bg_blur = blur_image_rgb(img, sigma=6.0)
    mg_blur = blur_image_rgb(img, sigma=3.0)

    # Masks for simple depth layers
    fg_mask = depth <= (focus_depth + 0.5)
    mg_mask = (depth > (focus_depth + 0.5)) & (depth <= 4.0)
    bg_mask = depth > 4.0

    out = np.zeros_like(img)
    out[fg_mask] = img[fg_mask]
    out[mg_mask] = mg_blur[mg_mask]
    out[bg_mask] = bg_blur[bg_mask]
    return out


def draw_ray_diagram(path):
    """Draw a simple ray diagram using Pillow."""
    width, height = 1000, 400
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # Two panels
    panels = [(0, 0, width // 2, height), (width // 2, 0, width, height)]
    titles = ["Pinhole Camera", "Lens Camera (Focused)"]

    for (x0, y0, x1, y1), title in zip(panels, titles):
        draw.text((x0 + 10, y0 + 10), title, fill="black", font=font)

        # Map scene coords (0..10, 0..6) to pixels
        def to_px(x, y):
            px = x0 + int((x / 10.0) * (x1 - x0))
            py = y1 - int((y / 6.0) * (y1 - y0))
            return px, py

        # Object line
        draw.line([to_px(1, 1), to_px(1, 5)], fill="black", width=2)
        draw.text(to_px(0.6, 5.2), "Object", fill="black", font=font)

        # Image plane
        draw.line([to_px(8, 0.5), to_px(8, 5.5)], fill="black", width=2)
        draw.text(to_px(7.5, 5.7), "Image plane", fill="black", font=font)

        if "Pinhole" in title:
            # Pinhole dot
            px, py = to_px(5, 3)
            draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill="black")
            draw.text(to_px(4.5, 2.6), "Pinhole", fill="black", font=font)
            # Rays
            draw.line([to_px(1, 5), to_px(5, 3), to_px(8, 1)], fill="#1f77b4", width=2)
            draw.line([to_px(1, 1), to_px(5, 3), to_px(8, 5)], fill="#1f77b4", width=2)
        else:
            # Lens shape (simple ellipse)
            lx0, ly0 = to_px(4.8, 4.5)
            lx1, ly1 = to_px(5.2, 1.5)
            draw.ellipse([lx0, ly0, lx1, ly1], outline="black", width=2)
            draw.text(to_px(4.6, 4.7), "Lens", fill="black", font=font)
            # Rays converge
            draw.line([to_px(1, 5), to_px(5, 3.5), to_px(8, 3)], fill="#d62728", width=2)
            draw.line([to_px(1, 1), to_px(5, 2.5), to_px(8, 3)], fill="#d62728", width=2)

    img.save(path)


def save_image(path, img):
    """Save float image [0..1] to PNG using Pillow."""
    img_clipped = np.clip(img, 0.0, 1.0)
    img_u8 = (img_clipped * 255.0).astype(np.uint8)
    Image.fromarray(img_u8).save(path)


def load_photo(path, target_width=400):
    """Load a photo, composite on white if needed, and resize."""
    img = Image.open(path)
    if img.mode in ("RGBA", "LA"):
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(bg, img.convert("RGBA")).convert("RGB")
    else:
        img = img.convert("RGB")

    w, h = img.size
    scale = target_width / float(w)
    new_size = (target_width, int(h * scale))
    img = img.resize(new_size, Image.BICUBIC)
    arr = np.asarray(img).astype(np.float32) / 255.0
    return arr


def fake_depth_from_photo(img):
    """
    Simple depth guess: bottom is closer, top is farther.
    This keeps the demo easy to understand.
    """
    h, w, _ = img.shape
    y = np.linspace(0.0, 1.0, h).reshape(h, 1)
    depth = 1.0 + 6.0 * (1.0 - y)  # top ~7, bottom ~1
    depth = np.repeat(depth, w, axis=1).astype(np.float32)
    return depth


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    scene, depth = make_scene()
    pinhole = render_pinhole(scene)
    lens = render_lens(scene, depth, focus_depth=1.0)

    save_image(os.path.join(OUTPUT_DIR, "scene_pinhole.png"), pinhole)
    save_image(os.path.join(OUTPUT_DIR, "scene_lens.png"), lens)

    draw_ray_diagram(os.path.join(OUTPUT_DIR, "ray_diagram.png"))

    photo_path = os.path.join(ASSETS_DIR, "photo.jpg")
    if os.path.exists(photo_path):
        photo = load_photo(photo_path)
        photo_depth = fake_depth_from_photo(photo)
        photo_pinhole = render_pinhole(photo)
        photo_lens = render_lens(photo, photo_depth, focus_depth=1.5)
        save_image(os.path.join(OUTPUT_DIR, "photo_pinhole.png"), photo_pinhole)
        save_image(os.path.join(OUTPUT_DIR, "photo_lens.png"), photo_lens)

    print("Saved outputs to:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
