import Phaser from 'phaser';
import BootScene from './scenes/BootScene.js';
import MenuScene from './scenes/MenuScene.js';
import WorldScene from './scenes/WorldScene.js';

// Game configuration
const config = {
    type: Phaser.AUTO,
    width: 320,
    height: 240,
    parent: 'game-container',
    backgroundColor: '#000000',

    // Pixel-perfect settings
    pixelArt: true,
    antialias: false,
    roundPixels: true,

    // Scale configuration for responsive design
    scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH,
        width: 320,
        height: 240,
        zoom: 3  // Scale up 3x for better visibility
    },

    // Physics configuration
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 0 },  // Top-down view, no gravity
            debug: false  // Set to true for collision debugging
        }
    },

    // Scene list
    scene: [BootScene, MenuScene, WorldScene]
};

// Create the game instance
const game = new Phaser.Game(config);
