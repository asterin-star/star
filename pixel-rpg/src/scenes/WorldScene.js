import Phaser from 'phaser';
import DialogueSystem from '../systems/DialogueSystem.js';
import NPC from '../entities/NPC.js';
import Interactable from '../entities/Interactable.js';
import dialogueData from '../data/dialogue.json';

/**
 * WorldScene - Main game world
 * Handles player movement, map rendering, and interactions
 */
export default class WorldScene extends Phaser.Scene {
    constructor() {
        super({ key: 'WorldScene' });
        this.player = null;
        this.cursors = null;
        this.dialogueSystem = null;
        this.npcs = [];
        this.interactables = [];
        this.nearbyEntity = null;
    }

    create() {
        const { width, height } = this.cameras.main;

        // Initialize DialogueSystem
        this.dialogueSystem = new DialogueSystem(this);

        // Background
        this.add.rectangle(0, 0, width, height, 0x222222).setOrigin(0);

        // Create floor using programmatic tiles
        for (let x = 0; x < width; x += 16) {
            for (let y = 0; y < height; y += 16) {
                this.add.image(x, y, 'tile_floor').setOrigin(0);
            }
        }

        // Create walls
        this.walls = this.physics.add.staticGroup();
        // Assuming frame 1 is wall
        // Border walls
        for (let x = 0; x < width; x += 16) {
            this.createTileWall(x, 0);
            this.createTileWall(x, height - 16);
        }
        for (let y = 16; y < height - 16; y += 16) {
            this.createTileWall(0, y);
            this.createTileWall(width - 16, y);
        }

        // Create player
        this.createPlayer(width / 2, height / 2);

        // Create NPCs
        this.createNPCs();

        // Create Interactables
        this.createInteractables();

        // Setup camera
        this.cameras.main.startFollow(this.player);
        this.cameras.main.setZoom(1);

        // Setup input
        this.cursors = this.input.keyboard.createCursorKeys();
        this.wasd = this.input.keyboard.addKeys({
            up: Phaser.Input.Keyboard.KeyCodes.W,
            down: Phaser.Input.Keyboard.KeyCodes.S,
            left: Phaser.Input.Keyboard.KeyCodes.A,
            right: Phaser.Input.Keyboard.KeyCodes.D,
            action: Phaser.Input.Keyboard.KeyCodes.SPACE
        });

        // Action key for interactions
        this.wasd.action.on('down', () => {
            if (this.nearbyEntity && !this.dialogueSystem.isActive) {
                this.nearbyEntity.interact();
            }
        });

        // Collision
        this.physics.add.collider(this.player, this.walls);

        // NPC collision (player can't walk through NPCs)
        this.npcs.forEach(npc => {
            this.physics.add.collider(this.player, npc);
        });

        // Interactable collision
        this.interactables.forEach(obj => {
            this.physics.add.collider(this.player, obj);
        });

        // UI
        this.instructionText = this.add.text(8, 8, 'WASD/Arrows: Move • SPACE: Interact', {
            fontFamily: 'monospace',
            fontSize: '8px',
            color: '#ffffff',
            backgroundColor: '#000000',
            padding: { x: 4, y: 2 }
        }).setScrollFactor(0).setDepth(200);
    }

    createTileWall(x, y) {
        const wall = this.physics.add.image(x + 8, y + 8, 'tile_wall');
        wall.setImmovable(true);
        this.walls.add(wall);
    }

    createPlayer(x, y) {
        // Create player sprite (programmatic, no animation frames)
        this.player = this.physics.add.sprite(x, y, 'player_down');

        this.player.setCollideWorldBounds(true);
        // Hitbox for 16x20 sprite
        this.player.body.setSize(12, 16);
        this.player.body.setOffset(2, 4);
        this.player.setDepth(10);
    }

    createNPCs() {
        // Create villager NPC
        const villager = new NPC(
            this,
            120,
            120,
            dialogueData.npcs.villager1,
            this.dialogueSystem,
            'npc_villager'
        );
        this.npcs.push(villager);

        // Create mysterious figure
        const mysteriousFigure = new NPC(
            this,
            200,
            80,
            dialogueData.npcs.mysterious_figure,
            this.dialogueSystem,
            'npc_mysterious'
        );
        this.npcs.push(mysteriousFigure);
    }

    createInteractables() {
        // Plant - using tile_wall as placeholder
        const plant = new Interactable(
            this,
            60,
            60,
            'tile_wall',
            0,
            "Es una planta artificial. Luce extrañamente real.",
            this.dialogueSystem
        );
        this.interactables.push(plant);

        // Bookshelf
        const bookshelf = new Interactable(
            this,
            90,
            32, // Near top wall
            'tiles',
            2, // Assuming frame 2 is bookshelf
            "Muchos libros viejos sobre historias de monstruos y humanos.",
            this.dialogueSystem
        );
        this.interactables.push(bookshelf);
    }

    update() {
        if (!this.player) return;

        // Player movement (only if not in dialogue)
        if (!this.dialogueSystem.isActive) {
            const speed = 80;
            this.player.setVelocity(0);

            // Check input
            let moving = false;

            if (this.cursors.left.isDown || this.wasd.left.isDown) {
                this.player.setVelocityX(-speed);
                moving = true;
            } else if (this.cursors.right.isDown || this.wasd.right.isDown) {
                this.player.setVelocityX(speed);
                moving = true;
            }

            if (this.cursors.up.isDown || this.wasd.up.isDown) {
                this.player.setVelocityY(-speed);
                moving = true;
            } else if (this.cursors.down.isDown || this.wasd.down.isDown) {
                this.player.setVelocityY(speed);
                moving = true;
            }

            // Normalize diagonal movement
            if (this.player.body.velocity.x !== 0 && this.player.body.velocity.y !== 0) {
                this.player.body.velocity.normalize().scale(speed);
            }

            if (!moving) {
                this.player.anims.stop();
                // Optionally set idle frame based on last direction
            }
        } else {
            // Stop player movement during dialogue
            this.player.setVelocity(0);
        }

        // Check proximity to Entities (NPCs + Interactables)
        this.nearbyEntity = null;
        const interactionDistance = 24;

        const allEntities = [...this.npcs, ...this.interactables];

        allEntities.forEach(entity => {
            const distance = Phaser.Math.Distance.Between(
                this.player.x,
                this.player.y,
                entity.x,
                entity.y
            );

            if (distance < interactionDistance) {
                entity.showIndicator();
                this.nearbyEntity = entity;
            } else {
                entity.hideIndicator();
            }

            // Call update IF the entity has one (Interactables might not need it if they just have indicators managed here)
            if (entity.update) entity.update();
        });
    }
}
