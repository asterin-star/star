# Configurar Credenciales de Google en Vercel

## Problema Actual

El API está desplegado pero falla con:
```
DefaultCredentialsError: Your default credentials were not found
```

Esto es porque `service_account.json` no está en Git (correcto por seguridad).

## Solución: Variables de Entorno en Vercel

### Opción 1: Via Vercel Dashboard (Recomendado)

1. **Codifica el archivo de credenciales:**
   ```bash
   cd /home/star/star
   base64 -w 0 service_account.json > credentials.b64
   cat credentials.b64
   ```

2. **Copia el contenido** del archivo `credentials.b64`

3. **En Vercel Dashboard:**
   - Ve a https://vercel.com/asterin-star/star/settings/environment-variables
   - Click "Add New"
   - Name: `GOOGLE_APPLICATION_CREDENTIALS_BASE64`
   - Value: Pega el contenido de `credentials.b64`
   - Environment: Production, Preview, Development (todos)
   - Click "Save"

4. **Redeploy:**
   - Ve a Deployments
   - Click en el último deployment
   - Click "Redeploy"

### Opción 2: Via Vercel CLI

```bash
# 1. Instalar Vercel CLI
npm i -g vercel

# 2. Login
vercel login

# 3. Link project
cd /home/star/star
vercel link

# 4. Codificar y agregar credenciales
base64 -w 0 service_account.json | vercel env add GOOGLE_APPLICATION_CREDENTIALS_BASE64

# 5. Seleccionar todos los ambientes (Production, Preview, Development)

# 6. Redeploy
vercel --prod
```

## Actualizar el Código del API

También necesitas actualizar `api/index.py` para decodificar las credenciales:

```python
# En initialize_vertex_ai()
import base64
import tempfile

credentials_b64 = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_BASE64')
if credentials_b64:
    # Decode and write to temp file
    credentials_json = base64.b64decode(credentials_b64)
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        f.write(credentials_json.decode('utf-8'))
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f.name
elif os.path.exists('service_account.json'):
    # Local development fallback
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_account.json'
```

## Testing Local

Para probar localmente mientras tanto:

```bash
cd /home/star/star
python3 backend.py
```

Luego en otra terminal:
```bash
curl -X POST http://localhost:8000/api/synthesize-numerology \
  -H "Content-Type: application/json" \
  -d '{"cardName":"El Loco","language":"es",...}'
```

## Alternativa Rápida: Archivo de Credenciales

Si prefieres no usar variables de entorno:

1. **Agrega el archivo al repo** (no recomendado para producción):
   ```bash
   git add -f service_account.json
   git commit -m "Add service account (temporary)"
   git push
   ```

2. **Después del deployment, remuévelo:**
   ```bash
   git rm service_account.json
   git commit -m "Remove service account"
   git push
   ```

**⚠️ ADVERTENCIA**: Esto expone tus credenciales en el historial de Git. Solo hazlo si el repo es privado y luego rotarás las credenciales.

## Verificación

Una vez configurado, verifica:

```bash
# Health check
curl https://star-rust.vercel.app/api/synthesize-numerology

# Debería mostrar:
# "vertex_initialized": true

# Test completo
curl -X POST https://star-rust.vercel.app/api/synthesize-numerology \
  -H "Content-Type: application/json" \
  -d '{...}'
```

## ¿Qué método prefieres?

1. **Variables de entorno via Dashboard** - Más seguro, recomendado
2. **Variables de entorno via CLI** - Automatizado, seguro
3. **Archivo en Git (temporal)** - Rápido pero menos seguro

Dime cuál prefieres y te ayudo a implementarlo.
