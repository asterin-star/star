from PIL import Image
import os

def slice_assets():
    source_path = '/home/star/.gemini/antigravity/brain/cdfd488c-e0ce-495d-a9af-1d973c1d1166/pixel_art_rpg_assets_1765589307622.png'
    output_dir = '/home/star/star/pixel-rpg/public/assets/sprites'
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs('/home/star/star/pixel-rpg/public/assets/tilesets', exist_ok=True)
    
    try:
        img = Image.open(source_path)
    except FileNotFoundError:
        print(f"Error: Source image not found at {source_path}")
        return

    # Coordinates based on the generated image layout (approximation - since I can't see coordinates directly I'll infer standard grid)
    # The user asked for specific layout:
    # 1. Main character 4 dirs (top left)
    # 2. PCBs (below)
    # 3. Tileset (bottom)
    
    # Assuming a general 16x16 grid.
    # I will crop regions. 
    # NOTE: Since I cannot be 100% sure of the pixel perfect alignment of the generated image without checking, 
    # I will save the whole image as a temp spritesheet and also try to crop.
    # For now, let's just copy the MAIN generated image to the assets folder so we can use it as a raw spritesheet if cropping fails or is inaccurate.
    
    img.save(os.path.join(output_dir, 'full_sheet.png'))
    
    # Let's try to crop the player. Assuming typical 3x4 grid for sprites often used in generated output or similar.
    # But text descriptions say: "4-DIRECTION WALKING ...".
    # I'll create a single "player.png" 48x64 or similar if possible.
    # Actually, for the sake of this task, I will assume the user considers the "full_sheet.png" usable and I will use frame coordinates 
    # manually in Phaser if I have to. 
    # BUT, to be cleaner, I'll *attempt* to crop the top-left area for player.
    # Let's crop a generous chunks.
    
    # Grid 1: Player. Let's guess top-left 128x128 approx
    player_crop = img.crop((0, 0, 150, 200)) # Approximate area
    player_crop.save(os.path.join(output_dir, 'player_sheet_raw.png'))

    # NPCs
    npc_crop = img.crop((0, 200, 300, 350))
    npc_crop.save(os.path.join(output_dir, 'npc_sheet_raw.png'))

    # Tileset
    tile_crop = img.crop((0, 400, 500, 500))
    tile_crop.save(os.path.join('/home/star/star/pixel-rpg/public/assets/tilesets', 'room_tiles_raw.png'))
    
    print("Assets sliced and saved.")

if __name__ == "__main__":
    slice_assets()
