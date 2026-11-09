#!/usr/bin/env python3
"""
Generate a high-resolution, seamless 4-color Firefly Cellular Automata (FCA) banner
for the website as an animated GIF (and static PNG fallback).

Model: 4-color FCA on Z^2 (von Neumann neighborhood, periodic horizontal boundary).
State space: Z_4 = {0, 1, 2, 3}.
Blinking state: b = 1.
Inhibited states: {2, 3} (states > b).
Update rule:
  - If x in {2, 3} and any neighbor is in state 1: stay x (inhibited).
  - Otherwise: x -> (x + 1) mod 4.

Color scheme:
  - 0: #303030 (Charcoal gray)
  - 1: #ff8000 (Vibrant orange)
  - 2: #ffffff (Pure white)
  - 3: #0080ff (Azure blue)

Periodic horizontal boundaries ensure that the banner tiles seamlessly across any
viewport width with zero discontinuity.
"""

import os
import argparse
import numpy as np
from PIL import Image

PALETTE_RGB = np.array([
    [48, 48, 48],    # 0: Charcoal (#303030)
    [255, 128, 0],   # 1: Orange (#ff8000)
    [255, 255, 255], # 2: White (#ffffff)
    [0, 128, 255],   # 3: Blue (#0080ff)
], dtype=np.uint8)

PALETTE_GIF = [
    48, 48, 48,      # 0
    255, 128, 0,     # 1
    255, 255, 255,   # 2
    0, 128, 255,     # 3
] + [0] * (768 - 12)


def fca_step(x: np.ndarray) -> np.ndarray:
    """Perform a single step of 4-color FCA on a 2D grid with periodic boundaries."""
    b = np.int8(1)
    left = np.roll(x, -1, axis=1)
    right = np.roll(x, 1, axis=1)
    up = np.roll(x, -1, axis=0)
    down = np.roll(x, 1, axis=0)
    stay = (x > b) & ((left == b) | (right == b) | (up == b) | (down == b))
    return np.where(stay, x, (x + 1) % 4)


def main():
    parser = argparse.ArgumentParser(description="Generate 4-color FCA banner (GIF & PNG)")
    parser.add_argument("--burnin", type=int, default=600, help="Burn-in steps before recording (default: 600)")
    parser.add_argument("--frames", type=int, default=48, help="Number of animation frames (default: 48)")
    parser.add_argument("--duration", type=int, default=120, help="Duration per frame in ms (default: 120)")
    parser.add_argument("--height", type=int, default=90, help="Grid height (default: 90)")
    parser.add_argument("--width", type=int, default=2700, help="Grid width (default: 2700)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    args = parser.parse_args()

    output_dir = os.path.join(os.path.dirname(__file__), "..", "images", "banner")
    gif_path = os.path.join(output_dir, "fca_banner.gif")
    png_path = os.path.join(output_dir, "fca_banner.png")

    print(f"Simulating 4-color FCA ({args.height} x {args.width}, seed {args.seed})...")
    np.random.seed(args.seed)
    x = np.random.randint(0, 4, size=(args.height, args.width), dtype=np.int8)

    print(f"Running burn-in of {args.burnin} steps to form cluster regions...")
    for _ in range(args.burnin):
        x = fca_step(x)

    props = [np.mean(x == c) for c in range(4)]
    print(f"Color proportions: 0={props[0]:.3f}, 1={props[1]:.3f}, 2={props[2]:.3f}, 3={props[3]:.3f}")

    seam_diff = np.mean(x[:, 0] != x[:, -1])
    interior_diff = np.mean(x[:, :-1] != x[:, 1:])
    print(f"Horizontal seam transition rate: {seam_diff:.3f} (interior average: {interior_diff:.3f})")

    # Save static PNG fallback (frame 0)
    rgb = PALETTE_RGB[x]
    im_static = Image.fromarray(rgb)
    im_static.save(png_path, optimize=True)
    print(f"Saved static PNG to {png_path} ({os.path.getsize(png_path) / 1024:.1f} KB)")

    # Record animation frames
    print(f"Recording {args.frames} animation frames ({args.duration}ms each)...")
    frames = []
    for _ in range(args.frames):
        im = Image.fromarray(x.astype(np.uint8))
        im.putpalette(PALETTE_GIF)
        frames.append(im)
        x = fca_step(x)

    # Save animated GIF
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=args.duration,
        loop=0,
        optimize=True,
    )
    print(f"Saved animated GIF to {gif_path} ({os.path.getsize(gif_path) / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
