#!/usr/bin/env python3
"""
Compress showcase_2 to under 500KB while maintaining 1080x1080px dimensions
"""
from PIL import Image
import os

INPUT_FILE = "showcases/resized/showcase_2_1080x1080.png"
OUTPUT_FILE = "showcases/resized/showcase_2_1080x1080_compressed.png"
TARGET_SIZE_KB = 500

print(f"Compressing {INPUT_FILE}...")

# Open image
img = Image.open(INPUT_FILE)
print(f"Original size: {img.size}")
print(f"Original file size: {os.path.getsize(INPUT_FILE) / 1024:.1f} KB")

# Convert RGBA to RGB if needed (smaller file size)
if img.mode == 'RGBA':
    # Create white background
    background = Image.new('RGB', img.size, (255, 255, 255))
    background.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
    img = background

# Try different compression levels
quality_levels = [85, 75, 65, 55, 45]

for quality in quality_levels:
    # Save with compression
    img.save(OUTPUT_FILE, 'PNG', optimize=True, quality=quality)
    
    # Check file size
    file_size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    print(f"Quality {quality}: {file_size_kb:.1f} KB")
    
    if file_size_kb < TARGET_SIZE_KB:
        print(f"\n✅ Success! Compressed to {file_size_kb:.1f} KB")
        print(f"📂 Output: {OUTPUT_FILE}")
        
        # Replace original
        os.replace(OUTPUT_FILE, INPUT_FILE)
        print(f"✅ Replaced original file")
        break
else:
    print(f"\n⚠️ Could not compress below {TARGET_SIZE_KB}KB, using best result")
    os.replace(OUTPUT_FILE, INPUT_FILE)

print(f"\n✅ Final size: {os.path.getsize(INPUT_FILE) / 1024:.1f} KB")
