# Configuración de Worldcoin Mini App

## Pasos para completar la integración:

1. **⚠️ IMPORTANTE - Reemplazar la dirección de wallet:**
   - Abrir `src/components/PaymentButton.jsx`
   - Buscar la línea con `to: '0x0000000000000000000000000000000000000000'`
   - Reemplazar con tu dirección de wallet de Worldcoin
   - **NO DESPLEGAR A PRODUCCIÓN SIN CAMBIAR ESTA DIRECCIÓN**
   - La dirección actual es un placeholder y no recibirá pagos

2. **Instalar dependencias:**
   ```bash
   npm install
   ```

3. **Ejecutar en desarrollo:**
   ```bash
   npm run dev
   ```

4. **Build para producción:**
   ```bash
   npm run build
   ```

## Notas importantes:
- La app debe ser probada dentro de World App para que funcione el sistema de pagos
- El precio actual está configurado a 0.1 WLD por lectura
- Cada pago genera un ID único con timestamp

## Estructura del proyecto:
```
star/
├── src/
│   ├── main.jsx                    # Punto de entrada con MiniKit.install()
│   ├── App.jsx                     # Componente principal con lógica de pago
│   ├── App.css                     # Estilos del componente principal
│   └── components/
│       └── PaymentButton.jsx       # Componente de pago con WLD
├── public/                         # Archivos estáticos (cartas, datos)
├── index.html                      # HTML base
├── vite.config.js                  # Configuración de Vite
└── package.json                    # Dependencias
```

## Flujo de la aplicación:
1. El usuario ve una carta boca abajo
2. Hace clic en el botón "Comprar Carta"
3. Se solicita el pago de 0.1 WLD a través de MiniKit
4. Si el pago es exitoso, la carta se revela con toda la información
5. El usuario puede hacer una nueva consulta que requerirá otro pago

## Desarrollo local:
Para pruebas locales fuera de World App, el componente detectará que MiniKit no está instalado y mostrará una alerta. Considera agregar un modo de desarrollo para testing sin pagos reales.
