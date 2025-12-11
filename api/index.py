from http.server import BaseHTTPRequestHandler
import json
import os
# Note: In Vercel, dependencies must be in requirements.txt

# Configuration
PROJECT_ID = 'gen-lang-client-0438257778'
LOCATION = 'us-central1'

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            
            # 1. Authentication & Initialization (Vertex AI)
            # We import here to avoid cold start issues if possible, though Vercel caches imports
            import vertexai
            from vertexai.generative_models import GenerativeModel
            
            # Initialize Vertex AI
            # Note: Vercel will need GOOGLE_APPLICATION_CREDENTIALS env var or similar
            # For this implementation, we assume the environment is set up or service_account.json is available
            # However, in Vercel, file paths can be tricky. 
            # Ideally, credentials should be passed via Environment Variables (Base64 encoded)
            # But for now we will try to use the existing pattern if the file is deployed.
            
            if os.path.exists('service_account.json'):
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_account.json'
            
            vertexai.init(project=PROJECT_ID, location=LOCATION)
            
            # 2. Build Prompt
            card_name = data.get('cardName', 'Carta Desconocida')
            definitions = data.get('definitions', {})
            examples = data.get('examples', {})
            
            prompt = f"""
            Eres un oráculo profesional especializado en orientación personal y desarrollo humano.
            Analiza la carta "{card_name}" y la siguiente configuración numerológica única para esta lectura:
            
            CONTEXTO DE LA LECTURA:
            - Arquetipo (Variante {examples.get('arquetipo', '?')}/22): "{definitions.get('arquetipo', '')}"
            - Sombra (Variante {examples.get('sombra', '?')}/22): "{definitions.get('sombra', '')}"
            - Misticismo (Variante {examples.get('misticismo', '?')}/22): "{definitions.get('misticismo', '')}"
            
            TAREA:
            Genera una lectura formal y directa (máximo 60 palabras) que identifique:
            1. El objetivo principal que esta persona debe desarrollar según esta carta
            2. La acción concreta que debe tomar basándose en la variante específica que le tocó
            3. El aspecto de su vida que requiere atención inmediata
            
            Usa lenguaje profesional, directo y orientado a la acción. Evita abstracciones excesivas.
            Dirígete a la persona directamente usando "usted" o la tercera persona.
            Responde en formato HTML simple (puedes usar <strong> o <em>).
            """

            # 3. Call Gemini API (Vertex AI)
            # Using Gemini 2.5 Pro - State-of-the-art thinking model
            model = GenerativeModel("gemini-2.5-pro")
            
            responses = model.generate_content(
                [prompt],
                generation_config={
                    "max_output_tokens": 256,
                    "temperature": 0.7,
                    "top_p": 0.95,
                },
                stream=False,
            )

            response_text = responses.text

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'reading': response_text}).encode('utf-8'))

        except Exception as e:
            print(f"Error in handler: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Star Oracle API Active")
