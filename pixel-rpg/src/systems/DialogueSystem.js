import Phaser from 'phaser';

/**
 * DialogueSystem - Manages dialogue display and interaction
 * Features: Typewriter effect, choices, callbacks
 */
export default class DialogueSystem {
    constructor(scene) {
        this.scene = scene;
        this.isActive = false;
        this.dialogueBox = null;
        this.dialogueText = null;
        this.nameText = null;
        this.currentText = '';
        this.displayedText = '';
        this.textIndex = 0;
        this.typewriterTimer = null;
        this.onCompleteCallback = null;
        this.choices = [];
        this.choiceTexts = [];
        this.currentChoice = 0;
    }

    /**
     * Show a dialogue with typewriter effect
     * @param {string} text - The dialogue text to display
     * @param {string} speakerName - Name of the speaker (optional)
     * @param {Array} choices - Array of choice objects {text, callback} (optional)
     * @param {Function} onComplete - Callback when dialogue is dismissed (optional)
     */
    show(text, speakerName = '', choices = [], onComplete = null) {
        if (this.isActive) {
            this.hide();
        }

        this.isActive = true;
        this.currentText = text;
        this.displayedText = '';
        this.textIndex = 0;
        this.onCompleteCallback = onComplete;
        this.choices = choices;
        this.currentChoice = 0;

        const { width, height } = this.scene.cameras.main;

        // Create dialogue box
        const boxHeight = choices.length > 0 ? 80 : 60;
        const boxY = height - boxHeight - 8;

        // Box background
        this.dialogueBox = this.scene.add.graphics();
        this.dialogueBox.fillStyle(0x000000, 0.9);
        this.dialogueBox.fillRoundedRect(8, boxY, width - 16, boxHeight, 4);
        this.dialogueBox.lineStyle(2, 0xffffff, 1);
        this.dialogueBox.strokeRoundedRect(8, boxY, width - 16, boxHeight, 4);
        this.dialogueBox.setScrollFactor(0);
        this.dialogueBox.setDepth(100);

        // Speaker name interaction (background pill)
        if (speakerName) {
            this.nameBox = this.scene.add.graphics();
            this.nameBox.fillStyle(0xffffff, 1);
            this.nameBox.fillRoundedRect(16, boxY - 10, speakerName.length * 7 + 10, 14, 2);
            this.nameBox.setScrollFactor(0);
            this.nameBox.setDepth(101);

            this.nameText = this.scene.add.text(21, boxY - 8, speakerName, {
                fontFamily: 'monospace',
                fontSize: '10px',
                color: '#000000',
                fontStyle: 'bold'
            });
            this.nameText.setScrollFactor(0);
            this.nameText.setDepth(102);
        }

        // Dialogue text
        const textY = boxY + 10;
        this.dialogueText = this.scene.add.text(16, textY, '', {
            fontFamily: 'monospace',
            fontSize: '8px',
            color: '#ffffff',
            wordWrap: { width: width - 32 }
        });
        this.dialogueText.setScrollFactor(0);
        this.dialogueText.setDepth(101);

        // Start typewriter effect
        this.startTypewriter();

        // Setup input to skip/advance
        this.setupInput();
    }

    startTypewriter() {
        const typeSpeed = 30; // milliseconds per character

        this.typewriterTimer = this.scene.time.addEvent({
            delay: typeSpeed,
            callback: () => {
                if (this.textIndex < this.currentText.length) {
                    this.displayedText += this.currentText[this.textIndex];
                    this.dialogueText.setText(this.displayedText);
                    this.textIndex++;
                } else {
                    this.typewriterTimer.destroy();
                    this.showChoices();
                }
            },
            loop: true
        });
    }

    showChoices() {
        if (this.choices.length === 0) return;

        const { width, height } = this.scene.cameras.main;
        const startY = height - 40;

        this.choiceTexts = [];
        this.choices.forEach((choice, index) => {
            const choiceText = this.scene.add.text(
                24,
                startY + (index * 12),
                `${index === this.currentChoice ? '> ' : '  '}${choice.text}`,
                {
                    fontFamily: 'monospace',
                    fontSize: '8px',
                    color: index === this.currentChoice ? '#ffff00' : '#ffffff'
                }
            );
            choiceText.setScrollFactor(0);
            choiceText.setDepth(101);
            this.choiceTexts.push(choiceText);
        });
    }

    updateChoices() {
        this.choiceTexts.forEach((text, index) => {
            const isSelected = index === this.currentChoice;
            text.setText(`${isSelected ? '> ' : '  '}${this.choices[index].text}`);
            text.setColor(isSelected ? '#ffff00' : '#ffffff');
        });
    }

    setupInput() {
        // Create unique key for this dialogue instance
        const spaceKey = this.scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);
        const upKey = this.scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.UP);
        const downKey = this.scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.DOWN);

        // Input lock to prevent immediate triggering from the same press that opened the dialogue
        this.inputLock = true;
        this.scene.time.delayedCall(200, () => {
            this.inputLock = false;
        });

        this.spaceListener = () => {
            if (!this.isActive || this.inputLock) return;

            // If typewriter is still going, complete it instantly
            if (this.typewriterTimer && this.typewriterTimer.getProgress() < 1) {
                this.typewriterTimer.destroy();
                this.displayedText = this.currentText;
                this.dialogueText.setText(this.displayedText);
                this.textIndex = this.currentText.length;
                this.showChoices();
                // Add short lock to prevent accidental double-skip
                this.inputLock = true;
                this.scene.time.delayedCall(200, () => {
                    this.inputLock = false;
                });
            } else {
                // Dialogue is complete, handle choice or dismiss
                if (this.choices.length > 0) {
                    const selectedChoice = this.choices[this.currentChoice];
                    // Hide first, then execute callback
                    this.hide();
                    if (selectedChoice.callback) {
                        selectedChoice.callback();
                    }
                } else {
                    this.hide();
                }
            }
        };

        this.upListener = () => {
            if (!this.isActive || this.choices.length === 0 || this.inputLock) return;
            this.currentChoice = Math.max(0, this.currentChoice - 1);
            this.updateChoices();
        };

        this.downListener = () => {
            if (!this.isActive || this.choices.length === 0 || this.inputLock) return;
            this.currentChoice = Math.min(this.choices.length - 1, this.currentChoice + 1);
            this.updateChoices();
        };

        spaceKey.on('down', this.spaceListener);
        upKey.on('down', this.upListener);
        downKey.on('down', this.downListener);

        // Store keys for cleanup
        this.inputKeys = { spaceKey, upKey, downKey };
    }

    hide() {
        if (!this.isActive) return;

        this.isActive = false;

        // Destroy visuals
        if (this.dialogueBox) this.dialogueBox.destroy();
        if (this.dialogueText) this.dialogueText.destroy();
        if (this.nameText) this.nameText.destroy();
        if (this.nameBox) this.nameBox.destroy();

        this.choiceTexts.forEach(text => text.destroy());
        this.choiceTexts = [];

        // Clean up timer
        if (this.typewriterTimer) {
            this.typewriterTimer.destroy();
            this.typewriterTimer = null;
        }

        // Clean up input listeners
        if (this.inputKeys) {
            this.inputKeys.spaceKey.off('down', this.spaceListener);
            this.inputKeys.upKey.off('down', this.upListener);
            this.inputKeys.downKey.off('down', this.downListener);
        }

        // Call completion callback
        if (this.onCompleteCallback) {
            this.onCompleteCallback();
            this.onCompleteCallback = null;
        }
    }

    destroy() {
        this.hide();
    }
}
