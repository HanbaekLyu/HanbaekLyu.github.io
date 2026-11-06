#!/usr/bin/env python3
"""
Generate a high-resolution, seamless 4-color Firefly Cellular Automata (FCA) banner
for the website.

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
import numpy as np
from PIL import Image

PALETTE = np.array([
    [48, 48, 48],    # 0: Charcoal (#303030)
    [255, 128, 0],   # 1: Orange (#ff8000)
    [255, 255, 255], # 2: White (#ffffff)
    [0, 128, 255],   # 3: Blue (#0080ff)
], dtype=np.uint8)


def simulate_4color_fca(height: int = 180, width: int = 11520, steps: int = 600, seed: int = 42) -> np.ndarray:
    """Run 4-color FCA on a 2D grid with periodic boundary conditions."""
    np.random.seed(seed)
    x = np.random.randint(0, 4, size=(height, width), dtype=np.int8)
    b = np.int8(1)

    for _ in range(steps):
        left = np.roll(x, -1, axis=1)
        right = np.roll(x, 1, axis=1)
        up = np.roll(x, -1, axis=0)
        down = np.roll(x, 1, axis=0)
        stay = (x > b) & ((left == b) | (right == b) | (up == b) | (down == b))
        x = np.where(stay, x, (x + 1) % 4)

    return x


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate 4-color FCA banner")
    parser.add_argument("--steps", type=int, default=600, help="Simulation steps (default: 600)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    parser.add_argument("--height", type=int, default=180, help="Grid height (default: 180)")
    parser.add_argument("--width", type=int, default=11520, help="Grid width (default: 11520)")
    args = parser.parse_args()

    output_dir = os.path.join(os.path.dirname(__file__), "..", "images", "banner")
    output_path = os.path.join(output_dir, "fca_banner.png")

    print(f"Simulating 4-color FCA ({args.height} x {args.width}, {args.steps} steps, seed {args.seed})...")
    grid = simulate_4color_fca(height=args.height, width=args.width, steps=args.steps, seed=args.seed)

    # Color distribution check
    props = [np.mean(grid == c) for c in range(4)]
    print(f"Color proportions: 0={props[0]:.3f}, 1={props[1]:.3f}, 2={props[2]:.3f}, 3={props[3]:.3f}")

    # Verify horizontal seam continuity
    left_col = grid[:, 0]
    right_col = grid[:, -1]
    seam_diff = np.mean(left_col != right_col)
    interior_diff = np.mean(grid[:, :-1] != grid[:, 1:])
    print(f"Horizontal seam transition rate: {seam_diff:.3f} (interior average: {interior_diff:.3f})")

    # Render RGB image
    rgb = PALETTE[grid]
    im = Image.fromarray(rgb)
    im.save(output_path, optimize=True)
    print(f"Saved banner to {output_path} ({os.path.getsize(output_path) / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
