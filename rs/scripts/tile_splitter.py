#!/usr/bin/env python3

import argparse
import os

try:
    from PIL import Image
except ImportError:
    print("Error: PIL (Pillow) is required. Install it with: pip install Pillow")
    exit(1)


def split_image(image_path, chunk_width, chunk_height):
    # Open the image
    img = Image.open(image_path)
    img_width, img_height = img.size

    # Calculate number of chunks
    num_chunks_x = img_width // chunk_width
    num_chunks_y = img_height // chunk_height

    # Base name for output files
    base_name = os.path.splitext(os.path.basename(image_path))[0]

    # Split and save chunks
    for y in range(num_chunks_y):
        for x in range(num_chunks_x):
            left = x * chunk_width
            upper = y * chunk_height
            right = left + chunk_width
            lower = upper + chunk_height

            # Crop the chunk
            chunk = img.crop((left, upper, right, lower))

            # Save the chunk
            chunk_filename = f"{base_name}_chunk_{x}_{y}.png"
            chunk.save(os.path.join(
                os.path.dirname(image_path), chunk_filename))
            print(f"Saved: {chunk_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split an image into chunks.")
    parser.add_argument("image_path", help="Path to the input image file.")
    parser.add_argument("-W", "--width", type=int,
                        required=True, help="Width of each chunk.")
    parser.add_argument("-H", "--height", type=int,
                        required=True, help="Height of each chunk.")

    args = parser.parse_args()

    split_image(args.image_path, args.width, args.height)
