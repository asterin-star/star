import Phaser from 'phaser';

/**
 * MenuScene - Main menu
 * Shows title and start game option
 */
export default class MenuScene extends Phaser.Scene {
    constructor() {
        super({ key: 'MenuScene' });
    }

    create() {
        const { width, height } = this.cameras.main;

        // Title
        this.add.text(
            width / 2,
            height / 3,
            'PIXEL RPG',
            {
                fontFamily: 'monospace',
                fontSize: '24px',
                color: '#ffffff',
                stroke: '#000000',
                strokeThickness: 4
            }
        ).setOrigin(0.5);

        // Subtitle
        this.add.text(
            width / 2,
            height / 3 + 30,
            'An Omori/Undertale Inspired Game',
            {
                fontFamily: 'monospace',
                fontSize: '8px',
                color: '#aaaaaa'
            }
        ).setOrigin(0.5);

        // Start button indicator
        const startText = this.add.text(
            width / 2,
            height / 2 + 40,
            'Press SPACE to Start',
            {
                fontFamily: 'monospace',
                fontSize: '12px',
                color: '#ffffff'
            }
        ).setOrigin(0.5);

        // Blinking animation for start text
        this.tweens.add({
            targets: startText,
            alpha: 0.3,
            duration: 800,
            yoyo: true,
            repeat: -1
        });

        // Controls text
        this.add.text(
            width / 2,
            height - 30,
            'Controls: Arrow Keys/WASD to move • SPACE to interact',
            {
                fontFamily: 'monospace',
                fontSize: '6px',
                color: '#666666'
            }
        ).setOrigin(0.5);

        // Input handling
        this.input.keyboard.once('keydown-SPACE', () => {
            this.scene.start('WorldScene');
        });
    }
}
