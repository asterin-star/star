import Phaser from 'phaser';
import { createPlayerSprite, createNPCSprite } from '../utils/SpriteGenerator.js';

/**
 * BootScene - Handles initial loading
 */
export default class BootScene extends Phaser.Scene {
    constructor() {
        super({ key: 'BootScene' });
    }

    preload() {
        const { width, height } = this.cameras.main;

        // Loading text
        const loadingText = this.add.text(width / 2, height / 2, 'Loading...', {
            fontFamily: 'monospace',
            fontSize: '16px',
            color: '#ffffff'
        }).setOrigin(0.5);

        // Progress bar
        const progressBar = this.add.graphics();
        const progressBox = this.add.graphics();
        progressBox.fillStyle(0x222222, 0.8);
        progressBox.fillRect(width / 2 - 160, height / 2 + 20, 320, 30);

        this.load.on('progress', (value) => {
            progressBar.clear();
            progressBar.fillStyle(0xffffff, 1);
            progressBar.fillRect(width / 2 - 150, height / 2 + 25, 300 * value, 20);
        });

        this.load.on('complete', () => {
            progressBar.destroy();
            progressBox.destroy();
            loadingText.destroy();
        });

        // Generate sprites programmatically instead of loading images
        // This ensures they always work
        createPlayerSprite(this);
        createNPCSprite(this, 'npc_villager', 0xe67e22);  // Orange villager
        createNPCSprite(this, 'npc_mysterious', 0x9b59b6); // Purple mysterious figure

        // Create simple tile textures
        const tileGraphics = this.add.graphics();

        // Floor tile
        tileGraphics.fillStyle(0x2d5016, 1);
        tileGraphics.fillRect(0, 0, 16, 16);
        tileGraphics.fillStyle(0x1a3010, 0.3);
        tileGraphics.fillRect(0, 0, 16, 1);
        tileGraphics.fillRect(0, 0, 1, 16);
        tileGraphics.generateTexture('tile_floor', 16, 16);
        tileGraphics.clear();

        // Wall tile
        tileGraphics.fillStyle(0x000000, 1);
        tileGraphics.fillRect(0, 0, 16, 16);
        tileGraphics.fillStyle(0x4a4a4a, 1);
        tileGraphics.fillRect(1, 1, 14, 14);
        tileGraphics.fillStyle(0x2a2a2a, 1);
        tileGraphics.fillRect(2, 2, 12, 12);
        tileGraphics.generateTexture('tile_wall', 16, 16);
        tileGraphics.clear();

        tileGraphics.destroy();

        console.log('BootScene: Assets generated programmatically');
    }

    create() {
        this.scene.start('MenuScene');
    }
}
