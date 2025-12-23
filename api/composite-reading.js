export default async function handler(req, res) {
    // Only allow POST requests
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    try {
        const { cards } = req.body;

        // Validate input
        if (!cards || !Array.isArray(cards) || cards.length !== 3) {
            return res.status(400).json({ error: 'Invalid card data' });
        }

        const DISCORD_WEBHOOK_URL = process.env.DISCORD_WEBHOOK_URL;

        // If no webhook configured, fail gracefully
        if (!DISCORD_WEBHOOK_URL) {
            console.error('DISCORD_WEBHOOK_URL not configured');
            return res.status(500).json({ error: 'Service not configured' });
        }

        // Create Discord embed payload
        const discordPayload = {
            embeds: [{
                title: "🔮 Nueva Solicitud de Lectura Compuesta",
                description: "Un usuario ha completado 3 cartas y solicita una lectura profunda.",
                color: 0xFFEB3B, // Gold color matching Star Oracle theme
                fields: cards.map((card, idx) => ({
                    name: `Carta ${idx + 1}`,
                    value: card.name || 'Unknown Card',
                    inline: true
                })),
                footer: {
                    text: "Star Oracle - Composite Reading Request"
                },
                timestamp: new Date().toISOString()
            }]
        };

        // Send to Discord
        const response = await fetch(DISCORD_WEBHOOK_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(discordPayload)
        });

        if (!response.ok) {
            throw new Error(`Discord API error: ${response.status}`);
        }

        return res.status(200).json({
            success: true,
            message: 'Solicitud enviada correctamente'
        });

    } catch (error) {
        console.error('Error sending to Discord:', error);
        return res.status(500).json({
            error: 'Failed to send request',
            details: error.message
        });
    }
}
