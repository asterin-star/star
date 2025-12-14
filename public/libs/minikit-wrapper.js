/**
 * MiniKit Wrapper for Vanilla JS
 * 
 * Este archivo crea un objeto window.MiniKit compatible con la API
 * esperada por la aplicación, pero funciona en entornos donde el
 * SDK oficial no se puede cargar (HTML vanilla sin bundler).
 * 
 * IMPORTANTE: Este es un POLYFILL. Si el World App Simulator inyecta
 * el MiniKit real, este código lo detectará y NO lo sobrescribirá.
 */

(function () {
    'use strict';

    // Si MiniKit ya existe (inyectado por World App), no hacer nada
    if (window.MiniKit && window.MiniKit.commands) {
        console.log('✅ MiniKit real detectado (inyectado por World App)');
        return;
    }

    console.log('⚠️ MiniKit no detectado. Inicializando wrapper local...');

    // Crear objeto MiniKit simulado
    const MiniKitWrapper = {
        isInstalled() {
            // En el simulador, esto debería ser true si estamos dentro de World App
            // Por ahora, asumimos que sí si este código se ejecuta
            return typeof window !== 'undefined';
        },

        install() {
            console.log('📦 MiniKit.install() llamado');
            // En el wrapper, no hay nada que instalar
            return true;
        },

        commands: {
            async pay(payload) {
                console.log('💳 MiniKit.commands.pay() llamado con:', payload);

                // SIMULACIÓN: En un entorno real, esto abriría el modal de World App
                // Aquí, mostramos un confirm para simular la aprobación del usuario
                const userApproved = confirm(
                    `🌍 Simulación de Pago Worldcoin\n\n` +
                    `Monto: ${payload.tokens[0].token_amount} ${payload.tokens[0].symbol}\n` +
                    `Destinatario: ${payload.to}\n` +
                    `Descripción: ${payload.description}\n\n` +
                    `¿Aprobar pago?`
                );

                if (userApproved) {
                    // Simular respuesta exitosa
                    return {
                        finalPayload: {
                            status: 'success',
                            transaction_id: 'sim_' + Date.now(),
                            reference: payload.reference
                        }
                    };
                } else {
                    // Simular rechazo
                    throw new Error('User rejected payment');
                }
            },

            async walletAuth(payload) {
                console.log('🔐 MiniKit.commands.walletAuth() llamado');
                throw new Error('walletAuth no implementado en wrapper');
            }
        }
    };

    // Exponer en window
    window.MiniKit = MiniKitWrapper;
    console.log('✅ MiniKit wrapper instalado');
})();
