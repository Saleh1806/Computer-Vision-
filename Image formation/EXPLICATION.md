# Pinhole vs Lens Camera (short explanation)

This folder compares two image formation models:
- **Pinhole camera**: a tiny hole, no optics. Everything is sharp, but very little light reaches the sensor.
- **Lens camera**: optics focus light. Brighter images and better quality, but sharpness is limited by focus (depth of field).

## What the images highlight
- **Pinhole**: the whole scene is sharp (in theory), but it would be dark in practice.
- **Lens**: only one plane is sharp; objects closer or farther are blurred (defocus).
- The ray diagram shows why: the pinhole forces a single ray per point, while a lens focuses rays only on the focal plane.

## Current embedded vision market
In embedded vision (robotics, automotive, drones, smartphones, industrial cameras),
we almost always use **lens-based cameras**. Main reasons:
- **More light**: larger aperture -> better low-light performance.
- **Higher resolution**: pinhole is limited by diffraction and noise.
- **Flexibility**: focal length, aperture, distortion control, and focus.

The **pinhole model** is still the standard **mathematical projection model** even for lens cameras.
So in practice: **hardware = lens**, **model = pinhole + distortion**.

## Useful formulas (comparison)

### 1) Pinhole projection (ideal model)
For a 3D point (X, Y, Z) in the camera frame:

x = f * X / Z  
y = f * Y / Z

In pixels using intrinsics:

u = fx * X / Z + cx  
v = fy * Y / Z + cy

Intrinsic matrix:

K = [ fx  0  cx
      0  fy  cy
      0   0   1 ]

### 2) Thin lens equation

1/f = 1/do + 1/di

f : focal length  
do: object distance  
di: image distance (sensor side)

### 3) Circle of confusion (defocus blur)
If a point is not on the focal plane, it becomes a blur disk:

approx: c ≈ A * |di - di0| / di

Using f-number:

N = f / A  
A = f / N

Smaller N (larger aperture) -> stronger blur.

### 4) Depth of field (simple idea)
Depth of field depends on:
- aperture (N)
- focus distance
- focal length (f)
- acceptable blur size (c)

Simple conclusion:
- small aperture (large N) -> more depth of field
- large aperture (small N) -> stronger blur

## In summary
- **Pinhole**: simple, everything sharp, but dark and impractical.
- **Lens**: bright and higher quality, but blur outside the focal plane.
- **Embedded vision**: almost always lens hardware with a pinhole model.
