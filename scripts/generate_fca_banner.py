#!/usr/bin/env python3
"""
Generate a seamless 4-color Firefly Cellular Automata (FCA) banner for the website
as an animated GIF showing the synchronization process.

Key design:
  - Stride = 4: samples every 4 iterations so that synchronized regions maintain their
    color phase (0 -> 1 -> 2 -> 3 -> 0) and only continuous spatial movement (wavefronts,
    domain coarsening, defect annihilation) is shown without high-frequency color flashing.
  - Slower frame rate: 200ms per frame (5 fps) for calm, non-distracting animation.
  - Synchronization progression: records 150 frames (600 simulation steps) starting
    from the initial state to clearly display the self-organizing synchronization behavior.
  - End pause: holds the final synchronized state for 15 frames (3s) before looping.
  - Exact 4-color palette matching the website design.
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
    parser = argparse.ArgumentParser(description="Generate 4-color FCA synchronization banner")
    parser.add_argument("--frames", type=int, default=150, help="Number of sampled frames (default: 150)")
    parser.add_argument("--stride", type=int, default=4, help="FCA steps per frame (default: 4)")
    parser.add_argument("--duration", type=int, default=200, help="Duration per frame in ms (default: 200)")
    parser.add_argument("--hold", type=int, default=15, help="Frames to hold final synchronized state (default: 15)")
    parser.add_argument("--height", type=int, default=60, help="Grid height (default: 60)")
    parser.add_argument("--width", type=int, default=2400, help="Grid width (default: 2400)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    args = parser.parse_args()

    output_dir = os.path.join(os.path.dirname(__file__), "..", "images", "banner")
    gif_path = os.path.join(output_dir, "fca_banner.gif")
    png_path = os.path.join(output_dir, "fca_banner.png")

    total_steps = args.frames * args.stride
    print(f"Simulating 4-color FCA: {args.height} x {args.width}, {total_steps} steps total, stride {args.stride}...")
    np.random.seed(args.seed)
    x = np.random.randint(0, 4, size=(args.height, args.width), dtype=np.int8)

    frames = []
    for f in range(args.frames):
        im = Image.fromarray(x.astype(np.uint8))
        im.putpalette(PALETTE_GIF)
        frames.append(im)
        for _ in range(args.stride):
            x = fca_step(x)

    # Final state stats
    props = [np.mean(x == c) for c in range(4)]
    print(f"Final state color proportions: 0={props[0]:.3f}, 1={props[1]:.3f}, 2={props[2]:.3f}, 3={props[3]:.3f}")

    # Save static fallback PNG of final synchronized state
    rgb = PALETTE_RGB[x]
    im_static = Image.fromarray(rgb)
    im_static.save(png_path, optimize=True)
    print(f"Saved static PNG fallback to {png_path} ({os.path.getsize(png_path) / 1024:.1f} KB)")

    # Append hold frames at the end
    all_frames = frames + [frames[-1]] * args.hold

    # Save animated GIF
    print(f"Saving animated GIF ({len(all_frames)} frames @ {args.duration}ms, total {len(all_frames)*args.duration/1000:.1f}s)...")
    all_frames[0].save(
        gif_path,
        save_all=True,
        append_images=all_frames[1:],
        duration=args.duration,
        loop=0,
        disposal=2,
        optimize=True,
    )
    print(f"Saved animated GIF to {gif_path} ({os.path.getsize(gif_path) / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
