# MiniKit SDK - Guía de Solución de Problemas

## Error: "MiniKit está NULL"

Este error indica que el SDK de MiniKit no se cargó correctamente.

### Soluciones por Orden de Probabilidad

#### 1. Limpiar Caché del Navegador (Más Común)

El navegador puede estar usando una versión en caché del SDK antiguo o corrupto.

**Chrome/Edge:**
1. Presiona `Ctrl+Shift+Delete` (Windows) o `Cmd+Shift+Delete` (Mac)
2. Selecciona "Archivos e imágenes en caché"
3. Haz clic en "Borrar datos"
4. Recarga la página con `Ctrl+F5` o `Cmd+Shift+R`

**Firefox:**
1. Presiona `Ctrl+Shift+Delete`
2. Selecciona "Caché"
3. Haz clic en "Limpiar ahora"
4. Recarga la página con `Ctrl+F5`

#### 2. Verificar Consola del Navegador

Abre las herramientas de desarrollador (F12) y revisa la consola.

**Logs Exitosos:**
```
MiniKit install ok [object]
```
o
```
MiniKit detected after 2 attempts
MiniKit install ok [object]
```

**Logs de Error:**
```
MiniKit SDK failed to load after multiple attempts
```
→ Indica que el SDK no se descargó. Revisa la pestaña "Network" (Red).

```
MiniKit install failed: [error message]
```
→ El SDK se cargó pero install() falló. Puede ser un problema de versión.

#### 3. Verificar Pestaña Network (Red)

En las herramientas de desarrollador:
1. Ve a la pestaña "Network" o "Red"
2. Recarga la página
3. Busca `minikit-js@latest` en la lista
4. Verifica:
   - Status: debe ser `200` (verde)
   - Type: `script`
   - Size: debe ser varios KB (no 0)

**Si el Status es:**
- `404`: El archivo no existe en el CDN → Reportar issue
- `CORS error`: Problema de seguridad del navegador
- `Failed`: Problema de conexión a internet

#### 4. Probar en Modo Incógnito/Privado

Esto elimina extensiones y caché que podrían interferir:
1. Abre una ventana de incógnito (Ctrl+Shift+N)
2. Ve a la URL de la app
3. Si funciona aquí, el problema es una extensión o configuración del navegador

#### 5. Verificar que Estés en el Entorno Correcto

**Localhost (Desarrollo):**
- URL debe ser `http://localhost:xxxx` o `http://127.0.0.1:xxxx`
- El modo dev mostrará un diálogo de simulación de pago
- No es necesario estar en World App

**World App (Producción):**
- Debe abrirse desde la app World App en el móvil
- No funcionará en navegador regular para pagos reales
- Puedes usar el simulador de World App

**Modo Amigos (Gratis):**
- URL debe incluir `?mode=friends`
- No requiere pago, salta directo a la revelación

#### 6. Verificar Bloqueadores de Anuncios

Algunos bloqueadores pueden bloquear scripts de CDN:
1. Desactiva temporalmente el bloqueador (AdBlock, uBlock, etc.)
2. Recarga la página
3. Si funciona, añade la URL a la lista blanca del bloqueador

#### 7. Revisar Versión del Navegador

MiniKit requiere un navegador moderno con soporte para ES6+:
- Chrome: v80+
- Firefox: v75+
- Safari: v13+
- Edge: v80+

Si tu navegador es muy antiguo, actualízalo.

### Debugging Avanzado

#### Ver Detalles Completos del SDK

Abre la consola y ejecuta:
```javascript
// Ver si MiniKit existe
console.log('MiniKit exists:', typeof window.MiniKit);

// Ver propiedades del SDK
if (window.MiniKit) {
    console.log('MiniKit keys:', Object.keys(window.MiniKit));
    console.log('Commands available:', !!window.MiniKit.commands);
    console.log('Is installed:', window.MiniKit.isInstalled?.());
}
```

#### Forzar Reinstalación Manual

Si el SDK está cargado pero no instalado:
```javascript
// En la consola
await window.MiniKit.install();
```

### Casos Especiales

#### Error Persiste Después de Todo

Si después de intentar todo lo anterior el error persiste:

1. **Captura de pantalla de la consola:**
   - Abre herramientas de desarrollador (F12)
   - Ve a la pestaña "Console"
   - Recarga la página
   - Toma captura de todos los mensajes

2. **Captura de la pestaña Network:**
   - Ve a "Network" o "Red"
   - Recarga la página
   - Filtra por "minikit"
   - Toma captura del resultado

3. **Información del entorno:**
   - Navegador y versión
   - Sistema operativo
   - URL exacta que estás usando
   - Si estás en World App, simulador, o navegador normal

4. **Reporta el issue** con toda esta información

### Notas Importantes

⚠️ **Pagos Reales:**
- Solo funcionan en World App (app móvil oficial)
- Requiere whitelist de la wallet en Developer Portal
- No funcionan en navegador regular ni simulador

✅ **Modo Dev (localhost):**
- Muestra diálogo de simulación
- No requiere World App
- Perfecto para desarrollo y pruebas

🎁 **Modo Amigos (`?mode=friends`):**
- Gratis, sin pagos
- Funciona en cualquier navegador
- URL: `https://tu-dominio.com/?mode=friends`

### Versión Actual del SDK

La app ahora usa:
```html
<script src="https://unpkg.com/@worldcoin/minikit-js@latest"></script>
```

Con retry logic de 10 intentos (1 segundo total) para manejar cargas lentas del SDK.

### Contacto

Si nada de esto funciona, abre un issue con:
- Capturas de consola y network
- Información de tu entorno
- Pasos que ya intentaste
