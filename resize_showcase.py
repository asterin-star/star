#!/usr/bin/env python3
"""Resize showcase images to 1080x1080px"""

from PIL import Image
import os

artifacts_dir = "/home/star/.gemini/antigravity/brain/dd4f5049-ade2-44a5-9b29-05c7cdfb6e54"

# Images to resize - All 24 images (3 per language × 8 languages)
images = [
    # Spanish (ES)
    ("screenshot_1_initial_1765248026857.png", "showcase_es_1_initial.png"),
    ("screenshot_2_revealed_1765248039308.png", "showcase_es_2_revealed.png"),
    ("screenshot_3_content_1765248050231.png", "showcase_es_3_content.png"),
    # English (EN)
    ("en_showcase_1_1765251667084.png", "showcase_en_1_initial.png"),
    ("en_showcase_2_1765251690354.png", "showcase_en_2_revealed.png"),
    ("en_showcase_3_1765251723334.png", "showcase_en_3_content.png"),
    # Portuguese (PT)
    ("pt_showcase_1_1765251762471.png", "showcase_pt_1_initial.png"),
    ("pt_showcase_2_1765252583295.png", "showcase_pt_2_revealed.png"),
    ("pt_showcase_3_1765252634918.png", "showcase_pt_3_content.png"),
    # French (FR)
    ("fr_showcase_1_1765252694997.png", "showcase_fr_1_initial.png"),
    ("fr_showcase_2_1765252761758.png", "showcase_fr_2_revealed.png"),
    ("fr_showcase_3_1765252868780.png", "showcase_fr_3_content.png"),
    # German (DE)
    ("de_showcase_1_1765252882812.png", "showcase_de_1_initial.png"),
    ("de_showcase_2_1765252895230.png", "showcase_de_2_revealed.png"),
    ("de_showcase_3_1765252910796.png", "showcase_de_3_content.png"),
    # Japanese (JA)
    ("ja_showcase_1_1765252926187.png", "showcase_ja_1_initial.png"),
    ("ja_showcase_2_1765252939173.png", "showcase_ja_2_revealed.png"),
    ("ja_showcase_3_1765252953339.png", "showcase_ja_3_content.png"),
    # Korean (KO)
    ("ko_showcase_1_1765252967135.png", "showcase_ko_1_initial.png"),
    ("ko_showcase_2_1765252979614.png", "showcase_ko_2_revealed.png"),
    ("ko_showcase_3_1765252993066.png", "showcase_ko_3_content.png"),
    # Chinese (ZH)
    ("zh_showcase_1_1765253005965.png", "showcase_zh_1_initial.png"),
    ("zh_showcase_2_1765253017521.png", "showcase_zh_2_revealed.png"),
    ("zh_showcase_3_1765253029395.png", "showcase_zh_3_content.png")
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
