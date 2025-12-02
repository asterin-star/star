#!/usr/bin/env python3
"""Resize showcase images to 1080x1080px"""

from PIL import Image
import os

artifacts_dir = "/home/star/.gemini/antigravity/brain/2cbce920-f290-4470-893d-c56ad581e484"

# Images to resize
images = [
    ("showcase_final_1_es_1764717911553.png", "showcase_1_spanish.png"),
    ("showcase_final_2_en_1764717932779.png", "showcase_2_english.png"),
    ("showcase_final_3_pt_1764717953726.png", "showcase_3_portuguese.png")
]

for src_name, dst_name in images:
    src_path = os.path.join(artifacts_dir, src_name)
    dst_path = os.path.join(artifacts_dir, dst_name)
    
    if not os.path.exists(src_path):
        print(f"Skipping {src_name} - file not found")
        continue
    
    # Open image
    img = Image.open(src_path)
    print(f"Original size: {img.size}")
    
    # Calculate aspect ratio and crop to square
    width, height = img.size
    if width > height:
        # Landscape - crop width
        left = (width - height) // 2
        img = img.crop((left, 0, left + height, height))
    elif height > width:
        # Portrait - crop height
        top = (height - width) // 2
        img = img.crop((0, top, width, top + width))
    
    # Resize to 1080x1080
    img = img.resize((1080, 1080), Image.Resampling.LANCZOS)
    
    # Save with optimization
    img.save(dst_path, "PNG", optimize=True, quality=90)
    
    # Check file size
    file_size = os.path.getsize(dst_path) / 1024  # KB
    print(f"Saved {dst_name}: {img.size}, {file_size:.1f}KB")
    
    if file_size > 500:
        print(f"WARNING: {dst_name} is larger than 500KB!")

print("Done!")
