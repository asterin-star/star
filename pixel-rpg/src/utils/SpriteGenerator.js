import Phaser from 'phaser';

/**
 * Creates programmatic pixel art sprites with clean outlines
 */
export function createPlayerSprite(scene) {
    const g = scene.add.graphics();

    // Player character - style inspired by Omori/Undertale
    // Size: 16x20 pixels

    // Outline (black)
    g.fillStyle(0x000000, 1);
    g.fillRect(4, 0, 8, 2);   // Top of head
    g.fillRect(2, 2, 12, 14);  // Main body outline
    g.fillRect(4, 16, 8, 4);   // Legs

    // Skin tone
    g.fillStyle(0xffd4a3, 1);
    g.fillRect(5, 1, 6, 5);    // Face

    // Hair (dark)
    g.fillStyle(0x4a3930, 1);
    g.fillRect(5, 1, 6, 3);    // Hair top

    // Eyes (white)
    g.fillStyle(0xffffff, 1);
    g.fillRect(6, 4, 1, 1);
    g.fillRect(9, 4, 1, 1);

    // Pupils (black)
    g.fillStyle(0x000000, 1);
    g.fillPixel(6, 4);
    g.fillPixel(9, 4);

    // Shirt (blue)
    g.fillStyle(0x5599ff, 1);
    g.fillRect(3, 7, 10, 6);

    // Pants (dark blue)
    g.fillStyle(0x334466, 1);
    g.fillRect(3, 13, 10, 3);
    g.fillRect(5, 16, 2, 4);   // Left leg
    g.fillRect(9, 16, 2, 4);   // Right leg

    // Shoes (black)
    g.fillStyle(0x000000, 1);
    g.fillRect(4, 19, 3, 1);
    g.fillRect(9, 19, 3, 1);

    g.generateTexture('player_down', 16, 20);
    g.destroy();
}

export function createNPCSprite(scene, key, color) {
    const g = scene.add.graphics();

    // Simple NPC with outline
    // Outline
    g.fillStyle(0x000000, 1);
    g.fillRect(2, 0, 12, 2);
    g.fillRect(0, 2, 16, 14);
    g.fillRect(2, 16, 12, 4);

    // Body color
    g.fillStyle(color, 1);
    g.fillRect(1, 1, 14, 15);

    // Face (simple)
    g.fillStyle(0xffd4a3, 1);
    g.fillRect(4, 3, 8, 6);

    // Eyes
    g.fillStyle(0x000000, 1);
    g.fillRect(6, 5, 1, 2);
    g.fillRect(9, 5, 1, 2);

    g.generateTexture(key, 16, 20);
    g.destroy();
}
