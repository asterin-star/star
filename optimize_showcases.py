#!/usr/bin/env python3
"""
Optimize all showcase images to 1080x1080px and under 500KB
"""
from PIL import Image
import os
import glob

SHOWCASES_DIR = "/home/star/star/showcases"
TARGET_SIZE = (1080, 1080)
MAX_SIZE_KB = 500

def get_file_size_kb(filepath):
    """Get file size in KB"""
    return os.path.getsize(filepath) / 1024

def resize_and_crop_to_square(img, target_size=1080):
    """Resize image to square dimensions"""
    width, height = img.size
    
    # First, crop to square
    if width > height:
        # Landscape - crop width
        left = (width - height) // 2
        img = img.crop((left, 0, left + height, height))
    elif height > width:
        # Portrait - crop height
        top = (height - width) // 2
        img = img.crop((0, top, width, top + width))
    
    # Then resize to target size
    if img.size != (target_size, target_size):
        img = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
    
    return img

def compress_to_target_size(img, output_path, max_kb=500):
    """Compress image to be under target file size"""
    
    # Convert RGBA to RGB if needed (for better compression)
    if img.mode == 'RGBA':
        # Create white background
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Try PNG first with optimization
    img.save(output_path, 'PNG', optimize=True)
    size_kb = get_file_size_kb(output_path)
    
    if size_kb <= max_kb:
        return size_kb, 'PNG'
    
    # If PNG is too large, convert to JPEG with progressive quality reduction
    quality_levels = [95, 90, 85, 80, 75, 70, 65, 60, 55, 50]
    
    for quality in quality_levels:
        # Change extension to .jpg
        jpg_path = output_path.rsplit('.', 1)[0] + '.jpg'
        img.save(jpg_path, 'JPEG', quality=quality, optimize=True)
        size_kb = get_file_size_kb(jpg_path)
        
        if size_kb <= max_kb:
            # Remove the PNG file and use JPG
            if os.path.exists(output_path) and output_path != jpg_path:
                os.remove(output_path)
            # Rename back to original name with .jpg extension
            final_path = output_path.rsplit('.', 1)[0] + '.jpg'
            if jpg_path != final_path:
                os.rename(jpg_path, final_path)
            return size_kb, f'JPEG (Q{quality})'
    
    # If still too large, keep the best result
    return size_kb, f'JPEG (Q{quality_levels[-1]})'

def process_showcase_images():
    """Process all showcase images in the directory"""
    
    # Find all PNG files in showcases directory (excluding subdirectories)
    pattern = os.path.join(SHOWCASES_DIR, "showcase_*.png")
    image_files = glob.glob(pattern)
    
    print(f"Found {len(image_files)} showcase images to process\n")
    print("=" * 80)
    
    results = []
    
    for img_path in sorted(image_files):
        filename = os.path.basename(img_path)
        print(f"\n📷 Processing: {filename}")
        
        try:
            # Get original size
            original_size_kb = get_file_size_kb(img_path)
            
            # Open image
            img = Image.open(img_path)
            original_dimensions = img.size
            
            print(f"   Original: {original_dimensions[0]}x{original_dimensions[1]}, {original_size_kb:.1f} KB")
            
            # Resize and crop to square
            img = resize_and_crop_to_square(img, TARGET_SIZE[0])
            
            # Create temporary output path
            temp_path = img_path + ".temp"
            
            # Compress to target size
            final_size_kb, format_info = compress_to_target_size(img, temp_path, MAX_SIZE_KB)
            
            # Determine the actual saved file (might be .jpg instead of .png)
            if os.path.exists(temp_path):
                actual_temp = temp_path
            else:
                actual_temp = temp_path.rsplit('.', 1)[0] + '.jpg'
            
            # Replace original file
            # If it's a JPG, we need to rename the original PNG to JPG
            if actual_temp.endswith('.jpg'):
                new_path = img_path.rsplit('.', 1)[0] + '.jpg'
                if os.path.exists(img_path):
                    os.remove(img_path)  # Remove original PNG
                os.rename(actual_temp, new_path)
                final_path = new_path
            else:
                os.replace(actual_temp, img_path)
                final_path = img_path
            
            status = "✅" if final_size_kb <= MAX_SIZE_KB else "⚠️"
            print(f"   {status} Final: {TARGET_SIZE[0]}x{TARGET_SIZE[1]}, {final_size_kb:.1f} KB ({format_info})")
            
            results.append({
                'filename': filename,
                'original_size': original_size_kb,
                'final_size': final_size_kb,
                'format': format_info,
                'within_target': final_size_kb <= MAX_SIZE_KB
            })
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            results.append({
                'filename': filename,
                'error': str(e)
            })
    
    # Print summary
    print("\n" + "=" * 80)
    print("\n📊 SUMMARY")
    print("=" * 80)
    
    successful = [r for r in results if 'error' not in r]
    errors = [r for r in results if 'error' in r]
    within_target = [r for r in successful if r['within_target']]
    over_target = [r for r in successful if not r['within_target']]
    
    print(f"\nTotal images processed: {len(results)}")
    print(f"✅ Successfully optimized: {len(successful)}")
    print(f"   └─ Within 500KB target: {len(within_target)}")
    print(f"   └─ Over 500KB (best effort): {len(over_target)}")
    print(f"❌ Errors: {len(errors)}")
    
    if over_target:
        print("\n⚠️  Images over 500KB:")
        for r in over_target:
            print(f"   • {r['filename']}: {r['final_size']:.1f} KB")
    
    if errors:
        print("\n❌ Errors:")
        for r in errors:
            print(f"   • {r['filename']}: {r['error']}")
    
    print("\n" + "=" * 80)
    print("✅ Done!")

if __name__ == "__main__":
    process_showcase_images()
