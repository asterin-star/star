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

    // ESTRATEGIA DE DETECCIÓN AGRESIVA
    // Esperar un momento para que World App inyecte su MiniKit
    const checkForNativeMiniKit = () => {
        // Si MiniKit ya existe con commands (inyectado por World App), usarlo
        if (window.MiniKit && window.MiniKit.commands && typeof window.MiniKit.commands.pay === 'function') {
            console.log('✅ MiniKit NATIVO detectado (World App)');
            return true;
        }
        return false;
    };

    // Verificar inmediatamente
    if (checkForNativeMiniKit()) {
        return; // Usar el nativo
    }

    console.log('⚠️ MiniKit nativo no detectado aún. Instalando wrapper...');

    // Determinar si estamos en localhost (desarrollo) o producción
    const isLocalhost = window.location.hostname === 'localhost' ||
        window.location.hostname === '127.0.0.1';

    // Crear objeto MiniKit wrapper
    const MiniKitWrapper = {
        isInstalled() {
            // Verificar de nuevo si el nativo apareció
            if (checkForNativeMiniKit()) {
                return window.MiniKit.isInstalled();
            }
            return typeof window !== 'undefined';
        },

        install() {
            console.log('📦 MiniKit.install() llamado');
            // Si el nativo existe, llamar su install
            if (window.MiniKit && window.MiniKit !== MiniKitWrapper && typeof window.MiniKit.install === 'function') {
                return window.MiniKit.install();
            }
            return true;
        },

        commands: {
            async pay(payload) {
                console.log('💳 MiniKit.commands.pay() llamado con:', payload);

                // CRÍTICO: Verificar si el MiniKit nativo apareció
                if (window.MiniKit &&
                    window.MiniKit !== MiniKitWrapper &&
                    window.MiniKit.commands &&
                    typeof window.MiniKit.commands.pay === 'function') {
                    console.log('🔄 Delegando a MiniKit nativo...');
                    return await window.MiniKit.commands.pay(payload);
                }

                // Si NO estamos en localhost, lanzar error (producción sin SDK)
                if (!isLocalhost) {
                    throw new Error('MiniKit no disponible. Por favor, abre esta app desde World App.');
                }

                // SOLO EN LOCALHOST: Simulación para desarrollo
                console.warn('🧪 Modo Simulación (Solo Desarrollo)');
                const userApproved = confirm(
                    `🧪 SIMULACIÓN DE PAGO (Solo Desarrollo)\n\n` +
                    `Monto: ${payload.tokens[0].token_amount} ${payload.tokens[0].symbol}\n` +
                    `Destinatario: ${payload.to}\n` +
                    `Descripción: ${payload.description}\n\n` +
                    `¿Aprobar pago simulado?`
                );

                if (userApproved) {
                    return {
                        finalPayload: {
                            status: 'success',
                            transaction_id: 'sim_' + Date.now(),
                            reference: payload.reference
                        }
                    };
                } else {
                    throw new Error('User rejected payment');
                }
            },

            async walletAuth(payload) {
                console.log('🔐 MiniKit.commands.walletAuth() llamado');

                // Intentar delegar al nativo
                if (window.MiniKit &&
                    window.MiniKit !== MiniKitWrapper &&
                    window.MiniKit.commands &&
                    typeof window.MiniKit.commands.walletAuth === 'function') {
                    return await window.MiniKit.commands.walletAuth(payload);
                }

                throw new Error('walletAuth no disponible');
            }
        }
    };

    // Exponer en window
    window.MiniKit = MiniKitWrapper;
    console.log('✅ MiniKit wrapper instalado (detectará nativo si aparece)');

    // Verificar de nuevo después de 500ms por si el nativo se inyecta tarde
    setTimeout(() => {
        if (checkForNativeMiniKit() && window.MiniKit === MiniKitWrapper) {
            console.log('🔄 MiniKit nativo detectado tardíamente. Considerar recargar.');
        }
    }, 500);
})();
