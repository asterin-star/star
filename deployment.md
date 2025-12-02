# 🚀 Guía de Despliegue para Star ✦

Tu aplicación **Star ✦** está lista para ser desplegada. Tienes dos opciones principales dependiendo de si quieres usar la versión "Smart Mock" (Frontend puro) o la versión "Full Stack" (con Backend Python).

## Opción 1: Despliegue Estático (Recomendado - Frontend Puro)

Esta es la opción más rápida y robusta. La versión actual de `index.html` incluye una "Simulación Inteligente" (Smart Mock) que genera lecturas holísticas usando el tiempo y el contexto, sin necesidad de un servidor backend activo.

### Plataformas Recomendadas:
- **Vercel** (Ideal para este proyecto)
- **Netlify**
- **GitHub Pages**

### Pasos para Vercel:
1.  Asegúrate de tener el archivo `vercel.json` en la raíz (ya creado).
2.  Instala Vercel CLI: `npm i -g vercel`
3.  Ejecuta: `vercel`
4.  Sigue las instrucciones en pantalla.

### Pasos para Netlify:
1.  Arrastra la carpeta `star` completa al panel de "Sites" en Netlify.
2.  ¡Listo!

---

## Opción 2: Despliegue Full Stack (Frontend + Python Backend)

Si deseas activar la integración real con la API de Google Gemini (usando `backend.py`), necesitarás un servidor que soporte Python.

### Requisitos:
- Cuenta de Google Cloud con Vertex AI habilitado.
- Archivo `service_account.json` válido.

### Pasos:
1.  **Configurar Backend**:
    - Asegúrate de que `backend.py` esté configurado con tu `PROJECT_ID`.
    - Instala dependencias: `pip install -r requirements.txt`
2.  **Actualizar Frontend**:
    - En `index.html`, modifica la función del botón IA para hacer `fetch('/api/synthesize-numerology')` en lugar del `setTimeout`.
3.  **Desplegar en Render/Railway**:
    - Sube el código a un repositorio.
    - Configura el servicio como "Web Service" con Python.
    - Comando de inicio: `python backend.py`

---

## 📂 Archivos Importantes

- `index.html`: Aplicación principal (Frontend).
- `vercel.json`: Configuración para despliegue estático en Vercel.
- `backend.py`: Servidor API (opcional para Opción 2).
- `service_account.json`: Credenciales (¡No subir a repositorios públicos!).
