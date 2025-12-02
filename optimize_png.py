#!/usr/bin/env python3
"""Optimize PNG files by reducing quality"""

from PIL import Image
import os

artifacts_dir = "/home/star/.gemini/antigravity/brain/2cbce920-f290-4470-893d-c56ad581e484"

# Optimize the large English image
src_path = os.path.join(artifacts_dir, "showcase_2_english.png")
dst_path = os.path.join(artifacts_dir, "showcase_2_english_optimized.png")

if os.path.exists(src_path):
    img = Image.open(src_path)
    # Convert to RGB if needed (for JPEG-like optimization)
    if img.mode == 'RGBA':
        # Create white background
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
        img = background
    
    # Save with more compression
    img.save(dst_path, "PNG", optimize=True, compress_level=9)
    
    original_size = os.path.getsize(src_path) / 1024
    new_size = os.path.getsize(dst_path) / 1024
    print(f"Original: {original_size:.1f}KB → Optimized: {new_size:.1f}KB ({new_size/original_size*100:.1f}%)")
    
    # Replace original if smaller
    if new_size < original_size:
        os.replace(dst_path, src_path)
        print(f"Replaced original with optimized version")
    else:
        print("Optimization didn't reduce size, keeping original")
        os.remove(dst_path)
else:
    print(f"File not found: {src_path}")
