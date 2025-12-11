#!/usr/bin/env python3
"""
Compress showcase_2 to under 500KB by converting to JPEG
"""
from PIL import Image
import os

INPUT_FILE = "showcases/resized/showcase_2_1080x1080.png"
OUTPUT_FILE = "showcases/resized/showcase_2_1080x1080.jpg"
TARGET_SIZE_KB = 490  # Slightly under 500KB for safety

print(f"Compressing {INPUT_FILE} to JPEG...")

# Open image
img = Image.open(INPUT_FILE)
print(f"Original size: {img.size}")
print(f"Original file size: {os.path.getsize(INPUT_FILE) / 1024:.1f} KB")

# Convert RGBA to RGB (JPEG doesn't support transparency)
if img.mode in ('RGBA', 'LA', 'P'):
    # Create white background
    background = Image.new('RGB', img.size, (0, 0, 0))  # Black background for dark design
    if img.mode == 'P':
        img = img.convert('RGBA')
    background.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
    img = background
elif img.mode != 'RGB':
    img = img.convert('RGB')

# Try different JPEG quality levels
quality_levels = [95, 90, 85, 80, 75, 70, 65]

for quality in quality_levels:
    # Save as JPEG with compression
    img.save(OUTPUT_FILE, 'JPEG', optimize=True, quality=quality)
    
    # Check file size
    file_size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    print(f"JPEG Quality {quality}: {file_size_kb:.1f} KB")
    
    if file_size_kb < TARGET_SIZE_KB:
        print(f"\n✅ Success! Compressed to {file_size_kb:.1f} KB")
        print(f"📂 Output: {OUTPUT_FILE}")
        break
else:
    print(f"\n⚠️ Using best available compression")

final_size = os.path.getsize(OUTPUT_FILE) / 1024
print(f"\n✅ Final file: {OUTPUT_FILE}")
print(f"✅ Final size: {final_size:.1f} KB")
print(f"✅ Dimensions: {img.size} (maintained)")
