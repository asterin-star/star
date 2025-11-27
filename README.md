# 🔮 Oráculo de Tarot - Aplicación Web

Una elegante aplicación web de oráculo de tarot con 22 cartas del Arca Mayor, diseño glassmorphism y experiencia interactiva completa.

## ✨ Características

- **22 Cartas del Arca Mayor** con imágenes y datos completos
- **Diseño Glassmorphism** con efectos de cristal translúcido
- **Modal Interactivo** con información completa de cada carta
- **6 Categorías de Interpretación**:
  - ✧ Sombras y Peligros
  - ✦ Misticismo  
  - 🌿 Botánica
  - 🏠 Cotidiano
  - 🔮 Místico
  - 📖 Bíblico
- **Contenido Sin Límites** - texto completo sin truncamiento
- **Responsive Design** - funciona en todos los dispositivos

## 🚀 Cómo Usar

### Opción 1: Con Python (Recomendado)

1. **Descomprimir el archivo ZIP**
2. **Abrir terminal/consola** en la carpeta del proyecto
3. **Ejecutar el servidor**:
   ```bash
   python server.py
   ```
4. **Abrir navegador** en: `http://localhost:8001`

### Opción 2: Con cualquier servidor web

Puedes usar cualquier servidor web para servir los archivos:
- **Node.js**: `npx serve .`
- **Python**: `python -m http.server 8001`
- **PHP**: `php -S localhost:8001`
- **Apache/Nginx**: Configurar la carpeta como document root

## 📁 Estructura del Proyecto

```
tarot-oracle-app/
├── index.html          # Aplicación principal
├── server.py           # Servidor Python (opcional)
├── cards/              # Imágenes de las cartas (ar00.jpg - ar21.jpg)
├── data/               # Datos JSON de las cartas
│   ├── 0-5.json
│   ├── 6-10.json
│   ├── 11-15.json
│   └── 16-21.json
└── README.md           # Este archivo
```

## 🎯 Cómo Funciona

1. **Haz clic** en el botón "Nueva Consulta" o en una carta
2. **Voltea la carta** para revelar la respuesta
3. **Lee el insight** con la interpretación completa
4. **Explora las 6 categorías** de interpretación mística

## 🛠️ Tecnologías

- **HTML5** + **CSS3** + **JavaScript**
- **CSS Grid** y **Flexbox** para layouts
- **Backdrop-filter** para efectos glassmorphism
- **JSON** para datos estructurados
- **Python HTTP Server** para desarrollo local

## 🎨 Características Técnicas

- **Efectos Glassmorphism**: Fondos translúcidos con blur
- **Animaciones Suaves**: Transiciones CSS fluidas
- **Sin Dependencias**: Funciona sin librerías externas
- **Carga Dinámica**: Contenido JSON cargado on-demand
- **Completamente Offline**: No requiere conexión a internet

## 📱 Compatibilidad

- ✅ Chrome, Firefox, Safari, Edge
- ✅ Dispositivos móviles y tablets
- ✅ Windows, macOS, Linux
- ✅ Python 3.6+

## 🔧 Personalización

Para modificar el contenido, edita los archivos JSON en la carpeta `data/`:
- `arquetipo`: Arquetipo principal de la carta
- `sombra`: Aspectos peligrosos/sombríos
- `misticismo`: Interpretación mística/esotérica
- `botanica`: Conexión con plantas/elementos naturales
- `cotidiano`: Aplicación práctica en la vida diaria
- `gnosis`: Conocimiento esotérico avanzado
- `resonancia_biblica`: Referencias bíblicas relevantes

---

**Desarrollado con ✨ por MiniMax Agent**

🎴 *Que las cartas te guíen en tu camino de autodescubrimiento*