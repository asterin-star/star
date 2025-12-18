import Phaser from 'phaser';

/**
 * NPC - Non-Player Character
 * Handles NPC rendering and interaction triggers
 */
export default class NPC extends Phaser.Physics.Arcade.Sprite {
    constructor(scene, x, y, npcData, dialogueSystem, textureKey = 'npc_villager') {
        super(scene, x, y, textureKey);

        this.scene = scene;
        this.npcData = npcData;
        this.dialogueSystem = dialogueSystem;
        this.currentDialogueId = 'greeting';
        this.isInteracting = false;

        // Add to scene
        scene.add.existing(this);
        scene.physics.add.existing(this);

        // Make static (NPCs don't move)
        this.body.setImmovable(true);
        this.body.setSize(12, 16);
        this.body.setOffset(2, 4);
        this.setDepth(5);

        // Add interaction indicator (exclamation mark)
        this.indicator = scene.add.text(x, y - 12, '!', {
            fontFamily: 'monospace',
            fontSize: '10px',
            color: '#ffff00',
            stroke: '#000000',
            strokeThickness: 2
        }).setOrigin(0.5);
        this.indicator.setDepth(6);
        this.indicator.setVisible(false);

        // Bobbing animation for indicator
        scene.tweens.add({
            targets: this.indicator,
            y: y - 14,
            duration: 500,
            yoyo: true,
            repeat: -1,
            ease: 'Sine.easeInOut'
        });
    }

    showIndicator() {
        if (!this.isInteracting) {
            this.indicator.setVisible(true);
        }
    }

    hideIndicator() {
        this.indicator.setVisible(false);
    }

    interact() {
        if (this.isInteracting || this.dialogueSystem.isActive) return;

        this.isInteracting = true;
        this.hideIndicator();

        // Find the current dialogue
        const dialogue = this.npcData.dialogues.find(d => d.id === this.currentDialogueId);

        if (!dialogue) {
            console.error('Dialogue not found:', this.currentDialogueId);
            this.isInteracting = false;
            return;
        }

        // Convert dialogue choices to DialogueSystem format
        const choices = dialogue.choices.map(choice => ({
            text: choice.text,
            callback: () => {
                if (choice.next) {
                    this.currentDialogueId = choice.next;
                    // Reset to greeting after showing next dialogue
                    this.scene.time.delayedCall(100, () => {
                        this.interact();
                    });
                } else {
                    this.isInteracting = false;
                }
            }
        }));

        // Show dialogue
        this.dialogueSystem.show(
            dialogue.text,
            this.npcData.name,
            choices,
            () => {
                this.isInteracting = false;
                // Reset to greeting for next interaction if no choices
                if (choices.length === 0) {
                    this.currentDialogueId = 'greeting';
                }
            }
        );
    }

    update() {
        // Update indicator position
        this.indicator.x = this.x;
    }

    destroy() {
        if (this.indicator) {
            this.indicator.destroy();
        }
        super.destroy();
    }
}
