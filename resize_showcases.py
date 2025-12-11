#!/usr/bin/env python3
"""
Resize and crop showcase images to exactly 1080x1080px for World App Developer Portal
"""
from PIL import Image
import os

INPUT_DIR = "showcases"
OUTPUT_DIR = "showcases/resized"
TARGET_SIZE = 1080

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Process each showcase
for i in range(1, 4):
    input_file = f"{INPUT_DIR}/showcase_{i}_{'initial' if i == 1 else 'revealed' if i == 2 else 'content'}.png"
    output_file = f"{OUTPUT_DIR}/showcase_{i}_1080x1080.png"
    
    print(f"Processing {input_file}...")
    
    # Open image
    img = Image.open(input_file)
    print(f"  Original size: {img.size}")
    
    # Calculate crop to center square
    width, height = img.size
    
    # We want to crop to a square, taking the smallest dimension
    min_dim = min(width, height)
    
    # Calculate crop box (center crop)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim
    
    # Crop to square
    img_square = img.crop((left, top, right, bottom))
    print(f"  Cropped to square: {img_square.size}")
    
    # Resize to exactly 1080x1080
    img_resized = img_square.resize((TARGET_SIZE, TARGET_SIZE), Image.Resampling.LANCZOS)
    print(f"  Resized to: {img_resized.size}")
    
    # Save
    img_resized.save(output_file, optimize=True, quality=95)
    print(f"  ✓ Saved: {output_file}\n")

print(f"\n✅ All showcases resized to {TARGET_SIZE}x{TARGET_SIZE}!")
print(f"📂 Output directory: {OUTPUT_DIR}/")
