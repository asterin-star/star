import Phaser from 'phaser';

export default class Interactable extends Phaser.GameObjects.Sprite {
    constructor(scene, x, y, texture, frame, message, dialogueSystem) {
        super(scene, x, y, texture, frame);
        this.scene = scene;
        this.message = message;
        this.dialogueSystem = dialogueSystem;

        scene.add.existing(this);
        scene.physics.add.existing(this, true); // true for static body

        this.body.setSize(16, 16);
        this.setDepth(5);

        // Interaction indicator
        this.indicator = scene.add.text(x, y - 12, '?', {
            fontFamily: 'monospace',
            fontSize: '10px',
            color: '#00ffff',
            stroke: '#000000',
            strokeThickness: 2
        }).setOrigin(0.5);
        this.indicator.setDepth(6);
        this.indicator.setVisible(false);

        scene.tweens.add({
            targets: this.indicator,
            y: y - 14,
            duration: 800,
            yoyo: true,
            repeat: -1
        });
    }

    showIndicator() {
        this.indicator.setVisible(true);
    }

    hideIndicator() {
        this.indicator.setVisible(false);
    }

    interact() {
        if (this.dialogueSystem.isActive) return;

        this.hideIndicator();
        this.dialogueSystem.show(this.message);
    }
}
