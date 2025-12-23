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
4.  **Verificación**: Worldcoin revisará que la app funcione y cumpla las normas.

## 4. Pruebas
- **En PC**: Si abres la app en tu navegador, te preguntará si quieres "Simular" el pago (Modo Dev).
- **En World App**: Al abrirla desde la billetera, intentará hacer la transacción real de 1 WLD.
