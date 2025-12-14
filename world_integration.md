# 🌍 Integración con World App (Mini App & Pagos)

Hemos configurado **Star ✦** para cobrar en WLD por cada lectura y la síntesis numerológica, enviando los fondos directamente a tu billetera.

## 1. Configuración Actual
- **Wallet de Destino**: `0xa3cdea9fe705bc16dcd9e9170e217b0f1ba5aaf6`
- **Precios**:
  - **Revelación de Carta**: 1.11 WLD
  - **Síntesis Numerológica IA**: 2.22 WLD
- **Flujo**:
    1.  Usuario toca la carta.
    2.  Se solicita el pago de 1.11 WLD en World App.
    3.  Si paga -> Se revela la carta.
    4.  Si cancela -> La carta permanece oculta.
    5.  Usuario puede solicitar síntesis IA (botón ✦).
    6.  Se solicita el pago de 2.22 WLD.
    7.  Si paga -> Se genera la lectura personalizada.
    8.  Al reiniciar (voltear de nuevo), se requiere un nuevo pago para la siguiente carta.

## 2. Modo "Amigos" (Gratis)
Para crear la versión gratuita para tus amigos, **no necesitas desplegar otra app**. Simplemente comparte el link con un código especial al final.

- **Link de Pago (Público)**: `https://star-rust.vercel.app/`
- **Link Gratis (Amigos)**: `https://star-rust.vercel.app/?mode=friends`

Cuando alguien entra con `?mode=friends`, el sistema omite el cobro automáticamente.

## 3. Pasos para Publicar en World App

1.  **Desplegar**: Usa el comando que te di anteriormente para subir la versión final a Vercel.
    ```bash
    npx vercel --token vck_4rUDwfRVtDpidNNHav1hqYGPA5qfGFiXvzp0ZlpKJIqGPZ2w0P02iuJx --prod
    ```
2.  **Developer Portal**: Ve a [developer.worldcoin.org](https://developer.worldcoin.org).
3.  **Crear App**:
    - **Name**: Star ✦
    - **Category**: Entertainment / Utility
    - **App URL**: La URL que te dio Vercel (ej. `https://star-oracle.vercel.app`).
    - **Description**: "Oráculo de Tarot y Numerología del presente."
4.  **Whitelisting de la dirección** (CRÍTICO):
    - En el Developer Portal, whitelistea la dirección de destino: `0xa3cdea9fe705bc16dcd9e9170e217b0f1ba5aaf6`
    - Sin esto, los pagos reales pueden fallar aunque el SDK cargue correctamente.
5.  **Verificación**: Worldcoin revisará que la app funcione y cumpla las normas.

## 4. Pruebas
- **En PC**: Si abres la app en tu navegador, te preguntará si quieres "Simular" el pago (Modo Dev).
- **En World App**: Al abrirla desde la billetera, intentará hacer la transacción real de 1 WLD.

## 5. Check-list de Pruebas Completo

### 5.1 Localhost con modo dev
- [ ] Abrir `http://localhost:8000/?mode=friends` en navegador
- [ ] Verificar que la carta se revela sin pagar (modo amigos)
- [ ] Abrir `http://localhost:8000/` sin parámetros
- [ ] Verificar que aparece el diálogo de simulación de pago en localhost

### 5.2 Simulador World App
- [ ] Abrir la app en el simulador de World App
- [ ] Usar `test_minikit.html` para verificar que `MiniKit.commands` existe
- [ ] Comprobar logs: `typeof MiniKit`, `MiniKit.isInstalled()`, y `Object.keys(MiniKit)`
- [ ] Si `commands` está ausente, es un problema de inyección parcial del simulador

### 5.3 World App real con pagos de prueba
- [ ] Hacer pago de 1.11 WLD para revelar carta
- [ ] Verificar que la carta se revela correctamente
- [ ] Hacer pago de 2.22 WLD para síntesis numerológica IA
- [ ] Verificar que se genera y muestra la síntesis

### 5.4 Confirmación de recepción
- [ ] Verificar que los fondos llegan a la wallet: `0xa3cdea9fe705bc16dcd9e9170e217b0f1ba5aaf6`
- [ ] Comprobar el historial de transacciones en World App

## 6. Cambios Técnicos Implementados (v2.8)

### 6.1 SDK Actualizado
- Cambio a `https://unpkg.com/@worldcoin/minikit-js@latest` (verified working CDN)
- Instalación defensiva con `async/await` y manejo de errores
- Retry logic con múltiples intentos (hasta 10 intentos con 100ms de intervalo)

### 6.2 Instalación Mejorada
```javascript
async function initMiniKit() {
    if (!window.MiniKit) {
        console.warn('MiniKit no presente en window');
        return;
    }
    try {
        const res = await window.MiniKit.install();
        console.log('MiniKit install ok', res);
    } catch (e) {
        console.error('MiniKit install failed', e);
    }
}
initMiniKit();
```

### 6.3 Revalidación de Commands
Antes de cada operación `commands.pay`, se verifica y reinstala si es necesario:
```javascript
if (!window.MiniKit.commands) {
    console.log('🔄 Commands missing. Forcing install()...');
    await window.MiniKit.install();
}
if (!window.MiniKit.commands) {
    throw new Error('MiniKit commands no disponibles');
}
```

### 6.4 Tolerancia para el Simulador
- Se mantiene el fallback para localhost (modo dev)
- Se lanza error explícito si `commands` está ausente, incluso si `MiniKit` existe
- Logs mejorados para diagnóstico de inyección parcial
